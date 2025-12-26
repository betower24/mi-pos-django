import os
import django
from decimal import Decimal
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from inventario.models import Producto, Categoria
from ventas.models import Venta, DetalleVenta

# Crear categoría si no existe
categoria, _ = Categoria.objects.get_or_create(nombre='Abarrotes')

# Crear productos de ejemplo
productos_ejemplo = [
    {'codigo_barras': '7501234567890', 'nombre': 'Coca Cola 600ml', 'precio': 15.00, 'stock': 100},
    {'codigo_barras': '7501234567891', 'nombre': 'Sabritas Original', 'precio': 18.00, 'stock': 80},
    {'codigo_barras': '7501234567892', 'nombre': 'Pan Blanco', 'precio': 12.00, 'stock': 50},
    {'codigo_barras': '7501234567893', 'nombre': 'Leche Lala 1L', 'precio': 23.00, 'stock': 60},
    {'codigo_barras': '7501234567894', 'nombre': 'Huevos 12pz', 'precio': 35.00, 'stock': 40},
]

productos_creados = []
for p_data in productos_ejemplo:
    producto, created = Producto.objects.get_or_create(
        codigo_barras=p_data['codigo_barras'],
        defaults={
            'nombre': p_data['nombre'],
            'categoria': categoria,
            'precio': Decimal(str(p_data['precio'])),
            'stock': p_data['stock']
        }
    )
    productos_creados.append(producto)
    if created:
        print(f'✅ Producto creado: {producto.nombre}')
    else:
        print(f'⚠️ Producto ya existe: {producto.nombre}')

# Crear ventas de ejemplo para hoy
ventas_ejemplo = [
    {'productos': [0, 1], 'cantidades': [2, 1]},  # Coca y Sabritas
    {'productos': [2, 3], 'cantidades': [3, 2]},  # Pan y Leche
    {'productos': [4], 'cantidades': [1]},        # Huevos
    {'productos': [0, 2, 3], 'cantidades': [1, 2, 1]},  # Coca, Pan, Leche
]

for venta_data in ventas_ejemplo:
    total = sum(
        productos_creados[i].precio * venta_data['cantidades'][idx]
        for idx, i in enumerate(venta_data['productos'])
    )
    
    venta = Venta.objects.create(total=total, fecha=datetime.now())
    
    for idx, producto_idx in enumerate(venta_data['productos']):
        producto = productos_creados[producto_idx]
        cantidad = venta_data['cantidades'][idx]
        
        DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio
        )
    
    print(f'✅ Venta creada: ${total} - ID: {venta.id}')

print('\n🎉 Datos de prueba creados exitosamente!')