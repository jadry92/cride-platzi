"""Membership serializer"""

# Django
from django.utils import timezone
# Django REST framework
from rest_framework import serializers
# Serializers
from cride.users.serializers import UserModelSerializer
# Models
from cride.circles.models import Membership, Invitation


class MembershipModelSerializer(serializers.ModelSerializer):
    """Member model serializer"""

    user = UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField()
    joined_at = serializers.DateTimeField(source='created', read_only=True)

    class Meta:
        """Meta Class"""

        model = Membership
        fields = (
            'user',
            'is_admin', 'is_active',
            'used_invitations', 'remaining_invitations',
            'invited_by',
            'rides_taken', 'rides_offered',
            'joined_at'
        )
        read_only_fields = (
            'user',
            'used_invitations',
            'invited_by',
            'rides_taken', 'rides_offered'
        )


class AddMemberSerializer(serializers.Serializer):
    """Add member serializer.

    Handel the addition of a new member to a circle.
    Circle object must be provided in the context.
    """

    invitation_code = serializers.CharField(min_length=10)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_user(self, attrs):
        """Verify use in not already member"""
        circle = self.context['circle']
        user = attrs
        mem = Membership.objects.filter(circle=circle, user=user)
        if mem.exists():
            raise serializers.ValidationError('User is already member of this circle')

    def validate_invitation_code(self, attrs):
        """Verify code exist and that it is related to the circle"""
        try:
            invitation = Invitation.objects.get(
                code=attrs,
                circle=self.context['circle'],
                used=False
            )
        except Invitation.DoesNotExist:
            raise serializers.ValidationError('Invalid invitation code.')
        self.context['invitation'] = invitation
        return attrs

    def validate(self, attrs):
        """Verify circle is capable of accepting a new member."""
        circle = self.context['circle']
        if circle.is_limited and circle.members.count() >= circle.members_limit:
            raise serializers.ValidationError('Circle {} has reached its member limit :/'.format(circle.slug_name))
        return attrs

    def create(self, validated_data):
        """Create new circle member."""
        circle = self.context['circle']
        invitation = self.context['invitation']
        if not validated_data['user']:
            user = self.context['request'].user
            validated_data['user'] = user
        else:
            user = validated_data['user']

        now = timezone.now()

        # Member creation
        member = Membership.objects.create(
            user=user,
            profile=user.profile,
            circle=circle,
            invited_by=invitation.issued_by
        )

        # Update Invitation
        invitation.used_by = user
        invitation.used = True
        invitation.used_at = now
        invitation.save()

        # Update issuer data
        issuer = Membership.objects.get(user=invitation.issued_by, circle=circle)
        issuer.used_invitations += 1
        issuer.remaining_invitations += 1
        issuer.save()

        return validated_data
