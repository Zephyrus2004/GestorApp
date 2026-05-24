from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    """Categoría de productos de informática."""
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
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
        return self.productos.count()


class Producto(models.Model):
    """Producto o equipo de informática."""
    
    class Estado(models.TextChoices):
        NUEVO = 'nuevo', 'Nuevo'
        BUENO = 'bueno', 'Buen estado'
        REGULAR = 'regular', 'Regular'
        MALO = 'malo', 'Mal estado'
        BAJA = 'baja', 'Dado de baja'

    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos',
        verbose_name='Categoría'
    )
    marca = models.CharField(max_length=100, blank=True, verbose_name='Marca')
    modelo = models.CharField(max_length=100, blank=True, verbose_name='Modelo')
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
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock')
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.NUEVO,
        verbose_name='Estado'
    )
    disponible = models.BooleanField(default=True, verbose_name='Disponible')
    imagen = models.ImageField(
        upload_to='productos/',
        blank=True,
        null=True,
        verbose_name='Imagen'
    )
    ubicacion = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Ubicación',
        help_text='Edificio, piso, sala, etc.'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
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
        return self.stock <= 5


class Asignacion(models.Model):
    """Asignación de un producto a un usuario o departamento."""
    
    class EstadoAsignacion(models.TextChoices):
        ACTIVA = 'activa', 'Activa'
        DEVUELTO = 'devuelto', 'Devuelto'
        PERDIDO = 'perdido', 'Perdido'

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='asignaciones',
        verbose_name='Producto'
    )
    asignado_a = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='asignaciones',
        verbose_name='Asignado a'
    )
    departamento = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Departamento'
    )
    fecha_asignacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de asignación'
    )
    fecha_devolucion = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Fecha de devolución'
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoAsignacion.choices,
        default=EstadoAsignacion.ACTIVA,
        verbose_name='Estado'
    )
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
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
