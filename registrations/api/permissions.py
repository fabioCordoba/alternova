from rest_framework.permissions import BasePermission, SAFE_METHODS

    
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
    
class IsStudentOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in SAFE_METHODS:
            return user.is_authenticated and user.rol in ['alumno', 'profesor']
        
        if request.method == 'POST':
            return user.is_authenticated and user.rol == 'alumno'
        
        return user.is_authenticated and user.is_staff