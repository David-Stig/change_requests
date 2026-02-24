from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import User


class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == User.Roles.SUPER_ADMIN:
            return True

        if request.user.role == User.Roles.APPROVER:
            return request.method in SAFE_METHODS

        if request.user.role == User.Roles.SUBMITTER:
            if view.basename == 'change-request':
                return request.method in SAFE_METHODS or request.method == 'POST'
            return request.method in SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == User.Roles.SUPER_ADMIN:
            return True

        if request.user.role == User.Roles.APPROVER:
            return view.basename == 'change-request' and request.method in SAFE_METHODS

        if request.user.role == User.Roles.SUBMITTER:
            if view.basename == 'change-request':
                if request.method in SAFE_METHODS:
                    return obj.submitted_by_id == request.user.id
                return False
            return request.method in SAFE_METHODS

        return False
