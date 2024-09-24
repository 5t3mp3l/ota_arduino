from aiohttp import web
from .ota_arduino_cli import compile_firmware, upload_firmware
from .helpers import get_firmware_logs

async def handle_upload_firmware(request):
    """Handle OTA firmware upload request."""
    data = await request.post()
    firmware_file = data.get('firmware')
    device = data.get('device')
    board = data.get('board')

    if not firmware_file or not device or not board:
        return web.json_response({'message': 'Firmware file, device, or board not provided'}, status=400)

    # Call function to upload firmware using the OTA logic
    success, message = upload_firmware(firmware_file, device, board)
    status = 200 if success else 500
    return web.json_response({'message': message}, status=status)

async def handle_compile_firmware(request):
    """Handle firmware compilation request."""
    data = await request.json()
    sketch_file = data.get('sketch_file')
    board = data.get('board')

    if not sketch_file or not board:
        return web.json_response({'message': 'Sketch file or board not provided'}, status=400)

    # Call function to compile the sketch using Arduino CLI
    success, message = compile_firmware(sketch_file, board)
    status = 200 if success else 500
    return web.json_response({'message': message}, status=status)

async def handle_log_stream(request):
    """Stream OTA/compilation logs."""
    logs = get_firmware_logs("/path/to/log_file.log")
    return web.json_response({'logs': logs}, status=200)

async def handle_board_list(request):
    """Fetch and return available boards via Arduino CLI."""
    # Assume the function `list_boards` fetches boards from Arduino CLI
    boards = ["arduino:avr:uno", "arduino:samd:mkrwifi1010"]  # Example
    return web.json_response(boards, status=200)

def setup_api_routes(hass):
    """Register the API routes for OTA Arduino."""
    hass.http.register_view(OtaArduinoView)

class OtaArduinoView(web.View):
    """Handle OTA Arduino API requests."""

    async def post(self):
        if self.path == "/api/ota_arduino/upload_firmware":
            return await handle_upload_firmware(self.request)
        elif self.path == "/api/ota_arduino/compile_firmware":
            return await handle_compile_firmware(self.request)
        elif self.path == "/api/ota_arduino/logs":
            return await handle_log_stream(self.request)
        elif self.path == "/api/ota_arduino/boards":
            return await handle_board_list(self.request)
        else:
            return web.json_response({'message': 'Invalid endpoint'}, status=404)
