from rest_framework.permissions import BasePermission


class CanAccessRecord(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_super_admin:
            return True
        return obj.taluka_id == user.taluka_id
