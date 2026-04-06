from django.contrib import admin

from .models import FinancialRecord


@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display = ("title", "record_type", "category", "amount", "entry_date", "created_by")
    list_filter = ("record_type", "category", "entry_date")
    search_fields = ("title", "category", "description")
