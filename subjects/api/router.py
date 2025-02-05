from rest_framework.routers import DefaultRouter
from subjects.api.views import SubjectApiViewSet

router_subjects = DefaultRouter()

router_subjects.register(prefix='subjects', basename='subjects', viewset=SubjectApiViewSet)