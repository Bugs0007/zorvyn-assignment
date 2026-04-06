from rest_framework.response import Response
from rest_framework.views import APIView

from config.permissions import DashboardAccessPermission

from .services import build_finance_summary


class DashboardSummaryAPIView(APIView):
    permission_classes = [DashboardAccessPermission]

    def get(self, request):
        return Response(build_finance_summary())
