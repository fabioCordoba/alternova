from rest_framework.permissions import BasePermission

    
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