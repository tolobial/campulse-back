"""
Views directly linked to associations.
"""
import json
import unicodedata

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.translation import gettext_lazy as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import generics, response, status
from rest_framework.permissions import AllowAny, IsAuthenticated

from plana.apps.associations.models.activity_field import ActivityField
from plana.apps.associations.models.association import Association
from plana.apps.associations.models.institution import Institution
from plana.apps.associations.models.institution_component import InstitutionComponent
from plana.apps.associations.serializers.activity_field import ActivityFieldSerializer
from plana.apps.associations.serializers.association import (
    AssociationAllDataNoSubTableSerializer,
    AssociationAllDataSerializer,
    AssociationMandatoryDataSerializer,
    AssociationPartialDataSerializer,
)
from plana.apps.associations.serializers.institution import InstitutionSerializer
from plana.apps.associations.serializers.institution_component import (
    InstitutionComponentSerializer,
)
from plana.apps.users.models.association_users import AssociationUsers
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
        ]
    )
)
class AssociationListCreate(generics.ListCreateAPIView):
    """
    GET : Lists all associations currently active.

    POST : Creates a new association with mandatory informations.
    """

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
            if name is not None:
                name = str(name).strip()
                queryset = queryset.filter(
                    name__nospaces__unaccent__icontains=name.replace(" ", "")
                )
            if acronym is not None:
                acronym = str(acronym).strip()
                queryset = queryset.filter(acronym__icontains=acronym)
            if is_enabled is not None:
                queryset = queryset.filter(is_enabled=to_bool(is_enabled))
            if is_public is not None:
                queryset = queryset.filter(is_public=to_bool(is_public))
            if is_site is not None:
                queryset = queryset.filter(is_site=to_bool(is_site))
            if institution is not None:
                if institution == "":
                    queryset = queryset.filter(institution_id__isnull=True)
                else:
                    queryset = queryset.filter(institution_id=institution)
            if institution_component is not None:
                queryset = queryset.filter(
                    institution_component_id=institution_component
                )
            if activity_field is not None:
                queryset = queryset.filter(activity_field_id=activity_field)
        return queryset

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == "POST":
            self.serializer_class = AssociationMandatoryDataSerializer
        else:
            self.serializer_class = AssociationPartialDataSerializer
        return super().get_serializer_class()

    def post(self, request, *args, **kwargs):
        if request.user.is_svu_manager:
            if "name" in request.data:
                association_name = request.data["name"]
            else:
                return response.Response(
                    {"error": _("No association name given.")},
                    status=status.HTTP_400_BAD_REQUEST,
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
            return super().create(request, *args, **kwargs)
        return response.Response(
            {"error": _("Bad request.")},
            status=status.HTTP_403_FORBIDDEN,
        )


@extend_schema(methods=["PUT"], exclude=True)
class AssociationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    GET : Lists an association with all its details.

    PATCH : Edit association details (with different permissions for SVU and president).

    DELETE : Removes an entire association.
    """

    serializer_class = AssociationAllDataSerializer
    queryset = Association.objects.all()

    def get_permissions(self):
        if self.request.method in ("PATCH", "DELETE"):
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            self.serializer_class = AssociationAllDataNoSubTableSerializer
        else:
            self.serializer_class = AssociationAllDataSerializer
        return super().get_serializer_class()

    def put(self, request, *args, **kwargs):
        return response.Response({}, status=status.HTTP_404_NOT_FOUND)

    # WARNING : to upload images the form sent must be "multipart/form-data" encoded
    def patch(self, request, *args, **kwargs):
        try:
            association_id = kwargs["pk"]
            association = Association.objects.get(id=association_id)
        except (ObjectDoesNotExist, MultiValueDictKeyError):
            return response.Response(
                {"error": _("No association id given.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "is_site" in request.data:
            is_site = to_bool(request.data["is_site"])
            if is_site is False:
                request.data["is_public"] = False

        if "is_enabled" in request.data:
            is_enabled = to_bool(request.data["is_enabled"])
            if is_enabled is False:
                request.data["is_public"] = False

        if "is_public" in request.data:
            is_public = to_bool(request.data["is_public"])
            if is_public is True and (
                association.is_site is False or association.is_enabled is False
            ):
                request.data["is_public"] = False

        try:
            social_networks = (
                json.loads(request.data["social_networks"])
                if "social_networks" in request.data
                else []
            )
            for social_network in social_networks:
                if sorted(list(social_network.keys())) != sorted(['type', 'location']):
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

        if not request.user.is_svu_manager:
            try:
                AssociationUsers.objects.get(
                    user_id=request.user.pk,
                    association_id=association_id,
                    has_office_status=True,
                )
                for restricted_field in [
                    "is_enabled",
                    "is_site",
                    "creation_date",
                ]:
                    request.data.pop(restricted_field, False)
            except (ObjectDoesNotExist, MultiValueDictKeyError):
                return response.Response(
                    {"error": _("No office link between association and user found.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

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
        try:
            association_id = kwargs["pk"]
            association = Association.objects.get(id=association_id)
        except (ObjectDoesNotExist, MultiValueDictKeyError):
            return response.Response(
                {"error": _("No association id given.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.user.is_svu_manager:
            if association.is_enabled is True:
                return response.Response(
                    {"error": _("Can't delete an enabled association.")},
                    status=status.HTTP_400_BAD_REQUEST,
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
        return response.Response(
            {"error": _("Bad request.")},
            status=status.HTTP_403_FORBIDDEN,
        )


class AssociationActivityFieldList(generics.ListAPIView):
    """
    GET : Lists all activity fields.
    """

    serializer_class = ActivityFieldSerializer

    def get_queryset(self):
        return ActivityField.objects.all().order_by("name")


class AssociationInstitutionComponentList(generics.ListAPIView):
    """
    GET : Lists all institution components.
    """

    serializer_class = InstitutionComponentSerializer

    def get_queryset(self):
        return InstitutionComponent.objects.all().order_by("name")


class AssociationInstitutionList(generics.ListAPIView):
    """
    GET : Lists all institutions.
    """

    serializer_class = InstitutionSerializer

    def get_queryset(self):
        return Institution.objects.all().order_by("name")
