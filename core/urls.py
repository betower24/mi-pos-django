from django.contrib import admin
from django.urls import path
from ventas.views import punto_de_venta, procesar_venta
from inventario.views import agregar_producto  # Esta es la importación correcta

# core/urls.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', punto_de_venta, name='pos'),
    path('procesar-venta/', procesar_venta, name='procesar_venta'),
    
    # Cambia 'agregar-producto/' por 'agregar_producto/'
    path('agregar_producto/', agregar_producto, name='agregar_producto'),
]