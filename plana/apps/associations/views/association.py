"""Views directly linked to associations."""

import json
import unicodedata

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.translation import gettext_lazy as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import filters, generics, response, status
from rest_framework.permissions import AllowAny, DjangoModelPermissions, IsAuthenticated

from plana.apps.associations.models.association import Association
from plana.apps.associations.serializers.association import (
    AssociationAllDataSerializer,
    AssociationMandatoryDataSerializer,
    AssociationNameSerializer,
    AssociationPartialDataSerializer,
)
from plana.apps.users.models.user import AssociationUsers
from plana.libs.mail_template.models import MailTemplate
from plana.utils import send_mail, to_bool


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description="Association name.",
            ),
            OpenApiParameter(
                "acronym",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description="Association acronym.",
            ),
            OpenApiParameter(
                "is_enabled",
                OpenApiTypes.BOOL,
                OpenApiParameter.QUERY,
                description="Filter for non-validated associations.",
            ),
            OpenApiParameter(
                "is_public",
                OpenApiTypes.BOOL,
                OpenApiParameter.QUERY,
                description="Filter for associations shown in the public list.",
            ),
            OpenApiParameter(
                "is_site",
                OpenApiTypes.BOOL,
                OpenApiParameter.QUERY,
                description="Filter for associations from site.",
            ),
            OpenApiParameter(
                "institution",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description="Filter by Institution ID.",
            ),
            OpenApiParameter(
                "institution_component",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description="Filter by Institution Component ID.",
            ),
            OpenApiParameter(
                "activity_field",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description="Filter by Activity Field ID.",
            ),
            OpenApiParameter(
                "user_id",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description="Filter by User ID.",
            ),
        ]
    )
)
class AssociationListCreate(generics.ListCreateAPIView):
    """/associations/ route"""

    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name__nospaces__unaccent",
        "acronym__nospaces__unaccent",
        "activity_field__name__nospaces__unaccent",
        "institution__name__nospaces__unaccent",
        "institution_component__name__nospaces__unaccent",
    ]

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated, DjangoModelPermissions]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Association.objects.all().order_by("name")
        if self.request.method == "GET":
            name = self.request.query_params.get("name")
            acronym = self.request.query_params.get("acronym")
            is_enabled = self.request.query_params.get("is_enabled")
            is_public = self.request.query_params.get("is_public")
            is_site = self.request.query_params.get("is_site")
            institution = self.request.query_params.get("institution")
            institution_component = self.request.query_params.get(
                "institution_component"
            )
            activity_field = self.request.query_params.get("activity_field")
            user_id = self.request.query_params.get("user_id")

            if self.request.user.is_anonymous:
                is_enabled = True
                is_public = True

            if not self.request.user.is_anonymous and not self.request.user.has_perm(
                "associations.view_association_not_enabled"
            ):
                is_enabled = True

            if not self.request.user.is_anonymous and not self.request.user.has_perm(
                "associations.view_association_not_public"
            ):
                is_public = True

            if name is not None and name != "":
                name = str(name).strip()
                queryset = queryset.filter(
                    name__nospaces__unaccent__icontains=name.replace(" ", "")
                )
            if acronym is not None and acronym != "":
                acronym = str(acronym).strip()
                queryset = queryset.filter(acronym__icontains=acronym)
            if is_enabled is not None and is_enabled != "":
                queryset = queryset.filter(is_enabled=to_bool(is_enabled))
            if is_public is not None and is_public != "":
                queryset = queryset.filter(is_public=to_bool(is_public))
            if is_site is not None and is_site != "":
                queryset = queryset.filter(is_site=to_bool(is_site))
            if institution is not None and institution != "":
                queryset = queryset.filter(institution_id=institution)
            if institution_component is not None:
                if institution_component == "":
                    queryset = queryset.filter(institution_component_id__isnull=True)
                else:
                    queryset = queryset.filter(
                        institution_component_id=institution_component
                    )
            if activity_field is not None and activity_field != "":
                queryset = queryset.filter(activity_field_id=activity_field)
            if (
                user_id is not None
                and user_id != ""
                and self.request.user.has_perm("users.view_user_anyone")
            ):
                assos_users_query = (
                    AssociationUsers.objects.filter(user_id=user_id)
                    .values_list("association_id", flat=True)
                    .all()
                )
                queryset = queryset.filter(id__in=assos_users_query)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            self.serializer_class = AssociationMandatoryDataSerializer
        else:
            self.serializer_class = AssociationPartialDataSerializer
        return super().get_serializer_class()

    def get(self, request, *args, **kwargs):
        """Lists all associations with many filters."""
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Creates a new association with mandatory informations (manager only)."""
        if "name" in request.data:
            association_name = request.data["name"]
        else:
            return response.Response(
                {"error": _("No association name given.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            not "institution" in request.data
            and request.user.get_user_institutions().count() == 1
        ):
            request.data["institution"] = (
                request.user.get_user_institutions().first().id
            )
        elif not "institution" in request.data:
            return response.Response(
                {"error": _("No institution given.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not request.user.has_perm(
            "associations.add_association_any_institution"
        ) and not request.user.is_staff_in_institution(request.data["institution"]):
            return response.Response(
                {
                    "error": _(
                        "Not allowed to create an association for this institution."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Removes spaces, uppercase and accented characters to avoid similar association names.
        new_association_name = (
            unicodedata.normalize(
                "NFD", association_name.strip().replace(" ", "").lower()
            )
            .encode("ascii", "ignore")
            .decode("utf-8")
        )
        associations = Association.objects.all()
        for association in associations:
            existing_association_name = (
                unicodedata.normalize(
                    "NFD", association.name.strip().replace(" ", "").lower()
                )
                .encode("ascii", "ignore")
                .decode("utf-8")
            )
            if new_association_name == existing_association_name:
                return response.Response(
                    {"error": _("Association name already taken.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if "is_site" not in request.data:
            request.data["is_site"] = settings.ASSOCIATION_IS_SITE_DEFAULT
        elif to_bool(request.data["is_site"]) is True:
            request.data["is_enabled"] = True
            request.data["is_public"] = True

        return super().create(request, *args, **kwargs)


@extend_schema(methods=["PUT"], exclude=True)
class AssociationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """/associations/{id} route"""

    queryset = Association.objects.all()
    serializer_class = AssociationAllDataSerializer

    def get_permissions(self):
        if self.request.method in ("PATCH", "DELETE"):
            self.permission_classes = [IsAuthenticated, DjangoModelPermissions]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get(self, request, *args, **kwargs):
        """Retrieves an association with all its details."""
        try:
            association_id = kwargs["pk"]
            association = Association.objects.get(id=association_id)
        except (ObjectDoesNotExist, MultiValueDictKeyError):
            return response.Response(
                {"error": _("No association id given.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user.is_anonymous and (
            not association.is_enabled or not association.is_public
        ):
            return response.Response(
                {"error": _("Association not visible.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            not request.user.is_anonymous
            and not association.is_enabled
            and not request.user.is_in_association(association_id)
            and not request.user.has_perm("associations.view_association_not_enabled")
        ):
            return response.Response(
                {"error": _("Association not enabled.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            not request.user.is_anonymous
            and not association.is_public
            and not request.user.is_in_association(association_id)
            and not request.user.has_perm("associations.view_association_not_public")
        ):
            return response.Response(
                {"error": _("Association not public.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return response.Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # WARNING : to upload images the form sent must be "multipart/form-data" encoded
    def patch(self, request, *args, **kwargs):
        """Updates association details (president and manager only, restricted fields for president)."""
        try:
            association_id = kwargs["pk"]
            association = Association.objects.get(id=association_id)
        except (ObjectDoesNotExist, MultiValueDictKeyError):
            return response.Response(
                {"error": _("No association id given.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            not request.user.is_president_in_association(association_id)
            and not request.user.has_perm(
                "associations.change_association_any_institution"
            )
            and not request.user.is_staff_in_institution(association.institution_id)
        ):
            return response.Response(
                {"error": _("No rights to edit this association.")},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            social_networks_data = (
                request.data["social_networks"]
                if "social_networks" in request.data
                else []
            )
            social_networks = (
                json.loads(social_networks_data)
                if isinstance(social_networks_data, str)
                else json.loads(json.dumps(social_networks_data))
            )
            for social_network in social_networks:
                if sorted(list(social_network.keys())) != sorted(["type", "location"]):
                    return response.Response(
                        {"error": _("Wrong social_networks parameters")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if not all(isinstance(s, str) for s in list(social_network.values())):
                    return response.Response(
                        {"error": _("Wrong social_networks values")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        except Exception as ex:
            print(ex)
            return response.Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if request.user.has_perm("associations.change_association_all_fields"):
            if "is_site" in request.data:
                is_site = to_bool(request.data["is_site"])
                if is_site is False:
                    request.data["is_public"] = False

            if "is_enabled" in request.data:
                is_enabled = to_bool(request.data["is_enabled"])
                if is_enabled is False:
                    request.data["is_public"] = False

        else:
            for restricted_field in [
                "amount_members_allowed",
                "can_submit_projects",
                "charter_status",
                "creation_date",
                "institution_id",
                "is_enabled",
                "is_site",
            ]:
                request.data.pop(restricted_field, False)

        if "is_public" in request.data:
            is_public = to_bool(request.data["is_public"])
            if is_public is True and (
                association.is_site is False or association.is_enabled is False
            ):
                request.data["is_public"] = False

        current_site = get_current_site(request)
        context = {
            "site_domain": current_site.domain,
            "site_name": current_site.name,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "association_name": association.name,
        }
        template = MailTemplate.objects.get(code="ASSOCIATION_CONTENT_CHANGE")
        send_mail(
            from_=settings.DEFAULT_FROM_EMAIL,
            to_=request.user.email,
            subject=template.subject.replace("{{ site_name }}", context["site_name"]),
            message=template.parse_vars(request.user, request, context),
        )

        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Destroys an entire association (manager only)."""
        try:
            association_id = kwargs["pk"]
            association = Association.objects.get(id=association_id)
        except (ObjectDoesNotExist, MultiValueDictKeyError):
            return response.Response(
                {"error": _("No association id given.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if association.is_enabled is True:
            return response.Response(
                {"error": _("Can't delete an enabled association.")},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not request.user.has_perm(
            "associations.delete_association_any_institution"
        ) and not request.user.is_staff_in_institution(association.institution):
            return response.Response(
                {
                    "error": _(
                        "Not allowed to delete an association for this institution."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if association.email:
            current_site = get_current_site(request)
            context = {
                "site_domain": current_site.domain,
                "site_name": current_site.name,
            }
            template = MailTemplate.objects.get(code="ASSOCIATION_DELETE")
            send_mail(
                from_=settings.DEFAULT_FROM_EMAIL,
                to_=association.email,
                subject=template.subject.replace(
                    "{{ site_name }}", context["site_name"]
                ),
                message=template.parse_vars(request.user, request, context),
            )
        return self.destroy(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                "institutions",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description="Filter by Institutions IDs.",
            ),
            OpenApiParameter(
                "is_public",
                OpenApiTypes.BOOL,
                OpenApiParameter.QUERY,
                description="Filter for associations shown in the public list.",
            ),
            OpenApiParameter(
                "allow_new_users",
                OpenApiTypes.BOOL,
                OpenApiParameter.QUERY,
                description="Filter for associations where registration is possible.",
            ),
        ]
    )
)
class AssociationNameList(generics.ListAPIView):
    """/associations/names route"""

    permission_classes = [AllowAny]
    serializer_class = AssociationNameSerializer

    def get_queryset(self):
        queryset = Association.objects.all()
        institutions = self.request.query_params.get("institutions")
        is_public = self.request.query_params.get("is_public")
        allow_new_users = self.request.query_params.get("allow_new_users")
        if institutions is not None and institutions != "":
            queryset = queryset.filter(institution_id__in=institutions.split(","))
        if is_public is not None and is_public != "":
            queryset = queryset.filter(is_public=to_bool(is_public))
        if allow_new_users is not None and allow_new_users != "":
            assos_ids_with_all_members = []
            for association in queryset:
                association_users = AssociationUsers.objects.filter(
                    association_id=association.id
                )
                if (
                    not association.amount_members_allowed is None
                    and association_users.count() >= association.amount_members_allowed
                ):
                    assos_ids_with_all_members.append(association.id)
            if to_bool(allow_new_users) is True:
                queryset = queryset.exclude(id__in=assos_ids_with_all_members)
            else:
                queryset = queryset.filter(id__in=assos_ids_with_all_members)

        return queryset.order_by("name")

    def get(self, request, *args, **kwargs):
        """Lists minimal details for all associations with many filters."""
        return self.list(request, *args, **kwargs)
