"""Models describing users and most of its details."""
import datetime

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _

from plana.apps.associations.models.association import Association
from plana.apps.commissions.models.commission import Commission
from plana.apps.commissions.models.commission_date import CommissionDate
from plana.apps.institutions.models.institution import Institution
from plana.apps.projects.models.project_commission_date import ProjectCommissionDate
from plana.apps.users.provider import CASProvider


class AssociationUser(models.Model):
    """Model that defines the link between a user and an association."""

    user = models.ForeignKey("User", verbose_name=_("User"), on_delete=models.CASCADE)
    association = models.ForeignKey(
        Association, verbose_name=_("Association"), on_delete=models.CASCADE
    )
    is_president = models.BooleanField(_("Is president"), default=False)
    can_be_president_from = models.DateField(_("Can be president from"), null=True)
    can_be_president_to = models.DateField(_("Can be president to"), null=True)
    is_validated_by_admin = models.BooleanField(
        _("Is validated by admin"), default=False
    )
    is_vice_president = models.BooleanField(_("Is vice president"), default=False)
    is_secretary = models.BooleanField(_("Is secretary"), default=False)
    is_treasurer = models.BooleanField(_("Is treasurer"), default=False)

    def __str__(self):
        return f"{self.user}, {self.association}"

    class Meta:
        verbose_name = _("Association")
        verbose_name_plural = _("Associations")
        permissions = [
            (
                "change_associationuser_any_institution",
                "Can change associations for all users.",
            ),
            (
                "delete_associationuser_any_institution",
                "Can delete associations for all users.",
            ),
            ("view_associationuser_anyone", "Can view all associations for a user."),
        ]


class GroupInstitutionCommissionUser(models.Model):
    """
    Define the link between a user and a group.

    And an institution if user is a manager.
    And a commission if user is a commission member.
    """

    user = models.ForeignKey("User", verbose_name=_("User"), on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True)
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user}, {self.group}, {self.institution}, {self.commission}"

    class Meta:
        verbose_name = _("User Institution Commission Groups")
        verbose_name_plural = _("Users Institution Commission Groups")
        permissions = [
            (
                "add_groupinstitutioncommissionuser_any_group",
                "Can add restricted groups to a user.",
            ),
            (
                "delete_groupinstitutioncommissionuser_any_group",
                "Can delete restricted groups to a user.",
            ),
            (
                "view_groupinstitutioncommissionuser_any_group",
                "Can view all groups for a user.",
            ),
        ]


class User(AbstractUser):
    """
    Model that extends the abstract User class.

    Following fields from Django User class are used :
    - username
    - password
    - email
    - first_name
    - last_name
    - is_active
    """

    email = models.EmailField(_("Email"), unique=True)
    first_name = models.CharField(_("First name"), max_length=150, blank=False)
    last_name = models.CharField(_("Last name"), max_length=150, blank=False)
    address = models.TextField(_("Address"), default="")
    zipcode = models.CharField(_("Zipcode"), max_length=32, default="")
    city = models.CharField(_("City"), max_length=128, default="")
    country = models.CharField(_("Country"), max_length=128, default="")
    phone = models.CharField(_("Phone"), default="", max_length=32, null=True)
    can_submit_projects = models.BooleanField(_("Can submit projects"), default=True)
    password_last_change_date = models.DateField(
        _("Password last change date"), null=True
    )
    is_validated_by_admin = models.BooleanField(
        _("Is validated by administrator"), default=False
    )
    associations = models.ManyToManyField(
        Association, verbose_name=_("Associations"), through="AssociationUser"
    )
    groups_institutions_commissions = models.ManyToManyField(
        Group,
        verbose_name=_("Groups"),
        through="GroupInstitutionCommissionUser",
        related_name="group_institution_commission_set",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        """Overriden has_perm to check for institutions."""
        if self.is_superuser:
            return True
        return (
            Permission.objects.filter(
                group__id__in=Group.objects.filter(
                    id__in=GroupInstitutionCommissionUser.objects.filter(
                        user_id=self.pk
                    ).values_list("group_id")
                ).values_list("id"),
                codename=perm.split(".")[1],
            ).count()
            > 0
        )

    def can_access_project(self, project_obj):
        """Check if a user can access a project as association president, misc user, commission member, or manager."""
        if self.is_staff:
            if project_obj.association_id is not None:
                institution_id = Institution.objects.get(
                    id=Association.objects.get(
                        id=project_obj.association_id
                    ).institution_id
                )
                if institution_id not in self.get_user_managed_institutions():
                    return False
            if project_obj.user is not None and not self.has_perm(
                "users.change_user_misc"
            ):
                return False
            return True

        if self.get_user_commissions().count() != 0:
            user_commissions_ids = self.get_user_commissions().values_list("id")
            project_commissions_ids = CommissionDate.objects.filter(
                id__in=ProjectCommissionDate.objects.filter(
                    project_id=project_obj.id
                ).values_list("commission_date_id")
            ).values_list("commission_id")
            if (
                len(set(project_commissions_ids).intersection(user_commissions_ids))
                == 0
            ):
                return False
            return True

        if project_obj.association is not None:
            try:
                member = AssociationUser.objects.get(
                    user_id=self.pk, association_id=project_obj.association
                )
                if not member.is_president or not self.is_president_in_association(
                    project_obj.association
                ):
                    return False
            except ObjectDoesNotExist:
                return False
            return True

        if project_obj.user is not None:
            if project_obj.user != self:
                return False
            return True

    def get_user_associations(self):
        """Return a list of Association IDs linked to a student user."""
        return Association.objects.filter(
            id__in=AssociationUser.objects.filter(user_id=self.pk).values_list(
                "association_id"
            )
        )

    def get_user_managed_associations(self):
        """Return a list of Association IDs linked to a manager user."""
        return Association.objects.filter(
            institution_id__in=Institution.objects.filter(
                id__in=GroupInstitutionCommissionUser.objects.filter(
                    user_id=self.pk
                ).values_list("institution_id")
            ).values_list("id")
        )

    def get_user_commissions(self):
        """Return a list of Commission IDs linked to a student user."""
        return Commission.objects.filter(
            id__in=GroupInstitutionCommissionUser.objects.filter(
                user_id=self.pk
            ).values_list("commission_id")
        )

    def get_user_managed_commissions(self):
        """Return a list of Commission IDs linked to a manager user."""
        return Commission.objects.filter(
            institution_id__in=Institution.objects.filter(
                id__in=GroupInstitutionCommissionUser.objects.filter(
                    user_id=self.pk
                ).values_list("institution_id")
            ).values_list("id")
        )

    def get_user_groups(self):
        """Return a list of Group IDs linked to a user."""
        return Group.objects.filter(
            id__in=GroupInstitutionCommissionUser.objects.filter(
                user_id=self.pk
            ).values_list("group_id")
        )

    def get_user_institutions(self):
        """Return a list of Institution IDs linked to a student user."""
        return Institution.objects.filter(
            id__in=Association.objects.filter(
                id__in=AssociationUser.objects.filter(user_id=self.pk).values_list(
                    "association_id"
                )
            ).values_list("institution_id")
        )

    def get_user_managed_institutions(self):
        """Return a list of Institution IDs linked to a manager user."""
        return Institution.objects.filter(
            id__in=GroupInstitutionCommissionUser.objects.filter(
                user_id=self.pk
            ).values_list("institution_id")
        )

    def has_validated_email_user(self):
        """Return True if the user account has a validated email."""
        try:
            EmailAddress.objects.get(user_id=self.pk, email=self.email, verified=True)
            return True
        except ObjectDoesNotExist:
            return False

    def is_cas_user(self):
        """Return True if the user account was generated through CAS on signup."""
        try:
            self.socialaccount_set.get(provider=CASProvider.id)
            return True
        except SocialAccount.DoesNotExist:
            return False

    def is_in_association(self, association_id):
        """Check if a user can read an association."""
        try:
            AssociationUser.objects.get(
                user_id=self.pk,
                association_id=association_id,
                is_validated_by_admin=True,
            )
            return True
        except ObjectDoesNotExist:
            return False

    def is_president_in_association(self, association_id):
        """Check if a user can write in an association."""
        try:
            now = datetime.datetime.now()
            AssociationUser.objects.filter(
                models.Q(is_president=True)
                | models.Q(
                    can_be_president_from__gte=now,
                    can_be_president_to__isnull=True,
                )
                | models.Q(
                    can_be_president_from__isnull=True,
                    can_be_president_to__lte=now,
                )
                | models.Q(
                    can_be_president_from__gte=now,
                    can_be_president_to__lte=now,
                )
            ).get(
                user_id=self.pk,
                association_id=association_id,
                is_validated_by_admin=True,
            )
            return True
        except ObjectDoesNotExist:
            return False

    def is_staff_for_association(self, association_id):
        """Check if a user is linked as manager for an association."""
        if self.is_staff:
            return GroupInstitutionCommissionUser.objects.filter(
                user_id=self.pk,
                institution_id=Association.objects.get(
                    id=association_id
                ).institution_id,
            )
        return False

    def is_staff_in_institution(self, institution_id):
        """Check if a user is linked as manager to an institution."""
        if self.is_staff:
            return GroupInstitutionCommissionUser.objects.filter(
                user_id=self.pk, institution_id=institution_id
            )
        return False

    def is_member_in_commission(self, commission_id):
        """Check if a user is linked as member to a commission."""
        return GroupInstitutionCommissionUser.objects.filter(
            user_id=self.pk, commission_id=commission_id
        )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        permissions = [
            ("add_user_misc", "Can add a user with no association linked."),
            ("change_user_misc", "Can change a user with no association linked."),
            ("change_user_all_fields", "Can change can_submit_projects on a user."),
            ("delete_user_misc", "Can delete a user with no association linked."),
            ("view_user_misc", "Can view a user with no association linked."),
            ("view_user_anyone", "Can view all users."),
        ]
