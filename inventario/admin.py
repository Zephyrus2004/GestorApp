from django.contrib import admin
from .models import Categoria, Producto, Asignacion


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'total_productos', 'icono', 'created_at')
    search_fields = ('nombre',)
    list_per_page = 25


class AsignacionInline(admin.TabularInline):
    model = Asignacion
    extra = 0
    readonly_fields = ('fecha_asignacion',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'marca', 'modelo', 'stock', 'estado', 'disponible', 'precio')
    list_filter = ('categoria', 'estado', 'disponible', 'marca')
    search_fields = ('nombre', 'marca', 'modelo', 'numero_serie')
    list_editable = ('stock', 'disponible', 'estado')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25
    inlines = [AsignacionInline]

    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'descripcion', 'categoria', 'imagen')
        }),
        ('Detalles del Producto', {
            'fields': ('marca', 'modelo', 'numero_serie', 'precio', 'stock', 'estado')
        }),
        ('Ubicación y Disponibilidad', {
            'fields': ('ubicacion', 'disponible', 'registrado_por')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['marcar_disponible', 'marcar_no_disponible']

    @admin.action(description='Marcar como disponible')
    def marcar_disponible(self, request, queryset):
        queryset.update(disponible=True)

    @admin.action(description='Marcar como no disponible')
    def marcar_no_disponible(self, request, queryset):
        queryset.update(disponible=False)


@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ('producto', 'asignado_a', 'departamento', 'estado', 'fecha_asignacion')
    list_filter = ('estado', 'departamento')
    search_fields = ('producto__nombre', 'asignado_a__username', 'departamento')
    readonly_fields = ('fecha_asignacion',)
    list_per_page = 25
