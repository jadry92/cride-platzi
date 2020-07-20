"""Rides permissions"""

# Django REST framework
from rest_framework.permissions import BasePermission


class IsRideOwner(BasePermission):
    """Verify the ride's ownership"""

    def has_object_permission(self, request, view, obj):
        """check request user equal to object"""
        return request.user == obj.offered_by


class IsNotRideOwner(BasePermission):
    """Verify the passenger is not owner of ride"""

    def has_object_permission(self, request, view, obj):
        """check request user doesn't equal to object"""
        return request.user != obj.offered_by
