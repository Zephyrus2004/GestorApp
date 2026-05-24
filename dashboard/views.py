from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .decorators import rol_requerido


def home_view(request):
    """Página principal pública."""
    if request.user.is_authenticated:
        return redirect('dashboard:redirect_dashboard')
    return render(request, 'dashboard/home.html')


@login_required
def redirect_dashboard(request):
    """Redirige al dashboard correspondiente según el rol del usuario."""
    if request.user.is_superuser:
        return redirect('dashboard:admin_panel')
    
    profile = request.user.profile
    
    redirect_map = {
        'admin': 'dashboard:admin_panel',
        'gestor': 'dashboard:gestor_panel',
        'usuario': 'dashboard:usuario_panel',
        'visitante': 'dashboard:visitante',
    }
    
    target = redirect_map.get(profile.rol, 'dashboard:visitante')
    return redirect(target)


@login_required
@rol_requerido('admin')
def admin_panel(request):
    """Panel del administrador."""
    from inventario.models import Producto, Categoria
    context = {
        'total_usuarios': User.objects.count(),
        'total_productos': Producto.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'usuarios_recientes': User.objects.order_by('-date_joined')[:5],
        'productos_recientes': Producto.objects.order_by('-created_at')[:5],
    }
    return render(request, 'dashboard/admin_panel.html', context)


@login_required
@rol_requerido('gestor')
def gestor_panel(request):
    """Panel del gestor."""
    from inventario.models import Producto, Categoria
    context = {
        'total_productos': Producto.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'productos_bajo_stock': Producto.objects.filter(stock__lte=5).order_by('stock')[:10],
        'productos_recientes': Producto.objects.order_by('-created_at')[:10],
    }
    return render(request, 'dashboard/gestor_panel.html', context)


@login_required
@rol_requerido('usuario')
def usuario_panel(request):
    """Panel del usuario regular."""
    from inventario.models import Producto
    context = {
        'productos_disponibles': Producto.objects.filter(disponible=True).count(),
    }
    return render(request, 'dashboard/usuario_panel.html', context)


@login_required
def visitante_view(request):
    """Vista del visitante."""
    return render(request, 'dashboard/visitante.html')


@login_required
def sin_permiso_view(request):
    """Vista de acceso denegado."""
    return render(request, 'dashboard/sin_permiso.html')
