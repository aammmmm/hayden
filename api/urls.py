from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets.user_viewset import UserViewSet

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]

