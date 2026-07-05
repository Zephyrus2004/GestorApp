from rest_framework import serializers
from .models import Categoria, Producto, Asignacion

class CategoriaSerializer(serializers.ModelSerializer):
    total_productos = serializers.IntegerField(source='total_productos', read_only=True)

    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'icono', 'total_productos', 'created_at']


class ProductoSerializer(serializers.ModelSerializer):
    categoria_detalle = CategoriaSerializer(source='categoria', read_only=True)
    registrado_por_name = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'categoria', 'categoria_detalle',
            'marca', 'modelo', 'numero_serie', 'precio', 'stock', 'estado',
            'disponible', 'imagen', 'ubicacion', 'created_at', 'updated_at',
            'registrado_por', 'registrado_por_name'
        ]
        read_only_fields = ['registrado_por', 'created_at', 'updated_at']

    def get_registrado_por_name(self, obj):
        if obj.registrado_por:
            return obj.registrado_por.get_full_name() or obj.registrado_por.username
        return None


class AsignacionSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    asignado_a_name = serializers.SerializerMethodField()
    asignado_por_name = serializers.SerializerMethodField()

    class Meta:
        model = Asignacion
        fields = [
            'id', 'producto', 'producto_nombre', 'asignado_a', 'asignado_a_name',
            'departamento', 'fecha_asignacion', 'fecha_devolucion', 'estado',
            'observaciones', 'asignado_por', 'asignado_por_name'
        ]
        read_only_fields = ['asignado_por', 'fecha_asignacion']

    def get_asignado_a_name(self, obj):
        if obj.asignado_a:
            return obj.asignado_a.get_full_name() or obj.asignado_a.username
        return None

    def get_asignado_por_name(self, obj):
        if obj.asignado_por:
            return obj.asignado_por.get_full_name() or obj.asignado_por.username
        return None
