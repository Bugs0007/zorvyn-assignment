from django.utils import timezone
from rest_framework import serializers

from .models import FinancialRecord


class FinancialRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRecord
        fields = "__all__"
        read_only_fields = ("created_by", "created_at", "updated_at")

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Title cannot be blank.")
        return value

    def validate_category(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Category cannot be blank.")
        return value

    def validate_description(self, value):
        return value.strip()

    def validate_entry_date(self, value):
        if value > timezone.localdate():
            raise serializers.ValidationError("Entry date cannot be in the future.")
        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)

        instance = getattr(self, "instance", None)
        candidate = {
            "title": attrs.get("title", getattr(instance, "title", None)),
            "description": attrs.get("description", getattr(instance, "description", "")),
            "record_type": attrs.get("record_type", getattr(instance, "record_type", None)),
            "category": attrs.get("category", getattr(instance, "category", None)),
            "amount": attrs.get("amount", getattr(instance, "amount", None)),
            "entry_date": attrs.get("entry_date", getattr(instance, "entry_date", None)),
        }

        duplicate_qs = FinancialRecord.objects.filter(**candidate)
        if instance is not None:
            duplicate_qs = duplicate_qs.exclude(pk=instance.pk)

        if duplicate_qs.exists():
            raise serializers.ValidationError(
                "An identical financial record already exists. Exact duplicate entries are not allowed.",
            )

        return attrs
