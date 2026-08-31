from django.test import TestCase

from audit.models import AuditLog
from audit.services import log_action
from django.core.management import call_command

from accounts.models import User


class AuditLogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_nanded", verbosity=0)

    def test_login_creates_audit_log(self):
        from rest_framework.test import APIClient

        client = APIClient()
        client.post(
            "/api/auth/login/",
            {"username": "admin", "password": "Admin@12345"},
            format="json",
        )
        self.assertTrue(AuditLog.objects.filter(action="LOGIN", user__username="admin").exists())

    def test_log_action_helper(self):
        user = User.objects.get(username="admin")
        log_action(user=user, action="USER_UPDATED", target_type="User", target_id=user.pk)
        self.assertTrue(AuditLog.objects.filter(action="USER_UPDATED").exists())
