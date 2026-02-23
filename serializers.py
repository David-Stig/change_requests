from rest_framework import serializers

from .models import ChangeRequest


class ChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeRequest
        fields = [
            "id",
            "title",
            "description",
            "change_category",
            "status",
            "approved_at",
            "rejected_at",
            "implemented_at",
            "completed_at",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "status",
            "approved_at",
            "rejected_at",
            "implemented_at",
            "completed_at",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        instance = getattr(self, "instance", None)
        if instance and instance.status in {
            ChangeRequest.Status.REJECTED,
            ChangeRequest.Status.COMPLETED,
        }:
            raise serializers.ValidationError(
                f"Cannot modify a change request in {instance.status} status."
            )
        return attrs
