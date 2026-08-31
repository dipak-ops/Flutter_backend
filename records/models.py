from django.conf import settings
from django.db import models
from django.utils import timezone


class Record(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
        DEACTIVATED = "DEACTIVATED", "Deactivated"

    taluka = models.ForeignKey(
        "talukas.Taluka",
        on_delete=models.PROTECT,
        related_name="records",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_records",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="updated_records",
        null=True,
        blank=True,
    )
    record_number = models.CharField(max_length=32, unique=True, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
    )
    is_active = models.BooleanField(default=True, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["taluka__code", "record_number"]
        indexes = [
            models.Index(fields=["taluka", "is_active"]),
            models.Index(fields=["taluka", "status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.record_number} - {self.title}"

    def deactivate(self, user=None):
        self.is_active = False
        self.status = self.Status.DEACTIVATED
        self.deleted_at = timezone.now()
        if user:
            self.updated_by = user
        self.save()

    def activate(self, user=None):
        self.is_active = True
        self.status = self.Status.ACTIVE
        self.deleted_at = None
        if user:
            self.updated_by = user
        self.save()


def next_record_number(taluka):
    prefix = taluka.code
    last = (
        Record.objects.filter(record_number__startswith=f"{prefix}-")
        .order_by("-record_number")
        .values_list("record_number", flat=True)
        .first()
    )
    if last:
        try:
            seq = int(last.split("-")[-1]) + 1
        except ValueError:
            seq = Record.objects.filter(taluka=taluka).count() + 1
    else:
        seq = 1
    while Record.objects.filter(record_number=f"{prefix}-{seq:03d}").exists():
        seq += 1
    return f"{prefix}-{seq:03d}"
