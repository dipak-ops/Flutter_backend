from rest_framework.permissions import BasePermission


class CanAccessTaluka(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_super_admin:
            return True
        return user.taluka_id == obj.pk
