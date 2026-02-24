from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class ChangeRequest(models.Model):
    class ChangeCategory(models.TextChoices):
        MINOR = "MINOR", "Minor"
        MAJOR = "MAJOR", "Major"

    class Status(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Submitted"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        IMPLEMENTED = "IMPLEMENTED", "Implemented"
        COMPLETED = "COMPLETED", "Completed"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    change_category = models.CharField(
        max_length=16,
        choices=ChangeCategory.choices,
        default=ChangeCategory.MAJOR,
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.SUBMITTED,
    )

    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    implemented_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="change_requests",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _ensure_mutable(self):
        if self.status in {self.Status.REJECTED, self.Status.COMPLETED}:
            raise ValidationError(
                f"Cannot modify a change request in {self.status} status."
            )

    def transition_to(self, new_status: str) -> None:
        self._ensure_mutable()

        if new_status == self.Status.APPROVED:
            if self.status != self.Status.SUBMITTED:
                raise ValidationError("Only submitted change requests can be approved.")
            self.status = self.Status.APPROVED
            self.approved_at = timezone.now()
            return

        if new_status == self.Status.REJECTED:
            if self.status != self.Status.SUBMITTED:
                raise ValidationError("Only submitted change requests can be rejected.")
            self.status = self.Status.REJECTED
            self.rejected_at = timezone.now()
            return

        if new_status == self.Status.IMPLEMENTED:
            if self.status != self.Status.APPROVED:
                raise ValidationError("Only approved change requests can be implemented.")
            self.status = self.Status.IMPLEMENTED
            self.implemented_at = timezone.now()
            return

        if new_status == self.Status.COMPLETED:
            if self.status != self.Status.IMPLEMENTED:
                raise ValidationError("Only implemented change requests can be completed.")
            self.status = self.Status.COMPLETED
            self.completed_at = timezone.now()
            return

        raise ValidationError(f"Unsupported status transition to {new_status}.")
