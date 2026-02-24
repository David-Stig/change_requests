from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedAndPrivilegedForMutations(BasePermission):
    message = 'Only users in approver or implementer groups may perform state transitions.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser or request.user.groups.filter(
            name__in=['approver', 'implementer']
        ).exists()
