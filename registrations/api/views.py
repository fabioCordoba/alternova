from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from registrations.api.permissions import IsStudentOrReadOnly
from registrations.api.serializers import RegistrationSerializer
from registrations.models import Registration
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class RegistrationApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsStudentOrReadOnly]
    serializer_class = RegistrationSerializer
    queryset = Registration.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['registration_date']

    
