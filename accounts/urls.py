from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.views import TahsildarViewSet, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("tahsildars", TahsildarViewSet, basename="tahsildar")

urlpatterns = [
    path("", include(router.urls)),
]
