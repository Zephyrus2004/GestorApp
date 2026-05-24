from rest_framework import viewsets, permissions, status, views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserCreateSerializer, LoginSerializer
from .permissions import IsAdminUser
from inventario.models import Producto, Categoria, Asignacion

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('profile').all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        return [IsAdminUser()]


class LoginAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"non_field_errors": ["Credenciales inválidas."]},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if not user.is_active:
            return Response(
                {"non_field_errors": ["Esta cuenta está desactivada."]},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        
        return Response({
            "token": token.key,
            "user": UserSerializer(user, context={'request': request}).data
        })


class LogoutAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        logout(request)
        return Response({"detail": "Sesión cerrada correctamente."}, status=status.HTTP_200_OK)


class ProfileAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DashboardStatsAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        rol = profile.rol if profile else 'visitante'
        
        if user.is_superuser:
            rol = 'admin'
            
        stats = {}
        
        if rol == 'admin':
            stats = {
                'total_usuarios': User.objects.count(),
                'total_productos': Producto.objects.count(),
                'total_categorias': Categoria.objects.count(),
                'usuarios_recientes': UserSerializer(User.objects.order_by('-date_joined')[:5], many=True, context={'request': request}).data,
                'productos_recientes': list(Producto.objects.order_by('-created_at')[:5].values('id', 'nombre', 'marca', 'modelo', 'precio', 'created_at', 'stock'))
            }
        elif rol == 'gestor':
            stats = {
                'total_productos': Producto.objects.count(),
                'total_categorias': Categoria.objects.count(),
                'productos_bajo_stock': list(Producto.objects.filter(stock__lte=5).order_by('stock')[:10].values('id', 'nombre', 'stock', 'estado', 'marca', 'modelo')),
                'productos_recientes': list(Producto.objects.order_by('-created_at')[:10].values('id', 'nombre', 'marca', 'modelo', 'precio', 'created_at', 'stock'))
            }
        elif rol == 'usuario':
            stats = {
                'productos_disponibles': Producto.objects.filter(disponible=True).count(),
                'tus_asignaciones_activas': Asignacion.objects.filter(asignado_a=user, estado='activa').count()
            }
        else: # visitante
            stats = {
                'mensaje': 'Bienvenido a la tienda de informática. Solicita privilegios de usuario para ver y realizar solicitudes.'
            }
            
        return Response(stats)
