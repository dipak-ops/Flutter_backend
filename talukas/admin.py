from django.contrib import admin

from talukas.models import Taluka


@admin.register(Taluka)
class TalukaAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "code")
    ordering = ("name",)
