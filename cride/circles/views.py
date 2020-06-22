""" circles Views """

# Django
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Models
from cride.circles.models import Circle

# Serializers
from cride.circles.serializers import CirclesSerializer, CreateCircle


@api_view(['GET'])
def list_circles(request):
    """List circles"""
    circles = Circle.objects.filter(is_public=True)
    serializer = CirclesSerializer(circles, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def create_circle(request):
    """create circle."""
    serializer = CreateCircle(data=request.data)
    serializer.is_valid(raise_exception=True)
    circle = serializer.save()
    return Response(circle)
