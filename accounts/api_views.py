# ==============================================================================
# SECCIÓN: CONTROLADORES Y VISTAS DE API (ACCOUNTS)
# ==============================================================================
# Este módulo contiene las vistas (APIViews y ViewSets) de Django REST Framework.
# Gestiona el registro de usuarios, inicio/cierre de sesión, gestión de perfiles
# y las estadísticas dinámicas para los Dashboards de cada rol.

from rest_framework import viewsets, permissions, status, views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserCreateSerializer, LoginSerializer
from .permissions import IsAdminUser
from inventario.models import Producto, Categoria, Asignacion

class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para la gestión de usuarios del sistema.
    Exclusivo para usuarios con rol de Administrador.
    """
    queryset = User.objects.select_related('profile').all()
    
    def get_serializer_class(self):
        # Utiliza un serializador diferente al crear un usuario (para manejar contraseña)
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        # Fuerza que solo administradores puedan consultar/modificar usuarios
        return [IsAdminUser()]


class LoginAPIView(views.APIView):
    """
    Endpoint para iniciar sesión en la aplicación.
    Genera y retorna un Token de autenticación de Django REST Framework (Token Auth)
    y los datos básicos del usuario autenticado.
    """
    permission_classes = [permissions.AllowAny] # Permite el acceso público a este endpoint

    def post(self, request):
        # 1. Validar las credenciales ingresadas usando el serializador
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # 2. Autenticar contra el backend de Django
        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"non_field_errors": ["Credenciales inválidas."]},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 3. Comprobar si el usuario no ha sido desactivado
        if not user.is_active:
            return Response(
                {"non_field_errors": ["Esta cuenta está desactivada."]},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 4. Obtener o crear el Token Auth correspondiente
        token, created = Token.objects.get_or_create(user=user)
        login(request, user) # Vincula la sesión a nivel de Django
        
        # 5. Responder con el token de acceso y la información del usuario
        return Response({
            "token": token.key,
            "user": UserSerializer(user, context={'request': request}).data
        })


class LogoutAPIView(views.APIView):
    """
    Endpoint para cerrar sesión en la aplicación.
    Elimina el token de sesión activo de la base de datos.
    """
    permission_classes = [permissions.IsAuthenticated] # Exige estar autenticado

    def post(self, request):
        try:
            # Eliminar token de base de datos
            request.user.auth_token.delete()
        except Exception:
            pass
        logout(request) # Limpia la sesión de Django
        return Response({"detail": "Sesión cerrada correctamente."}, status=status.HTTP_200_OK)


class ProfileAPIView(views.APIView):
    """
    Endpoint para que los usuarios consulten y editen su propio perfil.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Obtener los datos del usuario logueado actualmente
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    def put(self, request):
        # Actualización parcial o completa del perfil del propio usuario
        serializer = UserSerializer(request.user, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DashboardStatsAPIView(views.APIView):
    """
    Endpoint dinámico que recopila estadísticas del inventario y del sistema
    personalizadas según el rol de quien realiza la petición.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        rol = profile.rol if profile else 'usuario' # Rol fallback por defecto
        
        # Superusuarios de Django por defecto se tratan como admin en las vistas
        if user.is_superuser:
            rol = 'admin'
            
        stats = {}
        
        # 1. Estadísticas para Administradores (Vista global de la plataforma)
        if rol == 'admin':
            stats = {
                'total_usuarios': User.objects.count(),
                'total_productos': Producto.objects.count(),
                'total_categorias': Categoria.objects.count(),
                'usuarios_recientes': UserSerializer(User.objects.order_by('-date_joined')[:5], many=True, context={'request': request}).data,
                'productos_recientes': list(Producto.objects.order_by('-created_at')[:5].values('id', 'nombre', 'marca', 'modelo', 'precio', 'created_at', 'stock'))
            }
        # 2. Estadísticas para Gestores (Monitoreo de Stock e Inventario reciente)
        elif rol == 'gestor':
            stats = {
                'total_productos': Producto.objects.count(),
                'total_categorias': Categoria.objects.count(),
                'productos_bajo_stock': list(Producto.objects.filter(stock__lte=5).order_by('stock')[:10].values('id', 'nombre', 'stock', 'estado', 'marca', 'modelo')),
                'productos_recientes': list(Producto.objects.order_by('-created_at')[:10].values('id', 'nombre', 'marca', 'modelo', 'precio', 'created_at', 'stock'))
            }
        # 3. Estadísticas para Usuarios Estándar (Consulta de productos disponibles y préstamos activos)
        elif rol == 'usuario':
            stats = {
                'productos_disponibles': Producto.objects.filter(disponible=True).count(),
                'tus_asignaciones_activas': Asignacion.objects.filter(asignado_a=user, estado='activa').count()
            }
        # 4. Caso genérico por si no coincide con ninguno
        else:
            stats = {
                'mensaje': 'Bienvenido a la tienda de informática. Solicita privilegios de usuario para ver y realizar solicitudes.'
            }
            
        return Response(stats)

