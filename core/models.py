from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
        APPROVER = 'APPROVER', 'Approver'
        SUBMITTER = 'SUBMITTER', 'Submitter'

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.SUBMITTER)


class Ministry(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class System(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owning_ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE, related_name='systems')
    is_smart_zambia_owned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Functionality(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='functionalities')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ChangeRequest(models.Model):
    class ChangeCategory(models.TextChoices):
        MAJOR = 'MAJOR', 'Major'
        MINOR = 'MINOR', 'Minor'

    class Status(models.TextChoices):
        SUBMITTED = 'SUBMITTED', 'Submitted'

    title = models.CharField(max_length=255)
    description = models.TextField()
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='change_requests')
    functionality = models.ForeignKey(
        Functionality,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='change_requests',
    )
    change_category = models.CharField(max_length=10, choices=ChangeCategory.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submitted_change_requests',
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_change_requests',
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    implemented_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
