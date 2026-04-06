from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import LoginAPIView, UserViewSet


router = DefaultRouter()
router.register("", UserViewSet, basename="user")

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    *router.urls,
]
