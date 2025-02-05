from rest_framework import serializers
from registrations.models import Registration
from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['student_id', 'subject_id', 'registration_date', 'final_rating']

class RegistrationRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['subject_id', 'registration_date', 'final_rating']
        # read_only_fields = ['student_id'] 

    def create(self, validated_data):
        user = self.context.get('user') 
        print("***************************")
        # user = request.user  # Usuario autenticado desde el token JWT
        
        # # Buscar el Student asociado al usuario autenticado
        student = User.objects.get(user=user)

        # Asignar el student_id automáticamente
        validated_data['student_id'] = student
        return super().create(validated_data)