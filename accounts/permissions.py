from rest_framework import permissions
from .models import UserProfile

class IsAdminUser(permissions.BasePermission):
    """Permiso exclusivo para administradores."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.rol == UserProfile.Rol.ADMIN)


class IsGestorUser(permissions.BasePermission):
    """Permiso para gestores y administradores."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            request.user.is_superuser or 
            (hasattr(request.user, 'profile') and request.user.profile.rol in [UserProfile.Rol.ADMIN, UserProfile.Rol.GESTOR])
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permiso de solo lectura para todos, escritura solo para admin."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and (
            request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.rol == UserProfile.Rol.ADMIN)
        )


class IsGestorOrReadOnly(permissions.BasePermission):
    """Permiso de solo lectura para todos, escritura para gestor/admin."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and (
            request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.rol in [UserProfile.Rol.ADMIN, UserProfile.Rol.GESTOR])
        )
