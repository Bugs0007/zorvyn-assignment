from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from config.permissions import RoleBasedAccessPermission

from .models import FinancialRecord
from .serializers import FinancialRecordSerializer


class FinancialRecordViewSet(viewsets.ModelViewSet):
    queryset = FinancialRecord.objects.select_related("created_by").all()
    serializer_class = FinancialRecordSerializer
    permission_classes = [RoleBasedAccessPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "record_type": ["exact"],
        "category": ["exact", "icontains"],
        "entry_date": ["exact", "gte", "lte"],
    }

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
