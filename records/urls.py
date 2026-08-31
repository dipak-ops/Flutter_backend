from django.urls import include, path
from rest_framework.routers import DefaultRouter

from records.views import RecordViewSet

router = DefaultRouter()
router.register("records", RecordViewSet, basename="record")

urlpatterns = [
    path("", include(router.urls)),
]
