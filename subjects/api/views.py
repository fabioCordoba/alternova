from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response

from registrations.models import Registration
from subjects.api.permissions import IsAdminOrReadOnly, IsAlumnoOrReadOnly, IsTeacherOrReadOnly
from subjects.api.serializers import ApprovedSubjectsSerializer, FailedSubjectsSerializer, FinalizeSubjectSerializer, StudentSubjectsSerializer, SubjectSerializer, SubjectWithGradesSerializer, SubjectWithStudentsSerializer
from subjects.models import Subject


class SubjectApiViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['name']

class StudentSubjectsView(APIView):
    permission_classes = [IsAlumnoOrReadOnly]

    def get(self, request):
        user = request.user
        if user.rol != 'alumno':
            return Response({"error": "Solo los alumnos pueden ver sus materias inscritas."}, status=403)

        registrations = Registration.objects.filter(student_id=user)
        serialized_data = StudentSubjectsSerializer(registrations, many=True).data

        return Response(serialized_data)

class ApprovedSubjectsView(APIView):
    permission_classes = [IsAlumnoOrReadOnly]

    def get(self, request):
        user = request.user

        if user.rol != 'alumno':
            return Response({"error": "Solo los alumnos pueden ver sus materias aprobadas."}, status=403)
        approved_subjects = Registration.objects.filter(student_id=user, final_rating__gte=3.0)
        serialized_data = ApprovedSubjectsSerializer(approved_subjects, many=True).data

        return Response(serialized_data)
    
class TeacherSubjectsView(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    def get(self, request):
        user = request.user

        if user.rol != 'profesor':
            return Response({"error": "Solo los profesores pueden ver sus materias asignadas."}, status=403)

        subjects = user.subjects.all() 
        serialized_data = SubjectSerializer(subjects, many=True).data

        return Response(serialized_data)
    
class StudentsGradesView(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    def get(self, request):
        user = request.user

        if user.rol != 'profesor':
            return Response({"error": "Solo los profesores pueden ver las calificaciones."}, status=403)

        subjects = user.subjects.all()
        serialized_data = SubjectWithGradesSerializer(subjects, many=True).data

        return Response(serialized_data)
    
class StudentsPerSubjectView(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    def get(self, request):
        user = request.user
        if user.rol != 'profesor':
            return Response({"error": "Solo los profesores pueden ver la lista de estudiantes."}, status=403)

        subjects = user.subjects.all()
        serialized_data = SubjectWithStudentsSerializer(subjects, many=True).data

        return Response(serialized_data)
    
class FailedSubjectsView(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    def get(self, request):
        user = request.user
        if user.rol != 'alumno':
            return Response({"error": "Solo los estudiantes pueden ver sus materias reprobadas."}, status=403)

        failed_subjects = Registration.objects.filter(student_id=user, final_rating__lt=3.0)
        serialized_data = FailedSubjectsSerializer(failed_subjects, many=True).data
        
        return Response(serialized_data)
    
class FinalizeSubjectView(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    def patch(self, request, subject_id):
        user = request.user

        if user.rol != 'profesor':
            return Response({"error": "Solo los profesores pueden finalizar materias."}, status=403)

        try:
            subject = Subject.objects.get(id=subject_id, teacher_id=user)
        except Subject.DoesNotExist:
            return Response({"error": "Materia no encontrada o no pertenece al profesor."}, status=404)

        serializer = FinalizeSubjectSerializer(subject, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Materia finalizada con éxito."}, status=200)

        return Response(serializer.errors, status=400)