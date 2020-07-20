"""Rides Serializers"""

# django REST framework
from rest_framework import serializers
# Models
from cride.rides.models import Ride
from cride.circles.models import Membership
from cride.users.models import User
# Serializers
from cride.users.serializers import UserModelSerializer
# Utilities
from datetime import timedelta
from django.utils import timezone


class RideModelSerializer(serializers.ModelSerializer):
    """Ride model Serializer"""

    offered_by = UserModelSerializer(read_only=True)
    offered_in = serializers.StringRelatedField()
    passengers = UserModelSerializer(read_only=True, many=True)

    class Meta:
        """Meta class"""

        model = Ride
        fields = '__all__'
        read_only_fields = (
            'offered_by',
            'offered_in',
            'rating'
        )

    def update(self, instance, validated_data):
        """Allow updates only before departure date."""
        now = timezone.now()
        if instance.departure_date <= now:
            raise serializers.ValidationError('Ongoing rides cannot be modified')
        return super(RideModelSerializer, self).update(instance, validated_data)


class CreateRideSerializer(serializers.ModelSerializer):
    """Create ride serializer"""

    offered_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    available_seats = serializers.IntegerField(min_value=1, max_value=15)

    class Meta:
        """Meta class"""

        model = Ride
        exclude = ('offered_in', 'passengers', 'rating', 'is_active')

    def validate_departure_date(self, attrs):
        """Verify date is not in the past."""
        min_date = timezone.now() + timedelta(minutes=20)

        if attrs < min_date:
            raise serializers.ValidationError(
                'departure time mut be at least pass the next 20 minutes window'
            )

        return attrs

    def validate(self, attrs):
        """Validate

        Verify that the person who offers the ride is member
        and also the same user making the request.
        """
        if self.context['request'].user != attrs['offered_by']:
            raise serializers.ValidationError('Rides offered on behalf of others are not allowed.')

        user = attrs['offered_by']
        circle = self.context['circle']
        try:
            membership = Membership.objects.get(
                user=user,
                circle=circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the circle.')

        if attrs['departure_date'] >= attrs['arrival_date']:
            raise serializers.ValidationError('Departure must happen after arrival date.')

        self.context['membership'] = membership
        return attrs

    def create(self, validated_data):
        """create ride and update rides taken and offers"""

        # circle
        circle = self.context['circle']
        circle.rides_offered += 1
        circle.save()
        # Ride
        ride = Ride.objects.create(**validated_data, offered_in=circle)
        # Membership
        membership = self.context['membership']
        membership.rides_offered += 1
        membership.save()

        # profile offered
        profile = validated_data['offered_by'].profile
        profile.rides_offered += 1
        profile.save()

        return ride


class JoinRideSerializer(serializers.ModelSerializer):
    """Join ride serializer"""

    passenger = serializers.IntegerField()

    class Meta:
        """Meta class"""

        model = Ride
        fields = ('passenger',)

    def validate_passenger(self, attrs):
        """Verify passenger exists and is a circle member"""
        try:
            user = User.objects.get(pk=attrs)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid user')

        circle = self.context['circle']
        try:
            member = Membership.objects.get(
                user=user,
                circle=circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the circle.')

        self.context['user'] = user
        self.context['member'] = member
        return attrs

    def validate(self, attrs):
        """verify rides allow new passengers"""

        ride = self.context['ride']

        if ride.departure_date <= timezone.now():
            raise serializers.ValidationError('you can\'t join this ride now')

        if ride.available_seats < 1:
            raise serializers.ValidationError('Ride is already full!')

        if Ride.objects.filter(passengers__pk=attrs['passenger']):
            raise serializers.ValidationError('Passenger is already in this trip')

        return attrs

    def update(self, instance, validated_data):
        """Add passenger to ride and update stats."""
        ride = self.context['ride']
        user = self.context['user']

        ride.passengers.add(user)
        ride.available_seats -= 1
        # Profile
        profile = user.profile
        profile.rides_taken += 1
        profile.save()

        # Membership
        member = self.context['member']
        member.rides_taken += 1
        member.save()

        # Circle
        circle = self.context['circle']
        circle.rides_taken += 1
        circle.save()

        return ride


class EndRideSerializer(serializers.ModelSerializer):
    """End ride serializer"""

    current_time = serializers.DateTimeField()

    class Meta:
        """Meta Class"""

        model = Ride
        fields = ('is_active', 'current_time')

    def validated_current_time(self, attrs):
        """Verify ride have indeed started."""
        ride = self.context['view'].get_object()
        if attrs <= ride.departure_date:
            raise serializers.ValidationError('Ride has not stated yet')
        return attrs
