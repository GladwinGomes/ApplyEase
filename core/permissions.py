"""
Custom DRF permissions for ApplyEase.
"""

from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Allows access only to users with the 'admin' role.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'role', None) == 'admin'
        )


class IsApplicant(BasePermission):
    """
    Allows access only to users with the 'applicant' role.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'role', None) == 'applicant'
        )
