from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from records.models import Record, next_record_number
from talukas.models import Taluka


class RecordSerializer(serializers.ModelSerializer):
    taluka_name = serializers.CharField(source="taluka.name", read_only=True)
    taluka_code = serializers.CharField(source="taluka.code", read_only=True)
    created_by_username = serializers.CharField(source="created_by.username", read_only=True)
    updated_by_username = serializers.CharField(source="updated_by.username", read_only=True, default=None)
    taluka_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Record
        fields = [
            "id",
            "taluka",
            "taluka_id",
            "taluka_name",
            "taluka_code",
            "created_by",
            "created_by_username",
            "updated_by",
            "updated_by_username",
            "record_number",
            "title",
            "description",
            "status",
            "is_active",
            "deleted_at",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"taluka": {"required": False}}
        read_only_fields = [
            "id",
            "created_by",
            "updated_by",
            "record_number",
            "deleted_at",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        request = self.context["request"]
        actor = request.user
        incoming = getattr(self, "initial_data", {}) or {}
        supplied = incoming.get("taluka_id", incoming.get("taluka", serializers.empty))

        if actor.is_super_admin:
            if self.instance is None:
                taluka = attrs.get("taluka")
                if supplied is not serializers.empty and supplied not in (None, ""):
                    taluka = Taluka.objects.filter(pk=supplied).first()
                    if not taluka:
                        raise serializers.ValidationError({"taluka": "Invalid Taluka."})
                if taluka is None:
                    raise serializers.ValidationError(
                        {"taluka": "Super Admin must specify taluka or taluka_id when creating a record."}
                    )
                attrs["taluka"] = taluka
            return attrs

        if supplied is not serializers.empty and supplied not in (None, ""):
            try:
                requested_id = int(getattr(supplied, "pk", supplied))
            except (TypeError, ValueError):
                requested_id = None
            if requested_id is not None and requested_id != actor.taluka_id:
                raise PermissionDenied("You cannot create or assign records to another Taluka.")

        attrs["taluka"] = actor.taluka
        if self.instance and self.instance.taluka_id != actor.taluka_id:
            raise PermissionDenied("You cannot modify records from another Taluka.")
        return attrs

    def create(self, validated_data):
        validated_data.pop("taluka_id", None)
        request = self.context["request"]
        taluka = validated_data["taluka"]
        validated_data["created_by"] = request.user
        validated_data["updated_by"] = request.user
        validated_data["record_number"] = next_record_number(taluka)
        validated_data.setdefault("status", Record.Status.ACTIVE)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("taluka_id", None)
        validated_data.pop("taluka", None)
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)
