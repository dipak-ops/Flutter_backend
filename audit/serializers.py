from rest_framework import serializers

from audit.models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True, default=None)
    taluka_name = serializers.CharField(source="taluka.name", read_only=True, default=None)

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "user",
            "username",
            "action",
            "target_type",
            "target_id",
            "taluka",
            "taluka_name",
            "ip_address",
            "timestamp",
            "metadata",
        ]
        read_only_fields = fields
