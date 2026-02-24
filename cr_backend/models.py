from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    group = models.OneToOneField(Group, on_delete=models.PROTECT, related_name='role')

    def __str__(self) -> str:
        return self.name


class Ministry(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name


class System(models.Model):
    name = models.CharField(max_length=200, unique=True)
    ministry = models.ForeignKey(Ministry, on_delete=models.PROTECT, related_name='systems')
    owners = models.ManyToManyField(User, blank=True, related_name='owned_systems')

    def __str__(self) -> str:
        return self.name


class ChangeRequest(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        IMPLEMENTING = 'implementing', 'Implementing'
        COMPLETED = 'completed', 'Completed'

    class Category(models.TextChoices):
        BUGFIX = 'bugfix', 'Bugfix'
        FEATURE = 'feature', 'Feature'
        SECURITY = 'security', 'Security'
        MAINTENANCE = 'maintenance', 'Maintenance'

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='change_requests')
    system = models.ForeignKey(System, on_delete=models.PROTECT, related_name='change_requests')
    ministry = models.ForeignKey(Ministry, on_delete=models.PROTECT, related_name='change_requests')
    change_category = models.CharField(max_length=32, choices=Category.choices)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self) -> None:
        if self.system_id and self.ministry_id and self.system.ministry_id != self.ministry_id:
            raise ValidationError({'system': 'System must belong to the selected ministry.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.title} ({self.status})'


class ChangeRequestLog(models.Model):
    class Action(models.TextChoices):
        APPROVAL = 'approval', 'Approval'
        REJECTION = 'rejection', 'Rejection'
        IMPLEMENTATION = 'implementation', 'Implementation'
        COMPLETION = 'completion', 'Completion'

    change_request = models.ForeignKey(ChangeRequest, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=32, choices=Action.choices)
    performed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='change_request_actions')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self) -> str:
        return f'{self.change_request_id}:{self.action} by {self.performed_by_id}'
