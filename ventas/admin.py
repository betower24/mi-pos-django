from django.contrib import admin
from .models import Venta, DetalleVenta

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0 # Para que no salgan filas vacías de más
    readonly_fields = ('producto', 'cantidad', 'precio_unitario')

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'total')
    inlines = [DetalleVentaInline] # Muestra los productos dentro de la venta