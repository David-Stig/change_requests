from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from .models import ChangeRequest
from .serializers import ChangeRequestSerializer


class ChangeRequestViewSet(viewsets.ModelViewSet):
    queryset = ChangeRequest.objects.all()
    serializer_class = ChangeRequestSerializer

    def _is_approver_or_super_admin(self, user) -> bool:
        role = getattr(user, "role", None)
        if role in {"APPROVER", "SUPER_ADMIN"}:
            return True
        if getattr(user, "is_superuser", False):
            return True
        if hasattr(user, "groups"):
            return user.groups.filter(name__in=["APPROVER", "SUPER_ADMIN"]).exists()
        return False

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        change_category = serializer.validated_data.get("change_category")
        now = timezone.now()
        if change_category == ChangeRequest.ChangeCategory.MINOR:
            status_value = ChangeRequest.Status.APPROVED
            approved_at = now
        else:
            status_value = ChangeRequest.Status.SUBMITTED
            approved_at = None

        instance = serializer.save(
            created_by=request.user if request.user and request.user.is_authenticated else None,
            status=status_value,
            approved_at=approved_at,
        )

        output = self.get_serializer(instance)
        headers = self.get_success_headers(output.data)
        return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)

    def _run_transition(self, instance: ChangeRequest, new_status: str):
        try:
            instance.transition_to(new_status)
            instance.save(update_fields=[
                "status",
                "approved_at",
                "rejected_at",
                "implemented_at",
                "completed_at",
                "updated_at",
            ])
        except DjangoValidationError as exc:
            raise ValidationError(exc.message)

    @action(detail=True, methods=["patch"])
    def approve(self, request, pk=None):
        if not self._is_approver_or_super_admin(request.user):
            raise PermissionDenied("Only APPROVER or SUPER_ADMIN can approve requests.")

        instance = self.get_object()
        self._run_transition(instance, ChangeRequest.Status.APPROVED)
        return Response(self.get_serializer(instance).data)

    @action(detail=True, methods=["patch"])
    def reject(self, request, pk=None):
        if not self._is_approver_or_super_admin(request.user):
            raise PermissionDenied("Only APPROVER or SUPER_ADMIN can reject requests.")

        instance = self.get_object()
        self._run_transition(instance, ChangeRequest.Status.REJECTED)
        return Response(self.get_serializer(instance).data)

    @action(detail=True, methods=["patch"])
    def implement(self, request, pk=None):
        instance = self.get_object()
        self._run_transition(instance, ChangeRequest.Status.IMPLEMENTED)
        return Response(self.get_serializer(instance).data)

    @action(detail=True, methods=["patch"])
    def complete(self, request, pk=None):
        instance = self.get_object()
        self._run_transition(instance, ChangeRequest.Status.COMPLETED)
        return Response(self.get_serializer(instance).data)
