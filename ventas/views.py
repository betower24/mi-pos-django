from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Venta, DetalleVenta
from inventario.models import Producto
from .whatsapp import enviar_whatsapp_venta  # ⬅️ IMPORTAR

@csrf_exempt
@require_http_methods(["POST"])
def procesar_venta(request):
    try:
        data = json.loads(request.body)
        carrito = data.get('carrito', [])
        total = data.get('total', 0)

        if not carrito:
            return JsonResponse({'message': 'Carrito vacío'}, status=400)

        # Crear la venta
        venta = Venta.objects.create(total=total)

        # Procesar cada producto
        for item in carrito:
            producto = Producto.objects.get(nombre=item['nombre'])
            
            # Validar stock
            if producto.stock < item['cantidad']:
                venta.delete()
                return JsonResponse({
                    'message': f'Stock insuficiente para {producto.nombre}'
                }, status=400)
            
            # Reducir stock
            producto.stock -= item['cantidad']
            producto.save()
            
            # Crear detalle de venta
            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=item['cantidad'],
                precio_unitario=item['precio']
            )

        # 🔥 ENVIAR WHATSAPP
        enviar_whatsapp_venta(venta, carrito)

        return JsonResponse({
            'message': 'Venta realizada con éxito',
            'venta_id': venta.id
        }, status=200)

    except Producto.DoesNotExist:
        return JsonResponse({'message': 'Producto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
