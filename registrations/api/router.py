from django.urls import path
from rest_framework.routers import DefaultRouter
from registrations.api.views import RegistrationApiViewSet

router_registrations = DefaultRouter()
router_registrations.register(prefix='registrations', basename='registrations', viewset=RegistrationApiViewSet)
