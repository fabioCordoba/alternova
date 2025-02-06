from rest_framework import serializers
from registrations.models import Registration


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['student_id', 'subject_id', 'registration_date', 'final_rating']

