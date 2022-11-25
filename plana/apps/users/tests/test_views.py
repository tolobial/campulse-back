import json

from django.test import TestCase, Client
from django.contrib.auth.models import Group

from django.urls import reverse
from rest_framework import status

from django.core import serializers

from plana.apps.users.models.user import User, AssociationUsers
from plana.apps.groups.serializers.group import GroupSerializer


class UserTests(TestCase):
    fixtures = [
        "associations_activityfield.json",
        "associations_association.json",
        "associations_institution.json",
        "associations_institutioncomponent.json",
        "associations_socialnetwork.json",
        "account_emailaddress.json",
        "auth_group.json",
        "users_associationsusers.json",
        "users_user.json",
        "users_user_groups.json",
    ]

    def setUp(self):
        self.client = Client()
        url = reverse("rest_login")
        data = {
            "username": "test@pas-unistra.fr",
            "password": "motdepasse",
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse("home")

        self.anonymous_client = Client()

    # TODO Route doesn't exist anymore at this time.
    """
    def test_get_users_list(self):
        users_cnt = User.objects.count()
        self.assertTrue(users_cnt > 0)

        response = self.client.get(reverse("user_list"))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(len(content), users_cnt)
    """

    def test_get_user_detail(self):
        user = User.objects.get(pk=2)

        response = self.client.get("/users/auth/user/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        user_1 = json.loads(response.content.decode("utf-8"))
        self.assertEqual(user_1["username"], user.username)

    def test_get_associations_user_list(self):
        associations_user_cnt = AssociationUsers.objects.count()
        self.assertTrue(associations_user_cnt > 0)

        response = self.client.get("/users/associations/2")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    # TODO : add rights management
    def test_get_user_groups_list(self):
        user = User.objects.get(pk=2)
        groups = list(user.groups.all().values("id", "name"))

        response = self.client.get("/users/groups/2")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        response_unauthorized = self.anonymous_client.get("/users/groups/2")
        self.assertEquals(response_unauthorized.status_code, status.HTTP_401_UNAUTHORIZED)

        get_groups = json.loads(response.content.decode("utf-8"))
        self.assertEqual(get_groups, groups)
