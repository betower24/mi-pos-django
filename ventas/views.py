import json
from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from inventario.models import Producto
from .models import Venta, DetalleVenta
from django.views.decorators.csrf import csrf_protect

def punto_de_venta(request):
    busqueda = request.GET.get('q', '')
    if busqueda:
        productos = Producto.objects.filter(nombre__icontains=busqueda) | Producto.objects.filter(codigo_barras__icontains=busqueda)
    else:
        productos = Producto.objects.all()[:12]
    return render(request, 'pos/index.html', {'productos': productos, 'busqueda': busqueda})

@csrf_protect
def procesar_venta(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            carrito = data.get('carrito')
            total_venta = data.get('total')

            with transaction.atomic():
                # 1. Crear la venta
                nueva_venta = Venta.objects.create(total=total_venta)
                
                # 2. Crear los detalles
                for item in carrito:
                    # Buscamos el producto (es mejor por nombre o ID)
                    producto = Producto.objects.get(nombre=item['nombre'])
                    
                    DetalleVenta.objects.create(
                        venta=nueva_venta,
                        producto=producto,
                        cantidad=item['cantidad'],
                        precio_unitario=item['precio']
                    )
                    
                    # 3. Descontar stock
                    producto.stock -= int(item['cantidad'])
                    producto.save()

            return JsonResponse({'status': 'ok', 'venta_id': nueva_venta.id})
        except Exception as e:
            print(f"ERROR EN VENTA: {e}") # Esto saldrá en tu terminal de VS Code
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)