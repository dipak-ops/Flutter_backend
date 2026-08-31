from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_super_admin)


class IsTahsildar(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_tahsildar)


class IsSuperAdminOrTahsildar(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_super_admin or user.is_tahsildar))


class IsAuthenticatedStaffOrTalukaScoped(BasePermission):
    """Authenticated users; write operations extra-checked in views."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class TalukaObjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_super_admin:
            return True
        taluka_id = getattr(obj, "taluka_id", None)
        if taluka_id is None and hasattr(obj, "taluka"):
            taluka_id = getattr(obj.taluka, "id", None)
        if user.taluka_id is None:
            return False
        return taluka_id == user.taluka_id
