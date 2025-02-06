from rest_framework.permissions import BasePermission
from subjects.models import Subject


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return request.user.is_staff
        
class IsAlumnoOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True 
        return request.user.rol == 'alumno'
    
class IsTeacherOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True 
        return request.user.rol == 'profesor'