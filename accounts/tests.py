from django.core.management import call_command
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from records.models import Record
from talukas.models import Taluka


class SeededAPITestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_nanded", verbosity=0)

    def token(self, username, password):
        client = APIClient()
        response = client.post(
            "/api/auth/login/",
            {"username": username, "password": password},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        return client

    def results(self, response):
        data = response.data
        if isinstance(data, dict) and "results" in data:
            return data["results"]
        return data


class SuperAdminTests(SeededAPITestCase):
    def setUp(self):
        self.client = self.token("admin", "Admin@12345")

    def test_sees_all_talukas(self):
        response = self.client.get("/api/talukas/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.results(response)), 16)

    def test_sees_all_tahsildars(self):
        response = self.client.get("/api/tahsildars/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.results(response)), 16)

    def test_sees_all_users(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(self.results(response)), 1 + 16 + 48)

    def test_sees_all_records(self):
        response = self.client.get("/api/records/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(self.results(response)), 80)

    def test_admin_dashboard_counts(self):
        response = self.client.get("/api/dashboard/admin/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_talukas"], 16)
        self.assertEqual(response.data["total_tahsildars"], 16)
        self.assertEqual(response.data["total_users"], 48)
        self.assertGreaterEqual(response.data["total_records"], 80)

    def test_create_user_and_deactivate(self):
        nanded = Taluka.objects.get(code="NAN")
        response = self.client.post(
            "/api/users/",
            {
                "username": "nanded.extra",
                "first_name": "Extra",
                "last_name": "User",
                "phone": "9990001111",
                "password": "ExtraUser@12345",
                "role": "TALUKA_USER",
                "taluka": nanded.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        user_id = response.data["id"]
        patch = self.client.patch(
            f"/api/users/{user_id}/",
            {"first_name": "Updated"},
            format="json",
        )
        self.assertEqual(patch.status_code, 200)
        deact = self.client.post(f"/api/users/{user_id}/deactivate/")
        self.assertEqual(deact.status_code, 200)
        self.assertFalse(deact.data["is_active"])


class SuperAdminTahsildarCreateTests(SeededAPITestCase):
    def setUp(self):
        self.client = self.token("admin", "Admin@12345")

    def test_cannot_create_second_active_tahsildar_same_taluka(self):
        hadgaon = Taluka.objects.get(code="HAD")
        response = self.client.post(
            "/api/tahsildars/",
            {
                "username": "hadgaon.tahsildar2",
                "first_name": "Second",
                "last_name": "Tahsildar",
                "password": "SecondTahsildar@123",
                "taluka": hadgaon.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class HadgaonTahsildarTests(SeededAPITestCase):
    def setUp(self):
        self.client = self.token("hadgaon.tahsildar", "Tahsildar@123")
        self.hadgaon = Taluka.objects.get(code="HAD")
        self.nanded = Taluka.objects.get(code="NAN")
        self.nanded_user = User.objects.get(username="nanded.user1")
        self.nanded_record = Record.objects.get(record_number="NAN-001")
        self.hadgaon_user = User.objects.get(username="hadgaon.user1")

    def test_sees_only_hadgaon_users(self):
        response = self.client.get("/api/users/")
        usernames = {u["username"] for u in self.results(response)}
        self.assertTrue(all("hadgaon" in u for u in usernames))
        self.assertNotIn("nanded.user1", usernames)
        self.assertIn("hadgaon.user1", usernames)

    def test_sees_only_hadgaon_records(self):
        response = self.client.get("/api/records/")
        numbers = {r["record_number"] for r in self.results(response)}
        self.assertTrue(all(n.startswith("HAD-") for n in numbers))
        self.assertNotIn("NAN-001", numbers)

    def test_taluka_dashboard_isolated(self):
        response = self.client.get("/api/dashboard/taluka/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["taluka"], "Hadgaon")
        self.assertEqual(response.data["total_users"], 3)
        self.assertEqual(response.data["total_records"], 5)

    def test_cannot_see_nanded_user_by_id(self):
        response = self.client.get(f"/api/users/{self.nanded_user.id}/")
        self.assertIn(response.status_code, (403, 404))

    def test_cannot_update_nanded_user(self):
        response = self.client.put(
            f"/api/users/{self.nanded_user.id}/",
            {"first_name": "Hacked"},
            format="json",
        )
        self.assertIn(response.status_code, (403, 404))

    def test_cannot_delete_nanded_user(self):
        response = self.client.delete(f"/api/users/{self.nanded_user.id}/")
        self.assertIn(response.status_code, (403, 404))

    def test_cannot_see_nanded_record(self):
        response = self.client.get(f"/api/records/{self.nanded_record.id}/")
        self.assertIn(response.status_code, (403, 404))

    def test_cannot_update_nanded_record(self):
        response = self.client.patch(
            f"/api/records/{self.nanded_record.id}/",
            {"title": "Hacked"},
            format="json",
        )
        self.assertIn(response.status_code, (403, 404))

    def test_reject_creating_user_in_nanded(self):
        response = self.client.post(
            "/api/users/",
            {
                "username": "sneaky.nanded",
                "first_name": "Sneaky",
                "last_name": "User",
                "phone": "9111111111",
                "password": "SneakyUser@12345",
                "taluka_id": self.nanded.id,
            },
            format="json",
        )
        self.assertIn(response.status_code, (400, 403))
        self.assertFalse(User.objects.filter(username="sneaky.nanded").exists())

    def test_create_hadgaon_user_forces_taluka(self):
        response = self.client.post(
            "/api/users/",
            {
                "username": "hadgaon.user4",
                "first_name": "New",
                "last_name": "User",
                "phone": "9999999999",
                "password": "UserExtra@12345",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["role"], "TALUKA_USER")
        self.assertEqual(response.data["taluka"], self.hadgaon.id)

    def test_cannot_change_own_taluka(self):
        me = User.objects.get(username="hadgaon.tahsildar")
        response = self.client.patch(
            f"/api/users/{me.id}/",
            {"taluka": self.nanded.id},
            format="json",
        )
        self.assertIn(response.status_code, (400, 403))
        me.refresh_from_db()
        self.assertEqual(me.taluka_id, self.hadgaon.id)

    def test_cannot_create_tahsildar(self):
        response = self.client.post(
            "/api/tahsildars/",
            {
                "username": "another.tahsildar",
                "password": "AnotherTahsildar@123",
                "taluka": self.hadgaon.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_create_hadgaon_record(self):
        response = self.client.post(
            "/api/records/",
            {"title": "Hadgaon extra record", "description": "Created by tahsildar"},
            format="json",
        )
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["taluka"], self.hadgaon.id)
        self.assertTrue(response.data["record_number"].startswith("HAD-"))

    def test_update_and_deactivate_own_taluka_user(self):
        response = self.client.patch(
            f"/api/users/{self.hadgaon_user.id}/",
            {"first_name": "UpdatedHadgaon"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        deact = self.client.post(f"/api/users/{self.hadgaon_user.id}/deactivate/")
        self.assertEqual(deact.status_code, 200)
        self.assertFalse(deact.data["is_active"])


class HadgaonUserTests(SeededAPITestCase):
    def setUp(self):
        self.client = self.token("hadgaon.user1", "User@12345")
        self.nanded = Taluka.objects.get(code="NAN")
        self.nanded_record = Record.objects.get(record_number="NAN-001")
        self.ardhapur = Taluka.objects.get(code="ARD")

    def test_login_and_me(self):
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "hadgaon.user1")
        self.assertEqual(response.data["role"], "TALUKA_USER")

    def test_sees_hadgaon_records_only(self):
        response = self.client.get("/api/records/")
        numbers = {r["record_number"] for r in self.results(response)}
        self.assertTrue(numbers)
        self.assertTrue(all(n.startswith("HAD-") for n in numbers))

    def test_cannot_access_nanded_or_ardhapur_talukas(self):
        r1 = self.client.get(f"/api/talukas/{self.nanded.id}/")
        r2 = self.client.get(f"/api/talukas/{self.ardhapur.id}/")
        self.assertIn(r1.status_code, (403, 404))
        self.assertIn(r2.status_code, (403, 404))

    def test_cannot_see_nanded_record(self):
        response = self.client.get(f"/api/records/{self.nanded_record.id}/")
        self.assertIn(response.status_code, (403, 404))

    def test_cannot_change_role(self):
        me = User.objects.get(username="hadgaon.user1")
        response = self.client.patch(
            f"/api/users/{me.id}/",
            {"role": "SUPER_ADMIN"},
            format="json",
        )
        self.assertIn(response.status_code, (400, 403))
        me.refresh_from_db()
        self.assertEqual(me.role, User.Role.TALUKA_USER)

    def test_cannot_change_taluka(self):
        me = User.objects.get(username="hadgaon.user1")
        response = self.client.patch(
            f"/api/users/{me.id}/",
            {"taluka": self.nanded.id},
            format="json",
        )
        self.assertIn(response.status_code, (400, 403))
        me.refresh_from_db()
        self.assertEqual(me.taluka.code, "HAD")

    def test_cannot_create_tahsildar(self):
        response = self.client.post(
            "/api/tahsildars/",
            {
                "username": "evil.tahsildar",
                "password": "EvilTahsildar@123",
                "taluka": self.nanded.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_cannot_access_admin_dashboard(self):
        response = self.client.get("/api/dashboard/admin/")
        self.assertEqual(response.status_code, 403)

    def test_cannot_view_audit_logs(self):
        response = self.client.get("/api/audit-logs/")
        self.assertEqual(response.status_code, 403)
