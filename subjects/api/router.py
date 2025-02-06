from django.urls import path
from rest_framework.routers import DefaultRouter
from subjects.api.views import ApprovedSubjectsView, FailedSubjectsView, FinalizeSubjectView, StudentSubjectsView, StudentsGradesView, StudentsPerSubjectView, SubjectApiViewSet, TeacherSubjectsView

router_subjects = DefaultRouter()

router_subjects.register(prefix='subjects', basename='subjects', viewset=SubjectApiViewSet)
urlpatterns = [
    path('subjects/list', StudentSubjectsView.as_view()),
    path('subjects/approved', ApprovedSubjectsView.as_view()),
    path('subjects/teacher', TeacherSubjectsView.as_view()),
    path('subjects/professor-students', StudentsPerSubjectView.as_view()),
    path('subjects/professor/ratings', StudentsGradesView.as_view()),
    path('subjects/failed', FailedSubjectsView.as_view()),
    path('subjects/finalize/<int:subject_id>/', FinalizeSubjectView.as_view()),
]