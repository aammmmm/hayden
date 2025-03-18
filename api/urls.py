from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import viewsets

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'users', viewsets.UserViewSet, basename='user')
router.register(r'packages', viewsets.PackageViewSet, basename='package')

urlpatterns = [
    path('', include(router.urls)),
]

