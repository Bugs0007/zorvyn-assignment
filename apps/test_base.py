from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

from apps.records.models import FinancialRecord


class BaseAPITestCase(APITestCase):
    def setUp(self):
        user_model = get_user_model()

        self.admin = user_model.objects.create_user(
            username="admin",
            password="admin123",
            role=user_model.Role.ADMIN,
            is_staff=True,
            is_superuser=True,
        )
        self.analyst = user_model.objects.create_user(
            username="analyst",
            password="analyst123",
            role=user_model.Role.ANALYST,
        )
        self.viewer = user_model.objects.create_user(
            username="viewer",
            password="viewer123",
            role=user_model.Role.VIEWER,
        )

        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin)

        self.analyst_client = APIClient()
        self.analyst_client.force_authenticate(user=self.analyst)

        self.viewer_client = APIClient()
        self.viewer_client.force_authenticate(user=self.viewer)

        self.unauthenticated_client = APIClient()

        self.income_record = FinancialRecord.objects.create(
            title="Salary",
            description="Monthly income",
            record_type=FinancialRecord.RecordType.INCOME,
            category="Salary",
            amount=Decimal("5000.00"),
            entry_date=date(2026, 4, 1),
            created_by=self.admin,
        )
        self.expense_record = FinancialRecord.objects.create(
            title="Rent",
            description="Office rent",
            record_type=FinancialRecord.RecordType.EXPENSE,
            category="Rent",
            amount=Decimal("1200.00"),
            entry_date=date(2026, 4, 2),
            created_by=self.admin,
        )
