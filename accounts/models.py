# ==============================================================================
# SECCIÓN: CONFIGURACIÓN DE MODELOS DE USUARIO (ACCOUNTS)
# ==============================================================================
# Este archivo define la estructura de datos para los usuarios en la base de datos.
# Utiliza el modelo User predeterminado de Django y lo extiende a través de una
# relación uno a uno (OneToOneField) para añadir roles y campos personalizados.

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Perfil extendido del usuario que define los roles de seguridad y datos complementarios.
    Cada usuario del sistema Django tendrá asociado exactamente un UserProfile.
    """
    
    # Definición de los roles válidos del sistema utilizando TextChoices
    class Rol(models.TextChoices):
        ADMIN = 'admin', 'Administrador'   # Acceso total a la aplicación, APIs y panel de control
        GESTOR = 'gestor', 'Gestor'         # Gestión del catálogo de inventario y categorías
        USUARIO = 'usuario', 'Usuario'     # Consulta de inventario y realización de préstamos/solicitudes

    # Relación OneToOne con el modelo User nativo de Django
    # Si el usuario es eliminado, su perfil también se elimina en cascada (CASCADE)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Usuario'
    )
    
    # Campo para almacenar el rol del usuario, por defecto 'usuario' (Usuario Estándar)
    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.USUARIO,
        verbose_name='Rol'
    )
    
    # Campos adicionales del perfil
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Avatar'
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono'
    )
    departamento = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Departamento'
    )
    
    # Fechas de auditoría de creación y modificación
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de registro'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'
        ordering = ['-created_at']

    def __str__(self):
        # Devuelve el nombre completo del usuario si existe; de lo contrario, su nombre de usuario
        return f"{self.user.get_full_name() or self.user.username} ({self.get_rol_display()})"

    # Propiedades de conveniencia (helpers) para simplificar la verificación de permisos en las vistas y templates
    @property
    def is_admin(self):
        """Verifica si el usuario tiene el rol de Administrador."""
        return self.rol == self.Rol.ADMIN

    @property
    def is_gestor(self):
        """Verifica si el usuario tiene el rol de Gestor de Inventario."""
        return self.rol == self.Rol.GESTOR

    @property
    def is_usuario(self):
        """Verifica si el usuario tiene el rol de Usuario Estándar."""
        return self.rol == self.Rol.USUARIO

