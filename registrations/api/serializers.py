from rest_framework import serializers
from registrations.models import Registration


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['student_id', 'subject_id', 'registration_date', 'final_rating']

    def validate(self, data):
        """ Validar prerrequisitos antes de guardar """
        student = data.get('student_id')
        subject = data.get('subject_id')

        if student and subject:
            prerequisites = subject.prerequisitos.all()
            for prereq in prerequisites:
                # Verificar si el estudiante ha aprobado los prerrequisitos
                if not Registration.objects.filter(student_id=student, subject_id=prereq, final_rating__gte=3.0).exists():
                    raise serializers.ValidationError(
                        f"No puedes inscribirte en {subject} sin haber aprobado {prereq}."
                    )

        return data

