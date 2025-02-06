from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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

    @swagger_auto_schema(
        operation_summary="Obtain list of registered subjects",
        operation_description="Returns the list of subjects in which the authenticated student is enrolled. Only students can access.",
        responses={
            200: StudentSubjectsSerializer(many=True),
            403: openapi.Response("Solo los alumnos pueden ver sus materias inscritas."),
            401: "No autenticado. Se requiere un token JWT."
        }
    )
    def get(self, request):
        user = request.user
        if user.rol != 'alumno':
            return Response({"error": "Solo los alumnos pueden ver sus materias inscritas."}, status=403)

        registrations = Registration.objects.filter(student_id=user)
        serialized_data = StudentSubjectsSerializer(registrations, many=True).data

        return Response(serialized_data)

class ApprovedSubjectsView(APIView):
    permission_classes = [IsAlumnoOrReadOnly]

    @swagger_auto_schema(
        operation_summary="Obtain approved subjects",
        operation_description="Returns the list of passed subjects of the authenticated student (grade >= 3.0).",
        responses={
            200: ApprovedSubjectsSerializer(many=True),
            403: openapi.Response("Solo los alumnos pueden ver sus materias aprobadas."),
            401: "No autenticado. Se requiere un token JWT."
        }
    )
    def get(self, request):
        user = request.user

        if user.rol != 'alumno':
            return Response({"error": "Solo los alumnos pueden ver sus materias aprobadas."}, status=403)
        approved_subjects = Registration.objects.filter(student_id=user, final_rating__gte=3.0)
        serialized_data = ApprovedSubjectsSerializer(approved_subjects, many=True).data

        return Response(serialized_data)
    
class TeacherSubjectsView(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    @swagger_auto_schema(
        operation_summary="Obtain subjects assigned to a teacher",
        operation_description="Returns the list of subjects assigned to the authenticated teacher.",
        responses={
            200: SubjectSerializer(many=True),
            403: openapi.Response("Solo los profesores pueden ver sus materias."),
            401: "No autenticado. Se requiere un token JWT."
        }
    )
    def get(self, request):
        user = request.user

        if user.rol != 'profesor':
            return Response({"error": "Solo los profesores pueden ver sus materias asignadas."}, status=403)

        subjects = user.subjects.all() 
        serialized_data = SubjectSerializer(subjects, many=True).data

        return Response(serialized_data)
    
class StudentsGradesView(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    @swagger_auto_schema(
        operation_summary="Obtain student grades",
        operation_description="Returns students' grades in the authenticated teacher's subjects.",
        responses={
            200: SubjectWithGradesSerializer(many=True),
            403: openapi.Response("Solo los profesores pueden ver las calificaciones."),
            401: "No autenticado. Se requiere un token JWT."
        }
    )
    def get(self, request):
        user = request.user

        if user.rol != 'profesor':
            return Response({"error": "Solo los profesores pueden ver las calificaciones."}, status=403)

        subjects = user.subjects.all()
        serialized_data = SubjectWithGradesSerializer(subjects, many=True).data

        return Response(serialized_data)
    
class StudentsPerSubjectView(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    @swagger_auto_schema(
        operation_summary="Obtain students by subject",
        operation_description="Returns the list of students in each subject assigned to the authenticated teacher.",
        responses={
            200: SubjectWithStudentsSerializer(many=True),
            403: openapi.Response("Solo los profesores pueden ver la lista de estudiantes."),
            401: "No autenticado. Se requiere un token JWT."
        }
    )
    def get(self, request):
        user = request.user
        if user.rol != 'profesor':
            return Response({"error": "Solo los profesores pueden ver la lista de estudiantes."}, status=403)

        subjects = user.subjects.all()
        serialized_data = SubjectWithStudentsSerializer(subjects, many=True).data

        return Response(serialized_data)
    
class FailedSubjectsView(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    @swagger_auto_schema(
        operation_summary="Obtaining failed subjects",
        operation_description="Returns the list of failed subjects of the authenticated student (grade < 3.0).",
        responses={
            200: FailedSubjectsSerializer(many=True),
            403: openapi.Response("Solo los alumnos pueden ver sus materias reprobadas."),
            401: "No autenticado. Se requiere un token JWT."
        }
    )
    def get(self, request):
        user = request.user
        if user.rol != 'alumno':
            return Response({"error": "Solo los estudiantes pueden ver sus materias reprobadas."}, status=403)

        failed_subjects = Registration.objects.filter(student_id=user, final_rating__lt=3.0)
        serialized_data = FailedSubjectsSerializer(failed_subjects, many=True).data
        
        return Response(serialized_data)
    
class FinalizeSubjectView(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    @swagger_auto_schema(
        operation_summary="Completion of a subject",
        operation_description="Allows a teacher to finish an assigned subject. You must send a JSON with the completion data.",
        request_body=FinalizeSubjectSerializer,
        responses={
            200: openapi.Response("Materia finalizada con éxito."),
            403: openapi.Response("Solo los profesores pueden finalizar materias."),
            404: openapi.Response("Materia no encontrada o no pertenece al profesor."),
            400: "Error de validación en los datos enviados."
        }
    )
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