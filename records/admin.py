from django.contrib import admin

from records.models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        "record_number",
        "title",
        "taluka",
        "status",
        "is_active",
        "created_by",
        "created_at",
    )
    list_filter = ("taluka", "status", "is_active")
    search_fields = ("record_number", "title", "description")
    ordering = ("record_number",)
    raw_id_fields = ("created_by", "updated_by")
