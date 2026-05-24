from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from dashboard.decorators import rol_requerido
from .models import Producto, Categoria, Asignacion
from .forms import ProductoForm, CategoriaForm


@login_required
def producto_lista(request):
    """Listado de productos con búsqueda y filtros."""
    productos = Producto.objects.select_related('categoria', 'registrado_por').all()
    categorias = Categoria.objects.all()
    
    # Búsqueda
    query = request.GET.get('q', '')
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(marca__icontains=query) |
            Q(modelo__icontains=query) |
            Q(numero_serie__icontains=query)
        )
    
    # Filtro por categoría
    cat_id = request.GET.get('categoria', '')
    if cat_id:
        productos = productos.filter(categoria_id=cat_id)
    
    # Filtro por estado
    estado = request.GET.get('estado', '')
    if estado:
        productos = productos.filter(estado=estado)
    
    # Filtro por disponibilidad
    disponible = request.GET.get('disponible', '')
    if disponible:
        productos = productos.filter(disponible=(disponible == 'true'))
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'query': query,
        'cat_id': cat_id,
        'estado': estado,
        'disponible': disponible,
    }
    return render(request, 'inventario/producto_lista.html', context)


@login_required
def producto_detalle(request, pk):
    """Detalle de un producto."""
    producto = get_object_or_404(Producto.objects.select_related('categoria', 'registrado_por'), pk=pk)
    asignaciones = producto.asignaciones.select_related('asignado_a', 'asignado_por').all()
    
    context = {
        'producto': producto,
        'asignaciones': asignaciones,
    }
    return render(request, 'inventario/producto_detalle.html', context)


@login_required
@rol_requerido('admin', 'gestor')
def producto_crear(request):
    """Crear un nuevo producto."""
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.registrado_por = request.user
            producto.save()
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
            return redirect('inventario:producto_detalle', pk=producto.pk)
    else:
        form = ProductoForm()
    
    return render(request, 'inventario/producto_form.html', {
        'form': form,
        'titulo': 'Nuevo Producto',
        'boton': 'Crear Producto',
    })


@login_required
@rol_requerido('admin', 'gestor')
def producto_editar(request, pk):
    """Editar un producto existente."""
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado.')
            return redirect('inventario:producto_detalle', pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'inventario/producto_form.html', {
        'form': form,
        'producto': producto,
        'titulo': f'Editar: {producto.nombre}',
        'boton': 'Guardar Cambios',
    })


@login_required
@rol_requerido('admin')
def producto_eliminar(request, pk):
    """Eliminar un producto."""
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado correctamente.')
        return redirect('inventario:producto_lista')
    return render(request, 'inventario/producto_confirmar_eliminar.html', {'producto': producto})


@login_required
@rol_requerido('admin', 'gestor')
def categoria_lista(request):
    """Listado de categorías."""
    categorias = Categoria.objects.all()
    return render(request, 'inventario/categoria_lista.html', {'categorias': categorias})


@login_required
@rol_requerido('admin', 'gestor')
def categoria_crear(request):
    """Crear una nueva categoría."""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('inventario:categoria_lista')
    else:
        form = CategoriaForm()
    return render(request, 'inventario/categoria_form.html', {
        'form': form,
        'titulo': 'Nueva Categoría',
    })
