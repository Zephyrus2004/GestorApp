# ==============================================================================
# SECCIÓN: CONTROLADORES Y VISTAS DE API (INVENTARIO)
# ==============================================================================
# Este módulo define las vistas API para la gestión del inventario y las asignaciones.
# Utiliza Django REST Framework ViewSets para mapear automáticamente las operaciones
# CRUD (Create, Read, Update, Delete) a endpoints REST HTTP.

from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Categoria, Producto, Asignacion
from .serializers import CategoriaSerializer, ProductoSerializer, AsignacionSerializer
from accounts.permissions import IsGestorOrReadOnly, IsAdminUser, IsGestorUser

class CategoriaViewSet(viewsets.ModelViewSet):
    """
    Controlador para la gestión de Categorías.
    - Lectura (GET): Permitido para todos los usuarios autenticados.
    - Escritura (POST, PUT, DELETE): Restringido a Gestores y Administradores (IsGestorOrReadOnly).
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsGestorOrReadOnly]


class ProductoViewSet(viewsets.ModelViewSet):
    """
    Controlador para la gestión de Productos o Equipos de cómputo.
    - Búsqueda avanzada y filtros integrados en la consulta.
    - Eliminación (DELETE): Reservado exclusivamente para Administradores.
    - Creación/Edición: Permitido para Gestores y Administradores.
    """
    serializer_class = ProductoSerializer

    def get_permissions(self):
        # Restricción granular de permisos por acción
        if self.action == 'destroy':
            return [IsAdminUser()] # Eliminar sólo administradores
        return [IsGestorOrReadOnly()] # Crear, editar o listar para gestores/admin

    def get_queryset(self):
        # Optimiza la consulta cargando de antemano las relaciones foráneas (select_related)
        queryset = Producto.objects.select_related('categoria', 'registrado_por').all()
        
        # 1. Búsqueda por palabra clave en múltiples campos a la vez (?q=...)
        q = self.request.query_params.get('q', None)
        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q) |
                Q(marca__icontains=q) |
                Q(modelo__icontains=q) |
                Q(numero_serie__icontains=q)
            )
            
        # 2. Filtro por categoría específica (?categoria=ID)
        categoria = self.request.query_params.get('categoria', None)
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
            
        # 3. Filtro por estado físico (?estado=nuevo/bueno/etc.)
        estado = self.request.query_params.get('estado', None)
        if estado:
            queryset = queryset.filter(estado=estado)
            
        # 4. Filtro de disponibilidad (?disponible=true/false)
        disponible = self.request.query_params.get('disponible', None)
        if disponible:
            queryset = queryset.filter(disponible=disponible.lower() == 'true')
            
        return queryset

    def perform_create(self, serializer):
        # Inyecta automáticamente el usuario que crea el producto (registrado_por)
        serializer.save(registrado_por=self.request.user)


class AsignacionViewSet(viewsets.ModelViewSet):
    """
    Controlador para los Préstamos y Asignaciones de equipos.
    - Creación y edición: Exclusivo para Gestores y Administradores (IsGestorUser).
    - Lectura (GET): 
        * Gestores/Admin pueden ver todas las asignaciones del sistema.
        * Usuarios regulares solo pueden consultar las asignaciones hechas a su nombre.
    """
    serializer_class = AsignacionSerializer

    def get_permissions(self):
        # Métodos de escritura requieren rol de Gestor
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsGestorUser()]
        # Listado y detalle requiere autenticación básica
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        # Carga optimizada de relaciones
        queryset = Asignacion.objects.select_related('producto', 'asignado_a', 'asignado_por').all()
        
        # Filtro de visibilidad por rol
        # Si no es admin ni gestor, aplicar filtro estricto para ver solo lo propio
        if not (user.is_superuser or (hasattr(user, 'profile') and user.profile.rol in ['admin', 'gestor'])):
            queryset = queryset.filter(asignado_a=user)
            
        return queryset

    def perform_create(self, serializer):
        # Inyecta automáticamente qué administrador/gestor registró la entrega
        serializer.save(asignado_por=self.request.user)
