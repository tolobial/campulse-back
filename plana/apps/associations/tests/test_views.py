"""
List of tests done on associations views.
"""
import json

from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from plana.apps.associations.models.association import Association


class AssociationsViewsTests(TestCase):
    """
    Main tests class.
    """

    fixtures = [
        "account_emailaddress.json",
        "associations_activityfield.json",
        "associations_association.json",
        "associations_institution.json",
        "associations_institutioncomponent.json",
        "associations_socialnetwork.json",
        "auth_group.json",
        "users_associationusers.json",
        "users_user.json",
        "users_user_groups.json",
    ]

    def setUp(self):
        """
        Start a default client used on all tests.
        """
        self.client = Client()
        url_login = reverse("rest_login")

        self.member_client = Client()
        data_member = {
            "username": "étudiant-asso-hors-site@mail.tld",
            "password": "motdepasse",
        }
        self.response = self.member_client.post(url_login, data_member)

        self.president_client = Client()
        data_president = {
            "username": "président-asso-hors-site@mail.tld",
            "password": "motdepasse",
        }
        self.response = self.president_client.post(url_login, data_president)

        self.crous_client = Client()
        data_crous = {
            "username": "gestionnaire-crous@mail.tld",
            "password": "motdepasse",
        }
        self.response = self.crous_client.post(url_login, data_crous)

        self.svu_client = Client()
        data_svu = {
            "username": "gestionnaire-svu@mail.tld",
            "password": "motdepasse",
        }
        self.response = self.svu_client.post(url_login, data_svu)

    def test_get_associations_list(self):
        """
        GET /associations/
        - There's at least one association in the associations list.
        - The route can be accessed by anyone.
        - We get the same amount of associations through the model and through the view.
        - Main associations details are returned (test the "name" attribute).
        - All associations details aren't returned (test the "activities" attribute).
        - Non-enabled associations can be filtered.
        - Site associations can be filtered.
        """
        associations_cnt = Association.objects.count()
        self.assertTrue(associations_cnt > 0)

        response = self.client.get("/associations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(len(content), associations_cnt)

        association_1 = content[0]
        self.assertTrue(association_1.get("name"))
        self.assertFalse(association_1.get("activities"))

        response = self.client.get("/associations/?is_enabled=true")
        for association in response.data:
            self.assertEqual(association["is_enabled"], True)

        response = self.client.get("/associations/?is_site=true")
        for association in response.data:
            self.assertEqual(association["is_site"], True)

    def test_post_association(self):
        """
        POST /associations/
        - A SVU manager can add an association.
        - A Crous manager cannot add an association.
        - Another user cannot add an association.
        - An association cannot be added twice, neither associations with similar names.
        - name field is mandatory.
        """
        response_svu = self.svu_client.post(
            "/associations/",
            {
                "name": "Les Fans de Georges la Saucisse",
            },
        )
        self.assertEqual(response_svu.status_code, status.HTTP_201_CREATED)

        response_crous = self.crous_client.post(
            "/associations/",
            {
                "name": "Quand Brice de Nice se connecte via CAS, c'est CASsé.",
            },
        )
        self.assertEqual(response_crous.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(
            "/associations/",
            {
                "name": "Quelle chanteuse se connecte sans compte à l'application ? Patricia CAS",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        similar_names = [
            "Les Fans de Georges la Saucisse",
            "LesFansdeGeorgeslaSaucisse",
            "lesfansdegeorgeslasaucisse",
            " Les Fans de Georges la Saucisse ",
            "Lés Fàns dè Gêörgës lâ Säùcîsse",
        ]
        for similar_name in similar_names:
            response_svu = self.svu_client.post(
                "/associations/",
                {"name": similar_name},
            )
            self.assertEqual(response_svu.status_code, status.HTTP_400_BAD_REQUEST)

        response_svu = self.svu_client.post("/associations/", {})
        self.assertEqual(response_svu.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_association_retrieve(self):
        """
        GET /associations/{id}
        - The route can be accessed by anyone.
        - Main association details are returned (test the "name" attribute).
        - All associations details are returned (test the "activities" attribute).
        - A non-existing association can't be returned.
        """
        association = Association.objects.get(pk=1)

        response = self.client.get("/associations/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        association_1 = json.loads(response.content.decode("utf-8"))
        self.assertEqual(association_1["name"], association.name)
        self.assertEqual(association_1["activities"], association.activities)

        not_found_response = self.client.get("/associations/50")
        self.assertEqual(not_found_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_association(self):
        """
        PATCH /associations/{id}
        - An anonymous user cannot execute this request.
        - A Crous manager cannot edit an association.
        - A SVU manager can edit an association.
        - A non-existing association cannot be edited.
        - Someone from an association without status can't edit infos from another association.
        - Someone from an association's office cannot edit informations from another association.
        - Someone from the association without status can't edit infos from the association.
        - Someone from the association's office can edit informations from the association.
        """
        association_id = 1
        response_anonymous = self.client.patch(
            f"/associations/{association_id}",
            {"name": "La Grande Confrérie du Cassoulet de Castelnaudary"},
            content_type="application/json",
        )
        self.assertEqual(response_anonymous.status_code, status.HTTP_401_UNAUTHORIZED)
        response_crous = self.crous_client.patch(
            f"/associations/{association_id}",
            {"name": "L'assaucissiation"},
            content_type="application/json",
        )
        self.assertEqual(response_crous.status_code, status.HTTP_400_BAD_REQUEST)
        response_svu = self.svu_client.patch(
            f"/associations/{association_id}",
            {
                "name": "Association Amicale des Amateurs d'Andouillette Authentique",
                "institution": 1,
                # TODO Find correct way to test social networks.
                # "social_networks": [
                #    {"type": "Mastodon", "location": "https://framapiaf.org/@Framasoft"}
                # ],
            },
            content_type="application/json",
        )
        self.assertEqual(response_svu.status_code, status.HTTP_200_OK)
        association = Association.objects.get(id=association_id)
        self.assertEqual(
            association.name,
            "Association Amicale des Amateurs d'Andouillette Authentique",
        )
        self.assertEqual(association.institution_id, 1)
        # self.assertEqual(len(association.social_networks), 1)

        association_id = 99
        response_svu = self.svu_client.patch(
            f"/associations/{association_id}",
            {"name": "La singularité de l'espace-temps."},
            content_type="application/json",
        )
        self.assertEqual(response_svu.status_code, status.HTTP_400_BAD_REQUEST)

        association_id = 2
        response_incorrect_member = self.member_client.patch(
            f"/associations/{association_id}",
            {"name": "Je suis pas de cette asso mais je veux l'éditer."},
            content_type="application/json",
        )
        self.assertEqual(
            response_incorrect_member.status_code, status.HTTP_400_BAD_REQUEST
        )
        response_incorrect_president = self.president_client.patch(
            f"/associations/{association_id}",
            {
                "name": "Je suis membre du bureau d'une autre asso, mais je veux l'éditer."
            },
            content_type="application/json",
        )
        self.assertEqual(
            response_incorrect_president.status_code, status.HTTP_400_BAD_REQUEST
        )

        association_id = 3
        response_correct_member = self.member_client.patch(
            f"/associations/{association_id}",
            {
                "name": "Ah et bah moi je suis de l'asso mais je peux pas l'éditer c'est terrible."
            },
            content_type="application/json",
        )
        self.assertEqual(
            response_correct_member.status_code, status.HTTP_400_BAD_REQUEST
        )
        response_correct_president = self.president_client.patch(
            f"/associations/{association_id}",
            {"name": "Moi je peux vraiment éditer l'asso, nananère."},
            content_type="application/json",
        )
        self.assertEqual(response_correct_president.status_code, status.HTTP_200_OK)
        association = Association.objects.get(id=association_id)
        self.assertEqual(
            association.name,
            "Moi je peux vraiment éditer l'asso, nananère.",
        )

    def test_delete_association(self):
        """
        DELETE /associations/{id}
        - An anonymous user cannot execute this request.
        - A Crous manager cannot delete an association.
        - A SVU manager can delete an association.
        """
        association_id = 1
        response_anonymous = self.client.delete(f"/associations/{association_id}")
        self.assertEqual(response_anonymous.status_code, status.HTTP_401_UNAUTHORIZED)
        response_crous = self.crous_client.delete(f"/associations/{association_id}")
        self.assertEqual(response_crous.status_code, status.HTTP_403_FORBIDDEN)
        response_svu = self.svu_client.delete(f"/associations/{association_id}")
        self.assertEqual(response_svu.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            Association.objects.get(id=association_id)

    def test_put_association(self):
        """
        PUT /associations/{id}
        - Request should return an error.
        """
        response = self.client.put(
            "/associations/1", {"name": "Les aficionados d'endives au jambon"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
