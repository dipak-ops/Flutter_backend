from django.db.models import Count
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.permissions import IsSuperAdmin
from records.models import Record
from talukas.models import Taluka
from talukas.serializers import TalukaSerializer


def scoped_talukas(user):
    qs = Taluka.objects.all().annotate(
        user_count=Count("users", distinct=True),
        record_count=Count("records", distinct=True),
    )
    if user.is_super_admin:
        return qs
    if user.taluka_id:
        return qs.filter(pk=user.taluka_id)
    return qs.none()


class TalukaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TalukaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return scoped_talukas(self.request.user)


class AdminDashboardView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        return Response(
            {
                "total_talukas": Taluka.objects.count(),
                "total_tahsildars": User.objects.filter(role=User.Role.TAHSILDAR).count(),
                "total_users": User.objects.filter(role=User.Role.TALUKA_USER).count(),
                "total_records": Record.objects.count(),
                "active_users": User.objects.filter(
                    role=User.Role.TALUKA_USER, is_active=True
                ).count(),
                "inactive_users": User.objects.filter(
                    role=User.Role.TALUKA_USER, is_active=False
                ).count(),
            }
        )


class TalukaDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_super_admin:
            return Response(
                {
                    "detail": "Use /api/dashboard/admin/ for district-wide statistics.",
                    "taluka": None,
                },
                status=400,
            )
        if not user.taluka:
            return Response({"detail": "No Taluka assigned."}, status=403)
        taluka = user.taluka
        users = User.objects.filter(taluka=taluka, role=User.Role.TALUKA_USER)
        records = Record.objects.filter(taluka=taluka)
        return Response(
            {
                "taluka": taluka.name,
                "taluka_code": taluka.code,
                "total_users": users.count(),
                "total_records": records.count(),
                "active_users": users.filter(is_active=True).count(),
                "inactive_users": users.filter(is_active=False).count(),
            }
        )
