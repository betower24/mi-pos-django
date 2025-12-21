from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'codigo_barras')
    search_fields = ('nombre', 'codigo_barras') # Para que puedas buscar productos