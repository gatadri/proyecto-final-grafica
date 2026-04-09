from rest_framework.permissions import BasePermission


class IsDirector(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'director'


class IsProfesor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['profesor', 'director']


class IsPadre(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'padre'
