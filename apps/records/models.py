from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class FinancialRecord(models.Model):
    class RecordType(models.TextChoices):
        INCOME = "INCOME", "Income"
        EXPENSE = "EXPENSE", "Expense"
        ASSET = "ASSET", "Asset"
        LIABILITY = "LIABILITY", "Liability"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    record_type = models.CharField(max_length=20, choices=RecordType.choices)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    entry_date = models.DateField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="financial_records",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-entry_date", "-created_at"]

    def __str__(self) -> str:
        return f"{self.title} - {self.amount}"
