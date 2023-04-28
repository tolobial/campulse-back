"""Serializers describing fields used on projects."""
from rest_framework import serializers

from plana.apps.commissions.serializers.commission_date import CommissionDateSerializer
from plana.apps.projects.models.project import Project
from plana.apps.projects.serializers.category import CategorySerializer


class ProjectSerializer(serializers.ModelSerializer):
    """Main serializer."""

    other_first_name = serializers.CharField(required=False, allow_blank=True)
    other_last_name = serializers.CharField(required=False, allow_blank=True)
    other_email = serializers.CharField(required=False, allow_blank=True)
    other_phone = serializers.CharField(required=False, allow_blank=True)
    categories = CategorySerializer(many=True, read_only=True)
    commission_dates = CommissionDateSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "planned_start_date",
            "planned_end_date",
            "location",
            "other_first_name",
            "other_last_name",
            "other_email",
            "other_phone",
            "user",
            "association",
            "categories",
            "commission_dates",
            "budget_previous_edition",
            "target_audience",
            "amount_students_audience",
            "amount_all_audience",
            "ticket_price",
            "individual_cost",
            "goals",
            "summary",
            "planned_activities",
            "prevention_safety",
            "marketing_campaign",
            "project_status",
        ]


class ProjectUpdateSerializer(serializers.ModelSerializer):
    """Main serializer without project_status."""

    other_first_name = serializers.CharField(required=False, allow_blank=True)
    other_last_name = serializers.CharField(required=False, allow_blank=True)
    other_email = serializers.CharField(required=False, allow_blank=True)
    other_phone = serializers.CharField(required=False, allow_blank=True)
    categories = CategorySerializer(many=True, read_only=True)
    commission_dates = CommissionDateSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "planned_start_date",
            "planned_end_date",
            "location",
            "other_first_name",
            "other_last_name",
            "other_email",
            "other_phone",
            "user",
            "association",
            "categories",
            "commission_dates",
            "budget_previous_edition",
            "target_audience",
            "amount_students_audience",
            "amount_all_audience",
            "ticket_price",
            "individual_cost",
            "goals",
            "summary",
            "planned_activities",
            "prevention_safety",
            "marketing_campaign",
        ]


class ProjectPartialDataSerializer(serializers.ModelSerializer):
    """Serializer for project list."""

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "association",
            "user",
            "edition_date",
            "project_status",
        ]


class ProjectStatusSerializer(serializers.ModelSerializer):
    """Serializer for status field."""

    class Meta:
        model = Project
        fields = ["project_status"]
