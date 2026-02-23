from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ChangeRequest, ChangeRequestLog
from .permissions import IsAuthenticatedAndPrivilegedForMutations
from .serializers import ChangeRequestSerializer


class ChangeRequestViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ChangeRequestSerializer
    permission_classes = (IsAuthenticatedAndPrivilegedForMutations,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('status', 'system', 'ministry', 'change_category')

    def get_queryset(self):
        return (
            ChangeRequest.objects.select_related(
                'created_by',
                'system',
                'system__ministry',
                'ministry',
            )
            .prefetch_related('logs', 'logs__performed_by')
            .order_by('-created_at')
        )

    @transaction.atomic
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        return self._transition(request, self.get_object(), ChangeRequest.Status.APPROVED, ChangeRequestLog.Action.APPROVAL)

    @transaction.atomic
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        return self._transition(request, self.get_object(), ChangeRequest.Status.REJECTED, ChangeRequestLog.Action.REJECTION)

    @transaction.atomic
    @action(detail=True, methods=['post'])
    def implement(self, request, pk=None):
        return self._transition(
            request,
            self.get_object(),
            ChangeRequest.Status.IMPLEMENTING,
            ChangeRequestLog.Action.IMPLEMENTATION,
        )

    @transaction.atomic
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        return self._transition(
            request,
            self.get_object(),
            ChangeRequest.Status.COMPLETED,
            ChangeRequestLog.Action.COMPLETION,
        )

    def _transition(self, request, cr, target_status, action):
        if cr.status == ChangeRequest.Status.COMPLETED:
            return Response({'detail': 'Completed change requests are immutable.'}, status=status.HTTP_400_BAD_REQUEST)

        cr.status = target_status
        cr.save(update_fields=['status', 'updated_at'])
        ChangeRequestLog.objects.create(
            change_request=cr,
            action=action,
            performed_by=request.user,
        )
        return Response(self.get_serializer(cr).data, status=status.HTTP_200_OK)
