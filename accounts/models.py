from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Perfil extendido del usuario con rol y datos adicionales."""
    
    class Rol(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        GESTOR = 'gestor', 'Gestor'
        USUARIO = 'usuario', 'Usuario'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Usuario'
    )
    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.USUARIO,
        verbose_name='Rol'
    )
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
        return f"{self.user.get_full_name() or self.user.username} ({self.get_rol_display()})"

    @property
    def is_admin(self):
        return self.rol == self.Rol.ADMIN

    @property
    def is_gestor(self):
        return self.rol == self.Rol.GESTOR

    @property
    def is_usuario(self):
        return self.rol == self.Rol.USUARIO
