from rest_framework import serializers
from registrations.models import Registration
from subjects.models import Subject
from users.models import User


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'code', 'name', 'teacher_id', 'prerequisitos', 'is_finalized']

class StudentSubjectsSerializer(serializers.ModelSerializer):
    subject_id = SubjectSerializer() 

    class Meta:
        model = Registration
        fields = ['subject_id']

class ApprovedSubjectsSerializer(serializers.ModelSerializer):
    subject_id = SubjectSerializer()  # Serializar la materia

    class Meta:
        model = Registration
        fields = ['subject_id', 'final_rating']

class StudentGradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student_id.username")  # Nombre del estudiante
    student_email = serializers.CharField(source="student_id.email")    # Email del estudiante

    class Meta:
        model = Registration
        fields = ['student_name', 'student_email', 'final_rating']  # Incluye la nota final

class SubjectWithGradesSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'code', 'name', 'students']

    def get_students(self, obj):
        registrations = Registration.objects.filter(subject_id=obj)
        return StudentGradeSerializer(registrations, many=True).data
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

class SubjectWithStudentsSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'code', 'name', 'students']

    def get_students(self, obj):
        students = User.objects.filter(registrations__subject_id=obj)
        return StudentSerializer(students, many=True).data
    
class FailedSubjectsSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject_id.name")  # Nombre de la materia
    subject_code = serializers.CharField(source="subject_id.code")  # Código de la materia

    class Meta:
        model = Registration
        fields = ['subject_code', 'subject_name', 'final_rating']

class GradeStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['student_id', 'final_rating']  # Permite asignar la nota final

class FinalizeSubjectSerializer(serializers.ModelSerializer):
    students = GradeStudentSerializer(many=True, write_only=True)  # Lista de estudiantes con notas

    class Meta:
        model = Subject
        fields = ['id', 'code', 'name', 'is_finalized', 'students']

    def update(self, instance, validated_data):
        if instance.is_finalized:
            raise serializers.ValidationError("Esta materia ya ha sido finalizada.")

        students_data = validated_data.pop('students', [])
        
        # Actualizar las notas de los estudiantes inscritos
        for student_data in students_data:
            registration = Registration.objects.filter(subject_id=instance, student_id=student_data['student_id']).first()
            if registration:
                registration.final_rating = student_data['final_rating']
                registration.save()

        instance.is_finalized = True  # Marcar la materia como finalizada
        instance.save()
        return instance