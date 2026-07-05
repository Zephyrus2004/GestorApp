# ==============================================================================
# SECCIÓN: MODELOS DE DATOS DEL INVENTARIO (INVENTARIO)
# ==============================================================================
# Este módulo define el esquema de base de datos para la gestión del inventario.
# Contiene los modelos para Categorías, Productos (equipos de cómputo) y las
# Asignaciones o Préstamos de equipos a los usuarios finales del sistema.

from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    """
    Categoría para agrupar los equipos de cómputo/informática (ej. Laptops, Impresoras, Servidores).
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    
    # Campo para almacenar la clase CSS de Bootstrap Icons para renderizar íconos dinámicamente en el Frontend
    icono = models.CharField(
        max_length=50,
        default='bi-box',
        verbose_name='Ícono Bootstrap',
        help_text='Clase de ícono de Bootstrap Icons (ej: bi-laptop, bi-printer)'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    @property
    def total_productos(self):
        """Propiedad calculada para obtener el total de productos asociados a esta categoría."""
        return self.productos.count()


class Producto(models.Model):
    """
    Representa un producto, dispositivo o equipo informático individual.
    """
    
    # Estados físicos en los que puede encontrarse un equipo
    class Estado(models.TextChoices):
        NUEVO = 'nuevo', 'Nuevo'
        BUENO = 'bueno', 'Buen estado'
        REGULAR = 'regular', 'Regular'
        MALO = 'malo', 'Mal estado'
        BAJA = 'baja', 'Dado de baja'

    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    
    # Relación de llave foránea hacia Categoría. 
    # models.PROTECT impide eliminar una categoría si esta contiene productos asociados.
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos',
        verbose_name='Categoría'
    )
    
    marca = models.CharField(max_length=100, blank=True, verbose_name='Marca')
    modelo = models.CharField(max_length=100, blank=True, verbose_name='Modelo')
    
    # Campo único opcional para identificar dispositivos específicos (laptops, PCs, etc.)
    numero_serie = models.CharField(
        max_length=100,
        blank=True,
        unique=True,
        null=True,
        verbose_name='Número de serie'
    )
    
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Precio (USD)'
    )
    
    # Cantidad disponible en almacén
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock')
    
    # Estado físico actual
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.NUEVO,
        verbose_name='Estado'
    )
    
    # Indica si está visible o disponible para préstamos
    disponible = models.BooleanField(default=True, verbose_name='Disponible')
    
    # Imagen referencial del producto/dispositivo
    imagen = models.ImageField(
        upload_to='productos/',
        blank=True,
        null=True,
        verbose_name='Imagen'
    )
    
    # Lugar físico donde se resguarda el equipo (ej. Almacén A, Oficina 203)
    ubicacion = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Ubicación',
        help_text='Edificio, piso, sala, etc.'
    )
    
    # Fechas de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    # Registro de qué usuario creó o dio de alta este producto
    registrado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='productos_registrados',
        verbose_name='Registrado por'
    )

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nombre} - {self.marca} {self.modelo}".strip(' -')

    @property
    def stock_bajo(self):
        """Retorna True si quedan 5 o menos existencias del producto."""
        return self.stock <= 5


class Asignacion(models.Model):
    """
    Representa el préstamo o asignación de un equipo del inventario a un empleado/usuario.
    Permite dar seguimiento a quién tiene cada dispositivo en un momento dado.
    """
    
    class EstadoAsignacion(models.TextChoices):
        ACTIVA = 'activa', 'Activa'       # El equipo está en posesión del usuario
        DEVUELTO = 'devuelto', 'Devuelto' # El equipo ha regresado al almacén
        PERDIDO = 'perdido', 'Perdido'   # El equipo se extravió o dañó sin retorno

    # Llave foránea hacia el producto asignado
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='asignaciones',
        verbose_name='Producto'
    )
    
    # Llave foránea hacia el usuario receptor de la asignación
    asignado_a = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='asignaciones',
        verbose_name='Asignado a'
    )
    
    # Departamento de destino de la asignación (ej: Ventas, TI, Recursos Humanos)
    departamento = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Departamento'
    )
    
    # Fechas de préstamo y retorno
    fecha_asignacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de asignación'
    )
    fecha_devolucion = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Fecha de devolución'
    )
    
    # Estado actual de la asignación
    estado = models.CharField(
        max_length=20,
        choices=EstadoAsignacion.choices,
        default=EstadoAsignacion.ACTIVA,
        verbose_name='Estado'
    )
    
    # Notas del administrador o gestor (detalles de entrega, reportes de daños, etc.)
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    # Quién autorizó o registró este préstamo
    asignado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='asignaciones_realizadas',
        verbose_name='Asignado por'
    )

    class Meta:
        verbose_name = 'Asignación'
        verbose_name_plural = 'Asignaciones'
        ordering = ['-fecha_asignacion']

    def __str__(self):
        return f"{self.producto} → {self.asignado_a.get_full_name() or self.asignado_a.username}"

