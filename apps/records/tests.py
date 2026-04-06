from datetime import date
from decimal import Decimal

from django.urls import reverse
from rest_framework import status

from apps.records.models import FinancialRecord
from apps.test_base import BaseAPITestCase


class RecordAPITestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("record-list")
        self.detail_url = reverse("record-detail", args=[self.income_record.id])

    def test_admin_can_create_record(self):
        payload = {
            "title": "Consulting",
            "description": "Project payment",
            "record_type": FinancialRecord.RecordType.INCOME,
            "category": "Services",
            "amount": "2500.00",
            "entry_date": "2026-04-03",
        }

        response = self.admin_client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FinancialRecord.objects.count(), 3)

    def test_admin_can_update_record(self):
        payload = {
            "title": self.income_record.title,
            "description": self.income_record.description,
            "record_type": self.income_record.record_type,
            "category": "Updated Salary",
            "amount": str(self.income_record.amount),
            "entry_date": str(self.income_record.entry_date),
        }

        response = self.admin_client.put(self.detail_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.income_record.refresh_from_db()
        self.assertEqual(self.income_record.category, "Updated Salary")

    def test_admin_can_delete_record(self):
        response = self.admin_client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FinancialRecord.objects.filter(id=self.income_record.id).exists())

    def test_analyst_can_list_records(self):
        response = self.analyst_client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_analyst_cannot_create_record(self):
        payload = {
            "title": "Blocked",
            "description": "Should not be created",
            "record_type": FinancialRecord.RecordType.INCOME,
            "category": "Services",
            "amount": "100.00",
            "entry_date": "2026-04-03",
        }

        response = self.analyst_client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_viewer_can_list_records(self):
        response = self.viewer_client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_viewer_cannot_modify_record(self):
        response = self.viewer_client.patch(
            self.detail_url,
            {"category": "Blocked"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filtering_by_type_category_and_date_works(self):
        FinancialRecord.objects.create(
            title="Freelance",
            description="Extra income",
            record_type=FinancialRecord.RecordType.INCOME,
            category="Consulting",
            amount=Decimal("900.00"),
            entry_date=date(2026, 4, 10),
            created_by=self.admin,
        )

        response = self.admin_client.get(
            self.list_url,
            {
                "record_type": FinancialRecord.RecordType.INCOME,
                "category__icontains": "consult",
                "entry_date__gte": "2026-04-05",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Freelance")

    def test_negative_amount_fails(self):
        payload = {
            "title": "Invalid",
            "description": "Negative amount",
            "record_type": FinancialRecord.RecordType.EXPENSE,
            "category": "Error",
            "amount": "-50.00",
            "entry_date": "2026-04-03",
        }

        response = self.admin_client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("amount", response.data)

    def test_missing_required_fields_fail(self):
        payload = {
            "description": "Missing required fields",
            "amount": "100.00",
        }

        response = self.admin_client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
        self.assertIn("record_type", response.data)
        self.assertIn("category", response.data)
        self.assertIn("entry_date", response.data)

    def test_blank_title_and_category_fail(self):
        payload = {
            "title": "   ",
            "description": "Whitespace only",
            "record_type": FinancialRecord.RecordType.EXPENSE,
            "category": "   ",
            "amount": "100.00",
            "entry_date": "2026-04-03",
        }

        response = self.admin_client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
        self.assertIn("category", response.data)

    def test_future_entry_date_fails(self):
        payload = {
            "title": "Planned Expense",
            "description": "Future dated",
            "record_type": FinancialRecord.RecordType.EXPENSE,
            "category": "Planning",
            "amount": "100.00",
            "entry_date": "2099-01-01",
        }

        response = self.admin_client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("entry_date", response.data)

    def test_exact_duplicate_record_fails_on_create(self):
        payload = {
            "title": self.income_record.title,
            "description": self.income_record.description,
            "record_type": self.income_record.record_type,
            "category": self.income_record.category,
            "amount": str(self.income_record.amount),
            "entry_date": str(self.income_record.entry_date),
        }

        response = self.admin_client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_exact_duplicate_record_fails_on_update(self):
        other_record = FinancialRecord.objects.create(
            title="Freelance",
            description="Extra income",
            record_type=FinancialRecord.RecordType.INCOME,
            category="Consulting",
            amount=Decimal("900.00"),
            entry_date=date(2026, 4, 10),
            created_by=self.admin,
        )

        response = self.admin_client.patch(
            reverse("record-detail", args=[other_record.id]),
            {
                "title": self.income_record.title,
                "description": self.income_record.description,
                "record_type": self.income_record.record_type,
                "category": self.income_record.category,
                "amount": str(self.income_record.amount),
                "entry_date": str(self.income_record.entry_date),
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_unauthenticated_requests_are_blocked(self):
        response = self.unauthenticated_client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
