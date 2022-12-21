"""
List of URLs linked to operations that can be done on users and users related models.
"""
from django.conf import settings
from django.urls import include, path, re_path

from .views.association_users import (
    AssociationUsersDestroy,
    AssociationUsersListCreate,
    AssociationUsersRetrieve,
)
from .views.cas import CASLogin, CASLogout, cas_test, cas_verify
from .views.gdpr_consent_users import UserConsentsListCreate, UserConsentsRetrieve
from .views.user import (
    PasswordResetConfirm,
    UserAuthView,
    UserListCreate,
    UserRetrieveUpdateDestroy,
)
from .views.user_groups import (
    UserGroupsDestroy,
    UserGroupsListCreate,
    UserGroupsRetrieve,
)

urlpatterns = [
    path(
        "associations/",
        AssociationUsersListCreate.as_view(),
        name="user_associations_list_create",
    ),
    path(
        "associations/<int:user_id>",
        AssociationUsersRetrieve.as_view(),
        name="user_associations_retrieve",
    ),
    path(
        "associations/<int:user_id>/<int:association_id>",
        AssociationUsersDestroy.as_view(),
        name="user_associations_destroy",
    ),
    path("auth/cas/login/", CASLogin.as_view(), name="rest_cas_login"),
    path("auth/cas/logout/", CASLogout.as_view(), name="rest_cas_logout"),
    path("auth/user/", UserAuthView.as_view(), name="rest_user_details"),
    path("auth/", include("dj_rest_auth.urls")),
    re_path(
        r"auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$",
        PasswordResetConfirm.as_view(),
        name="password_reset_confirm",
    ),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "consents/", UserConsentsListCreate.as_view(), name="user_consents_list_create"
    ),
    path(
        "consents/<int:user_id>",
        UserConsentsRetrieve.as_view(),
        name="user_consents_retrieve",
    ),
    path("", UserListCreate.as_view(), name="user_list_create"),
    path("<int:pk>", UserRetrieveUpdateDestroy.as_view(), name="user_detail"),
    path("groups/", UserGroupsListCreate.as_view(), name="user_groups_list_create"),
    path(
        "groups/<int:user_id>",
        UserGroupsRetrieve.as_view(),
        name="user_groups_retrieve",
    ),
    path(
        "groups/<int:user_id>/<int:group_id>",
        UserGroupsDestroy.as_view(),
        name="user_groups_destroy",
    ),
]

if settings.DEBUG:  # pragma: no cover
    urlpatterns += [
        path("auth/cas_test/", cas_test, name="cas_test"),
        path("auth/cas_verify/", cas_verify, name="cas_verify"),
    ]
