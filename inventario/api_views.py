from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Categoria, Producto, Asignacion
from .serializers import CategoriaSerializer, ProductoSerializer, AsignacionSerializer
from accounts.permissions import IsGestorOrReadOnly, IsAdminUser, IsGestorUser

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsGestorOrReadOnly]


class ProductoViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdminUser()]
        return [IsGestorOrReadOnly()]

    def get_queryset(self):
        queryset = Producto.objects.select_related('categoria', 'registrado_por').all()
        
        # Búsqueda por texto (nombre, marca, modelo, número de serie)
        q = self.request.query_params.get('q', None)
        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q) |
                Q(marca__icontains=q) |
                Q(modelo__icontains=q) |
                Q(numero_serie__icontains=q)
            )
            
        # Filtros
        categoria = self.request.query_params.get('categoria', None)
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
            
        estado = self.request.query_params.get('estado', None)
        if estado:
            queryset = queryset.filter(estado=estado)
            
        disponible = self.request.query_params.get('disponible', None)
        if disponible:
            queryset = queryset.filter(disponible=disponible.lower() == 'true')
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(registrado_por=self.request.user)


class AsignacionViewSet(viewsets.ModelViewSet):
    serializer_class = AsignacionSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsGestorUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        queryset = Asignacion.objects.select_related('producto', 'asignado_a', 'asignado_por').all()
        
        # Si no es admin ni gestor, solo puede ver sus propias asignaciones
        if not (user.is_superuser or (hasattr(user, 'profile') and user.profile.rol in ['admin', 'gestor'])):
            queryset = queryset.filter(asignado_a=user)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(asignado_por=self.request.user)
