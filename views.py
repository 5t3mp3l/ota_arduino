from aiohttp import web

async def async_register_view(hass):
    """Register the OTA Arduino view for frontend interactions"""
    hass.http.register_view(
        web.View('/api/ota_arduino', MyArduinoView)
    )
