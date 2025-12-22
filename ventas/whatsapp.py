from twilio.rest import Client
from django.conf import settings
from datetime import datetime

def enviar_whatsapp_venta(venta, carrito):
    """
    Envía un mensaje de WhatsApp con los detalles de la venta
    """
    try:
        # Inicializar cliente de Twilio
        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )
        
        # Crear el mensaje
        productos_texto = ""
        for item in carrito:
            subtotal = item['precio'] * item['cantidad']
            productos_texto += f"\n• {item['nombre']} x{item['cantidad']} = ${subtotal:.2f}"
        
        mensaje = f"""
🛒 *NUEVA VENTA #{venta.id}*

📅 Fecha: {venta.fecha.strftime('%d/%m/%Y %H:%M')}

📦 *Productos:*{productos_texto}

💰 *TOTAL: ${venta.total:.2f}*

✅ Venta registrada exitosamente
"""
        
        # Enviar mensaje
        message = client.messages.create(
            from_=settings.TWILIO_WHATSAPP_FROM,
            body=mensaje,
            to=settings.WHATSAPP_TO
        )
        
        print(f"WhatsApp enviado: {message.sid}")
        return True
        
    except Exception as e:
        print(f"Error al enviar WhatsApp: {e}")
        return False