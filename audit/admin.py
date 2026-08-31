from django.contrib import admin

from audit.models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "action", "user", "taluka", "target_type", "target_id", "ip_address")
    list_filter = ("action", "taluka")
    search_fields = ("action", "target_type", "target_id", "user__username")
    ordering = ("-timestamp",)
    readonly_fields = (
        "user",
        "action",
        "target_type",
        "target_id",
        "taluka",
        "ip_address",
        "timestamp",
        "metadata",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
