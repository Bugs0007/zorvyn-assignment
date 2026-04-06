from decimal import Decimal

from django.db.models import Sum

from apps.records.models import FinancialRecord


def build_finance_summary() -> dict:
    totals_by_type = {
        item["record_type"]: item["total_amount"] or Decimal("0.00")
        for item in FinancialRecord.objects.values("record_type").annotate(
            total_amount=Sum("amount"),
        )
    }

    total_income = totals_by_type.get(FinancialRecord.RecordType.INCOME, Decimal("0.00"))
    total_expense = totals_by_type.get(FinancialRecord.RecordType.EXPENSE, Decimal("0.00"))
    category_totals = {
        item["category"]: item["total_amount"] or Decimal("0.00")
        for item in FinancialRecord.objects.values("category").annotate(
            total_amount=Sum("amount"),
        )
    }

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense,
        "category_wise_totals": category_totals,
    }
