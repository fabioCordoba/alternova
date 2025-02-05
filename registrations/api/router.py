from django.urls import path
from rest_framework.routers import DefaultRouter
from registrations.api.views import RegistrationApiViewSet
from registrations.api.views import RegisterView

router_registrations = DefaultRouter()

router_registrations.register(prefix='registrations', basename='registrations', viewset=RegistrationApiViewSet)
urlpatterns = [
    path('reg/register', RegisterView.as_view()),
]