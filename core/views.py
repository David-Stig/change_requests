from rest_framework import viewsets

from .models import ChangeRequest, Functionality, Ministry, System, User
from .permissions import RoleBasedPermission
from .serializers import (
    ChangeRequestSerializer,
    FunctionalitySerializer,
    MinistrySerializer,
    SystemSerializer,
    UserSerializer,
)


class MinistryViewSet(viewsets.ModelViewSet):
    queryset = Ministry.objects.all().order_by('-created_at')
    serializer_class = MinistrySerializer
    permission_classes = [RoleBasedPermission]


class SystemViewSet(viewsets.ModelViewSet):
    queryset = System.objects.all().order_by('-created_at')
    serializer_class = SystemSerializer
    permission_classes = [RoleBasedPermission]


class FunctionalityViewSet(viewsets.ModelViewSet):
    queryset = Functionality.objects.all().order_by('-id')
    serializer_class = FunctionalitySerializer
    permission_classes = [RoleBasedPermission]


class ChangeRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ChangeRequestSerializer
    permission_classes = [RoleBasedPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = ChangeRequest.objects.select_related('system', 'functionality', 'submitted_by', 'approved_by')

        if user.role in (User.Roles.SUPER_ADMIN, User.Roles.APPROVER):
            return queryset.order_by('-created_at')

        if user.role == User.Roles.SUBMITTER:
            return queryset.filter(submitted_by=user).order_by('-created_at')

        return queryset.none()

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [RoleBasedPermission]
