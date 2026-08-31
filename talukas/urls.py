from django.urls import include, path
from rest_framework.routers import DefaultRouter

from talukas.views import AdminDashboardView, TalukaDashboardView, TalukaViewSet

router = DefaultRouter()
router.register("talukas", TalukaViewSet, basename="taluka")

urlpatterns = [
    path("dashboard/admin/", AdminDashboardView.as_view(), name="dashboard-admin"),
    path("dashboard/taluka/", TalukaDashboardView.as_view(), name="dashboard-taluka"),
    path("", include(router.urls)),
]
