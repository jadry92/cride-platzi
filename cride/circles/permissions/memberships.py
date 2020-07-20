"""Permissions Memberships"""

# Django Rest framework
from rest_framework.permissions import BasePermission
# Model
from cride.circles.models import Membership


class IsActiveCircleMember(BasePermission):
    """
    Allow access only to circle members active.

    :except that the views implementing this permission
    have a `circle` attribute assigned.

    """

    def has_permission(self, request, view):
        """Verify user is an active member of the circle"""
        try:
            Membership.objects.get(
                user=request.user,
                circle=view.circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True


class IsSelfMember(BasePermission):
    """
    Allow access only to members owners.
    """

    def has_permission(self, request, view):
        """Check if the user is a member of the circle"""

        obj = view.get_object()
        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj):
        """Allow access only if member is owned bt the  requesting user."""
        return request.user == obj.user
