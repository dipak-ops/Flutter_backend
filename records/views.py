from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from audit.services import get_client_ip, log_action
from records.models import Record
from records.serializers import RecordSerializer


def scoped_records(user):
    qs = Record.objects.select_related("taluka", "created_by", "updated_by")
    if user.is_super_admin:
        return qs
    if user.taluka_id:
        return qs.filter(taluka_id=user.taluka_id)
    return qs.none()


class RecordViewSet(viewsets.ModelViewSet):
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return scoped_records(self.request.user)

    def perform_create(self, serializer):
        record = serializer.save()
        log_action(
            user=self.request.user,
            action="RECORD_CREATED",
            target_type="Record",
            target_id=record.pk,
            taluka=record.taluka,
            ip_address=get_client_ip(self.request),
            metadata={"record_number": record.record_number},
        )

    def perform_update(self, serializer):
        record = serializer.save()
        log_action(
            user=self.request.user,
            action="RECORD_UPDATED",
            target_type="Record",
            target_id=record.pk,
            taluka=record.taluka,
            ip_address=get_client_ip(self.request),
            metadata={"record_number": record.record_number},
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deactivate(user=request.user)
        log_action(
            user=request.user,
            action="RECORD_DEACTIVATED",
            target_type="Record",
            target_id=instance.pk,
            taluka=instance.taluka,
            ip_address=get_client_ip(request),
            metadata={"record_number": instance.record_number, "soft_delete": True},
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        instance = self.get_object()
        instance.activate(user=request.user)
        log_action(
            user=request.user,
            action="RECORD_UPDATED",
            target_type="Record",
            target_id=instance.pk,
            taluka=instance.taluka,
            ip_address=get_client_ip(request),
            metadata={"activated": True},
        )
        return Response(RecordSerializer(instance, context={"request": request}).data)

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        instance = self.get_object()
        instance.deactivate(user=request.user)
        log_action(
            user=request.user,
            action="RECORD_DEACTIVATED",
            target_type="Record",
            target_id=instance.pk,
            taluka=instance.taluka,
            ip_address=get_client_ip(request),
        )
        return Response(RecordSerializer(instance, context={"request": request}).data)
