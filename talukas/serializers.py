from rest_framework import serializers

from talukas.models import Taluka


class TalukaSerializer(serializers.ModelSerializer):
    user_count = serializers.IntegerField(read_only=True)
    record_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Taluka
        fields = [
            "id",
            "name",
            "code",
            "is_active",
            "user_count",
            "record_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
