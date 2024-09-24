import logging
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.service import ServiceResponseError
from .ota_arduino_cli import compile_firmware, upload_firmware
from .helpers import report_error

_LOGGER = logging.getLogger(__name__)

async def handle_upload_firmware(call: ServiceCall):
    """Service to handle OTA firmware uploads."""
    try:
        firmware_file = call.data.get("firmware_file")
        target_device = call.data.get("device")
        board = call.data.get("board")

        if not firmware_file or not target_device or not board:
            raise ServiceResponseError("Firmware file, device, or board not specified")

        _LOGGER.info(f"Uploading firmware {firmware_file} to device {target_device}")
        success, message = upload_firmware(firmware_file, target_device, board)
        if not success:
            report_error(message, "Firmware Upload")
    except Exception as e:
        report_error(f"Error during firmware upload: {e}")

async def handle_compile_firmware(call: ServiceCall):
    """Service to handle firmware compilation."""
    try:
        sketch_file = call.data.get("sketch_file")
        board = call.data.get("board")
        
        if not sketch_file or not board:
            raise ServiceResponseError("Sketch file or board not provided for compilation")

        _LOGGER.info(f"Compiling firmware for {sketch_file} on board {board}")
        success, message = compile_firmware(sketch_file, board)
        if not success:
            report_error(message, "Firmware Compilation")
    except Exception as e:
        report_error(f"Error during firmware compilation: {e}")

async def handle_log_stream(call: ServiceCall):
    """Service to stream OTA/compilation logs."""
    try:
        # Stream logs from the compilation or OTA process
        _LOGGER.info("Streaming logs...")
        # Fetch logs from some log file or source
    except Exception as e:
        report_error(f"Error while streaming logs: {e}")
