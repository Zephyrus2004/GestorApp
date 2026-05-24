from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CategoriaViewSet, ProductoViewSet, AsignacionViewSet

router = DefaultRouter()
router.register('categorias', CategoriaViewSet, basename='api-categoria')
router.register('productos', ProductoViewSet, basename='api-producto')
router.register('asignaciones', AsignacionViewSet, basename='api-asignacion')

urlpatterns = [
    path('', include(router.urls)),
]
