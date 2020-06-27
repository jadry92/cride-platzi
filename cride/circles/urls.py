"""Circle URls"""

# django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import circles as circle_views

router = DefaultRouter()
router.register(r'circles', circle_views.CirclesViewSet, basename='circle')

urlpatterns = [
    path('', include(router.urls))
]