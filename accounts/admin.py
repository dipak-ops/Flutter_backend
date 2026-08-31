from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from accounts.models import Tahsildar, User

admin.site.site_header = "Nanded District Taluka Administration"
admin.site.site_title = "Nanded TMS Admin"
admin.site.index_title = "Backend administration"


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "taluka",
        "is_active",
        "last_login",
        "created_at",
    )
    list_filter = ("role", "taluka", "is_active")
    search_fields = ("username", "email", "first_name", "last_name", "phone")
    ordering = ("username",)
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Taluka profile", {"fields": ("phone", "role", "taluka")}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("Taluka profile", {"fields": ("phone", "role", "taluka", "email")}),
    )


@admin.register(Tahsildar)
class TahsildarAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(role=User.Role.TAHSILDAR)
