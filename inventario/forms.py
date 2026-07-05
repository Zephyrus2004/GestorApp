from django import forms
from .models import Producto, Categoria, Asignacion


class ProductoForm(forms.ModelForm):
    """Formulario para crear/editar productos."""
    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'categoria', 'marca', 'modelo',
            'numero_serie', 'precio', 'stock', 'estado', 'disponible',
            'imagen', 'ubicacion'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CategoriaForm(forms.ModelForm):
    """Formulario para crear/editar categorías."""
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'icono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'icono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'bi-laptop'}),
        }


class AsignacionForm(forms.ModelForm):
    """Formulario para asignar productos."""
    class Meta:
        model = Asignacion
        fields = ['producto', 'asignado_a', 'departamento', 'observaciones']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'asignado_a': forms.Select(attrs={'class': 'form-select'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
