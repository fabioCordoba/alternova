from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from subjects.api.permissions import IsAdminOrReadOnly
from subjects.api.serializers import SubjectSerializer
from subjects.models import Subject


class SubjectApiViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    # ordering = ['-created_at']
    filterset_fields = ['name']