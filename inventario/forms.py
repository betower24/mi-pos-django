from django import forms
from .models import Producto, Categoria

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo_barras', 'nombre', 'categoria', 'precio', 'stock']
        widgets = {
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_codigo_barras'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }