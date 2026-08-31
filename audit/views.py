from rest_framework import viewsets

from accounts.permissions import IsSuperAdmin
from audit.models import AuditLog
from audit.serializers import AuditLogSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    permission_classes = [IsSuperAdmin]
    queryset = AuditLog.objects.select_related("user", "taluka").all()
