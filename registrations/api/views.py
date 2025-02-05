from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from registrations.api.permissions import IsAlumnoOrReadOnly
from registrations.api.serializers import RegistrationRegisterSerializer, RegistrationSerializer
from registrations.models import Registration
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from users.api.serializers import UserSerializer
from users.models import User


class RegistrationApiViewSet(ModelViewSet):
    permission_classes = [IsAlumnoOrReadOnly]
    serializer_class = RegistrationSerializer
    queryset = Registration.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['registration_date']

class RegisterView(APIView):
    def post(self, request):
        user = User.objects.get(id=request.user.id)
        print(user)
        serializer = RegistrationRegisterSerializer(user, data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
