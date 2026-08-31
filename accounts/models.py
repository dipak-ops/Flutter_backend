from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q


class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
        TAHSILDAR = "TAHSILDAR", "Tahsildar"
        TALUKA_USER = "TALUKA_USER", "Taluka User"

    phone = models.CharField(max_length=15, blank=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.TALUKA_USER,
        db_index=True,
    )
    taluka = models.ForeignKey(
        "talukas.Taluka",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="users",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["username"]
        indexes = [
            models.Index(fields=["taluka", "role"]),
            models.Index(fields=["role", "is_active"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["created_at"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["taluka"],
                condition=Q(role="TAHSILDAR", is_active=True),
                name="unique_active_tahsildar_per_taluka",
            ),
            models.CheckConstraint(
                check=(
                    Q(role="SUPER_ADMIN", taluka__isnull=True)
                    | Q(role__in=["TAHSILDAR", "TALUKA_USER"], taluka__isnull=False)
                ),
                name="super_admin_no_taluka_others_require_taluka",
            ),
        ]

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_super_admin(self):
        return self.role == self.Role.SUPER_ADMIN

    @property
    def is_tahsildar(self):
        return self.role == self.Role.TAHSILDAR

    @property
    def is_taluka_user(self):
        return self.role == self.Role.TALUKA_USER


class Tahsildar(User):
    class Meta:
        proxy = True
        verbose_name = "Tahsildar"
        verbose_name_plural = "Tahsildars"
