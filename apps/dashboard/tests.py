from decimal import Decimal

from django.urls import reverse
from rest_framework import status

from apps.records.models import FinancialRecord
from apps.test_base import BaseAPITestCase


class DashboardAPITestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("dashboard-summary")

    def test_dashboard_returns_correct_aggregations(self):
        FinancialRecord.objects.create(
            title="Bonus",
            description="Quarterly bonus",
            record_type=FinancialRecord.RecordType.INCOME,
            category="Salary",
            amount=Decimal("800.00"),
            entry_date="2026-04-05",
            created_by=self.admin,
        )

        response = self.admin_client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data["total_income"]), Decimal("5800.00"))
        self.assertEqual(Decimal(response.data["total_expense"]), Decimal("1200.00"))
        self.assertEqual(Decimal(response.data["net_balance"]), Decimal("4600.00"))
        self.assertEqual(
            Decimal(response.data["category_wise_totals"]["Salary"]),
            Decimal("5800.00"),
        )
        self.assertEqual(
            Decimal(response.data["category_wise_totals"]["Rent"]),
            Decimal("1200.00"),
        )

    def test_dashboard_accessible_by_admin(self):
        response = self.admin_client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dashboard_accessible_by_analyst(self):
        response = self.analyst_client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dashboard_restricted_for_viewer(self):
        response = self.viewer_client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_dashboard_blocks_unauthenticated_requests(self):
        response = self.unauthenticated_client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
