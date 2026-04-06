from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.records.models import FinancialRecord


class Command(BaseCommand):
    help = "Create sample users and financial records for local development."

    def handle(self, *args, **options):
        user_model = get_user_model()

        admin_user, _ = user_model.objects.update_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "first_name": "Admin",
                "last_name": "User",
                "role": user_model.Role.ADMIN,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin_user.set_password("admin123")
        admin_user.save()

        analyst_user, _ = user_model.objects.update_or_create(
            username="analyst",
            defaults={
                "email": "analyst@example.com",
                "first_name": "Analyst",
                "last_name": "User",
                "role": user_model.Role.ANALYST,
            },
        )
        analyst_user.set_password("analyst123")
        analyst_user.save()

        viewer_user, _ = user_model.objects.update_or_create(
            username="viewer",
            defaults={
                "email": "viewer@example.com",
                "first_name": "Viewer",
                "last_name": "User",
                "role": user_model.Role.VIEWER,
            },
        )
        viewer_user.set_password("viewer123")
        viewer_user.save()

        sample_records = [
            {
                "title": "Client Retainer",
                "description": "Monthly consulting revenue",
                "record_type": FinancialRecord.RecordType.INCOME,
                "category": "Consulting",
                "amount": Decimal("5000.00"),
                "entry_date": date.today() - timedelta(days=12),
                "created_by": admin_user,
            },
            {
                "title": "Software Subscription",
                "description": "Accounting tool subscription",
                "record_type": FinancialRecord.RecordType.EXPENSE,
                "category": "Software",
                "amount": Decimal("199.00"),
                "entry_date": date.today() - timedelta(days=10),
                "created_by": analyst_user,
            },
            {
                "title": "Product Sales",
                "description": "Online sales income",
                "record_type": FinancialRecord.RecordType.INCOME,
                "category": "Sales",
                "amount": Decimal("3200.00"),
                "entry_date": date.today() - timedelta(days=7),
                "created_by": admin_user,
            },
            {
                "title": "Office Rent",
                "description": "Monthly office rent expense",
                "record_type": FinancialRecord.RecordType.EXPENSE,
                "category": "Rent",
                "amount": Decimal("1200.00"),
                "entry_date": date.today() - timedelta(days=5),
                "created_by": analyst_user,
            },
            {
                "title": "Internet Bill",
                "description": "Office internet and phone",
                "record_type": FinancialRecord.RecordType.EXPENSE,
                "category": "Utilities",
                "amount": Decimal("150.00"),
                "entry_date": date.today() - timedelta(days=2),
                "created_by": viewer_user,
            },
        ]

        for record in sample_records:
            FinancialRecord.objects.update_or_create(
                title=record["title"],
                entry_date=record["entry_date"],
                defaults=record,
            )

        self.stdout.write(self.style.SUCCESS("Sample users and financial records created."))
