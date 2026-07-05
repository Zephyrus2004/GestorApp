from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def rol_requerido(*roles):
    """Decorador que restringe el acceso a usuarios con roles específicos."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('accounts:login')
            
            if not hasattr(request.user, 'profile'):
                messages.error(request, 'Tu cuenta no tiene un perfil configurado.')
                return redirect('accounts:login')
            
            if request.user.is_superuser or request.user.profile.rol in roles:
                return view_func(request, *args, **kwargs)
            
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('dashboard:sin_permiso')
        return wrapper
    return decorator
