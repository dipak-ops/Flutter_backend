from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIClient

from records.models import Record


class RecordIsolationTests(TestCase):
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

    def test_hadgaon_tahsildar_denied_nanded_record(self):
        client = self.auth("hadgaon.tahsildar", "Tahsildar@123")
        record = Record.objects.get(record_number="NAN-001")
        response = client.get(f"/api/records/{record.id}/")
        self.assertIn(response.status_code, (403, 404))

    def test_record_create_ignores_foreign_taluka(self):
        client = self.auth("hadgaon.tahsildar", "Tahsildar@123")
        nanded_id = Record.objects.get(record_number="NAN-001").taluka_id
        response = client.post(
            "/api/records/",
            {
                "title": "Should stay in Hadgaon",
                "description": "Isolation test",
                "taluka_id": nanded_id,
            },
            format="json",
        )
        self.assertIn(response.status_code, (400, 403))
