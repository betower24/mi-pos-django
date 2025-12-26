from django.contrib import admin
from django.urls import path
from ventas.views import punto_de_venta, procesar_venta
from ventas.dashboard_views import dashboard, dashboard_data  # ← NUEVO
from inventario.views import agregar_producto
from ventas.debug_views import debug_ventas 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', punto_de_venta, name='pos'),
    path('procesar-venta/', procesar_venta, name='procesar_venta'),
    path('agregar_producto/', agregar_producto, name='agregar_producto'),
    path('dashboard/', dashboard, name='dashboard'),  # ← NUEVO
    path('api/dashboard-data/', dashboard_data, name='dashboard_data'),  # ← NUEVO
    path('debug/ventas/', debug_ventas, name='debug_ventas'),
]