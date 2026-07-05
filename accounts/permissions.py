# ==============================================================================
# SECCIÓN: CONTROL DE ACCESOS Y PERMISOS PERSONALIZADOS (ACCOUNTS)
# ==============================================================================
# Este módulo define las reglas de autorización (permissions) para las APIs de Django.
# Restringe el acceso a las vistas de Django REST Framework según el rol asignado 
# en el perfil del usuario (UserProfile.Rol).

from rest_framework import permissions
from .models import UserProfile

class IsAdminUser(permissions.BasePermission):
    """
    Permiso exclusivo para administradores o superusuarios.
    Se requiere autenticación y que el rol asignado sea 'admin'.
    """
    def has_permission(self, request, view):
        # 1. Verificar si el usuario está autenticado en la petición
        if not request.user or not request.user.is_authenticated:
            return False
            
        # 2. Permitir el paso si es superusuario de Django o si su rol de perfil es ADMIN
        return request.user.is_superuser or (
            hasattr(request.user, 'profile') and 
            request.user.profile.rol == UserProfile.Rol.ADMIN
        )


class IsGestorUser(permissions.BasePermission):
    """
    Permiso para gestores y administradores.
    Ideal para secciones de gestión de inventario y categorías.
    """
    def has_permission(self, request, view):
        # 1. Verificar autenticación
        if not request.user or not request.user.is_authenticated:
            return False
            
        # 2. Permitir el paso si es superusuario o si tiene rol de GESTOR o ADMIN
        return (
            request.user.is_superuser or 
            (hasattr(request.user, 'profile') and 
             request.user.profile.rol in [UserProfile.Rol.ADMIN, UserProfile.Rol.GESTOR])
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso híbrido:
    - Métodos seguros (GET, HEAD, OPTIONS): Solo requiere estar autenticado.
    - Métodos de escritura (POST, PUT, PATCH, DELETE): Exclusivo para el Administrador.
    """
    def has_permission(self, request, view):
        # 1. Si la petición es de solo lectura, permitir a cualquier usuario autenticado
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
            
        # 2. Si es una acción de modificación, exigir que sea Administrador
        return request.user and request.user.is_authenticated and (
            request.user.is_superuser or (
                hasattr(request.user, 'profile') and 
                request.user.profile.rol == UserProfile.Rol.ADMIN
            )
        )


class IsGestorOrReadOnly(permissions.BasePermission):
    """
    Permiso híbrido:
    - Métodos seguros (GET, HEAD, OPTIONS): Solo requiere estar autenticado.
    - Métodos de escritura (POST, PUT, PATCH, DELETE): Exclusivo para Gestores o Administradores.
    """
    def has_permission(self, request, view):
        # 1. Si la petición es de solo lectura, permitir a cualquier usuario autenticado
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
            
        # 2. Si es una acción de modificación, exigir que sea Gestor o Administrador
        return request.user and request.user.is_authenticated and (
            request.user.is_superuser or (
                hasattr(request.user, 'profile') and 
                request.user.profile.rol in [UserProfile.Rol.ADMIN, UserProfile.Rol.GESTOR]
            )
        )

