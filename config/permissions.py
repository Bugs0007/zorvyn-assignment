from rest_framework.permissions import SAFE_METHODS, BasePermission


class RoleBasedAccessPermission(BasePermission):
    """
    ADMIN: full access
    ANALYST: read-only access
    VIEWER: read-only access
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.role == "ADMIN":
            return True

        if user.role in {"ANALYST", "VIEWER"}:
            return request.method in SAFE_METHODS

        return False


class DashboardAccessPermission(BasePermission):
    """
    ADMIN and ANALYST can access dashboard APIs.
    VIEWER cannot.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        return user.role in {"ADMIN", "ANALYST"}


class AdminOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        return user.role == "ADMIN"
