from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIClient

from talukas.models import Taluka


class TalukaIsolationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_nanded", verbosity=0)

    def auth(self, username, password):
        client = APIClient()
        response = client.post(
            "/api/auth/login/",
            {"username": username, "password": password},
            format="json",
        )
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        return client

    def test_tahsildar_sees_only_own_taluka(self):
        client = self.auth("hadgaon.tahsildar", "Tahsildar@123")
        response = client.get("/api/talukas/")
        results = response.data["results"] if "results" in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Hadgaon")

    def test_taluka_user_sees_only_own_taluka(self):
        client = self.auth("umri.user2", "User@12345")
        umri = Taluka.objects.get(code="UMR")
        response = client.get(f"/api/talukas/{umri.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], "UMR")
