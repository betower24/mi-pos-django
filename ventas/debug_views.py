from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncDate
from .models import Venta, DetalleVenta
from datetime import datetime, timedelta

def debug_ventas(request):
    """Vista para debuggear ventas"""
    hoy = datetime.now().date()
    
    # Todas las ventas
    todas_ventas = Venta.objects.all().count()
    
    # Ventas de hoy
    ventas_hoy = Venta.objects.filter(fecha__date=hoy)
    
    # Ventas por día (últimos 7 días)
    ventas_semana = Venta.objects.filter(
        fecha__date__gte=hoy - timedelta(days=7)
    ).annotate(
        dia=TruncDate('fecha')
    ).values('dia').annotate(
        count=Count('id')
    ).order_by('-dia')
    
    # Detalles de ventas de hoy
    detalles_hoy = list(DetalleVenta.objects.filter(
        venta__fecha__date=hoy
    ).values(
        'venta__id',
        'venta__fecha',
        'producto__nombre',
        'cantidad',
        'precio_unitario'
    ))
    
    return JsonResponse({
        'total_ventas_sistema': todas_ventas,
        'ventas_hoy': ventas_hoy.count(),
        'ventas_ultima_semana': list(ventas_semana),
        'detalles_ventas_hoy': detalles_hoy,
        'fecha_servidor': str(datetime.now()),
        'fecha_hoy': str(hoy)
    }, json_dumps_params={'indent': 2})