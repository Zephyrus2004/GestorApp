from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Productos
    path('', views.producto_lista, name='producto_lista'),
    path('producto/<int:pk>/', views.producto_detalle, name='producto_detalle'),
    path('producto/nuevo/', views.producto_crear, name='producto_crear'),
    path('producto/<int:pk>/editar/', views.producto_editar, name='producto_editar'),
    path('producto/<int:pk>/eliminar/', views.producto_eliminar, name='producto_eliminar'),
    # Categorías
    path('categorias/', views.categoria_lista, name='categoria_lista'),
    path('categorias/nueva/', views.categoria_crear, name='categoria_crear'),
]
