"""Circles views"""

# Django rest framework
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
# Models
from cride.circles.models import Circle
from cride.circles.models import Membership
# Serializer
from cride.circles.serializers import CircleModelSerializer
# Permissions
from cride.circles.permissions.circles import IsCircleAdmin


class CirclesViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """Circle view set."""

    serializer_class = CircleModelSerializer
    lookup_field = 'slug_name'

    def get_permissions(self):
        """Assign permissions based on action"""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        return [permission() for permission in permissions]

    def get_queryset(self):
        """Restrict list to public-only"""
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset

    def perform_create(self, serializer):
        """Assign circle admin."""
        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10
        )