from aiohttp import web

async def async_register_view(hass):
    """Register the OTA Arduino view for frontend interactions."""
    hass.http.register_view(
        web.View('/api/ota_arduino', MyArduinoView)
    )

async def handle_log_stream(request):
    """Handle log streaming request."""
    log_file = "/path/to/log_file.log"
    
    if not os.path.exists(log_file):
        return web.json_response({"message": "Log file not found."}, status=404)

    with open(log_file, "r") as file:
        logs = file.read()

    return web.json_response({"logs": logs}, status=200)
