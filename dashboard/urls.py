from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.redirect_dashboard, name='redirect_dashboard'),
    path('dashboard/admin/', views.admin_panel, name='admin_panel'),
    path('dashboard/gestor/', views.gestor_panel, name='gestor_panel'),
    path('dashboard/usuario/', views.usuario_panel, name='usuario_panel'),
    path('dashboard/sin-permiso/', views.sin_permiso_view, name='sin_permiso'),
]
