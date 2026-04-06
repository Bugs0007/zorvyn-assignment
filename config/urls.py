from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.dashboard.views import DashboardSummaryAPIView
from apps.records.views import FinancialRecordViewSet
from apps.users.views import LoginAPIView, UserViewSet


router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("records", FinancialRecordViewSet, basename="record")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/dashboard/", DashboardSummaryAPIView.as_view(), name="dashboard-summary"),
    path("api/users/login/", LoginAPIView.as_view(), name="login"),
    path("api/", include(router.urls)),
]
