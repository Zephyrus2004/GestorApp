from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """Inline para mostrar el perfil dentro del admin de User."""
    model = UserProfile
    can_delete = False
    verbose_name = 'Perfil'
    verbose_name_plural = 'Perfil'
    fk_name = 'user'


class CustomUserAdmin(BaseUserAdmin):
    """Admin personalizado de User con perfil inline."""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_rol')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__rol')

    def get_rol(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.get_rol_display()
        return '-'
    get_rol.short_description = 'Rol'
    get_rol.admin_order_field = 'profile__rol'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin para gestionar perfiles de usuario."""
    list_display = ('user', 'get_email', 'rol', 'departamento', 'telefono', 'created_at')
    list_filter = ('rol', 'departamento')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_editable = ('rol',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Correo'
    get_email.admin_order_field = 'user__email'

    actions = ['hacer_gestor', 'hacer_usuario', 'hacer_visitante']

    @admin.action(description='Cambiar rol a Gestor')
    def hacer_gestor(self, request, queryset):
        count = queryset.update(rol=UserProfile.Rol.GESTOR)
        self.message_user(request, f'{count} usuario(s) actualizados a Gestor.')

    @admin.action(description='Cambiar rol a Usuario')
    def hacer_usuario(self, request, queryset):
        count = queryset.update(rol=UserProfile.Rol.USUARIO)
        self.message_user(request, f'{count} usuario(s) actualizados a Usuario.')

    @admin.action(description='Cambiar rol a Visitante')
    def hacer_visitante(self, request, queryset):
        count = queryset.update(rol=UserProfile.Rol.VISITANTE)
        self.message_user(request, f'{count} usuario(s) actualizados a Visitante.')


# Reemplazar el admin de User por defecto
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
