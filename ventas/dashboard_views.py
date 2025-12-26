from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Count, Avg, F, DecimalField, ExpressionWrapper
from django.db.models.functions import TruncHour
from datetime import datetime, timedelta
from .models import Venta, DetalleVenta

def dashboard(request):
    """Vista principal del dashboard"""
    return render(request, 'dashboard.html')

def dashboard_data(request):
    """API que devuelve los datos del dashboard"""
    try:
        hoy = datetime.now().date()
        ayer = hoy - timedelta(days=1)
        
        # Ventas de hoy
        ventas_hoy = Venta.objects.filter(fecha__date=hoy)
        ventas_ayer = Venta.objects.filter(fecha__date=ayer)
        
        # Total de ventas
        total_ventas_hoy = ventas_hoy.aggregate(total=Sum('total'))['total'] or 0
        total_ventas_ayer = ventas_ayer.aggregate(total=Sum('total'))['total'] or 0
        
        # Número de ventas
        numero_ventas = ventas_hoy.count()
        
        # Promedio de venta
        promedio_venta = ventas_hoy.aggregate(promedio=Avg('total'))['promedio'] or 0
        
        # Comparación con día anterior
        if total_ventas_ayer > 0:
            comparacion = ((total_ventas_hoy - total_ventas_ayer) / total_ventas_ayer) * 100
        else:
            comparacion = 0 if total_ventas_hoy == 0 else 100
        
        # Productos más vendidos (CORREGIDO)
        detalles_hoy = DetalleVenta.objects.filter(venta__fecha__date=hoy)
        
        # Crear un diccionario para agrupar productos
        productos_dict = {}
        
        for detalle in detalles_hoy:
            nombre = detalle.producto.nombre
            if nombre not in productos_dict:
                productos_dict[nombre] = {
                    'nombre': nombre,
                    'cantidad': 0,
                    'ingresos': 0
                }
            productos_dict[nombre]['cantidad'] += detalle.cantidad
            productos_dict[nombre]['ingresos'] += float(detalle.cantidad * detalle.precio_unitario)
        
        # Convertir a lista y ordenar
        productos_mas_vendidos = sorted(
            productos_dict.values(),
            key=lambda x: x['cantidad'],
            reverse=True
        )[:5]
        
        # Ventas por hora
        ventas_por_hora_raw = ventas_hoy.annotate(
            hora=TruncHour('fecha')
        ).values('hora').annotate(
            ventas=Count('id'),
            total=Sum('total')
        ).order_by('hora')
        
        ventas_hora_formateadas = []
        for v in ventas_por_hora_raw:
            if v['hora']:
                ventas_hora_formateadas.append({
                    'hora': v['hora'].strftime('%H:00'),
                    'ventas': v['ventas'],
                    'total': float(v['total'] or 0)
                })
        
        # Si no hay ventas por hora, crear estructura vacía
        if not ventas_hora_formateadas:
            hora_actual = datetime.now().hour
            ventas_hora_formateadas = [{
                'hora': f'{hora_actual}:00',
                'ventas': 0,
                'total': 0
            }]
        
        data = {
            'totalVentas': float(total_ventas_hoy),
            'numeroVentas': numero_ventas,
            'productosMasVendidos': productos_mas_vendidos,
            'ventasPorHora': ventas_hora_formateadas,
            'promedioVenta': float(promedio_venta),
            'comparacionDiaAnterior': round(comparacion, 2)
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        # Devolver el error en JSON para debugging
        import traceback
        return JsonResponse({
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc()
        }, status=500)