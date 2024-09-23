import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers import service

from .api import setup_api_routes

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the OTA Arduino integration."""
    
    _LOGGER.info("Setting up OTA Arduino")
    
    # Set the initial state of the integration in Home Assistant
    hass.states.async_set("ota_arduino.status", "Integration loaded")
    
    # Register custom services for OTA firmware, compiling, and log streaming
    await setup_services(hass)
    
    # Setup the API routes (if you have API endpoints for OTA handling, compiling, and logs)
    setup_api_routes(hass)

    return True

async def setup_services(hass: HomeAssistant):
    """Register custom services for OTA Arduino."""
    
    # Register the 'upload_firmware' service
    hass.services.async_register("ota_arduino", "upload_firmware", handle_upload_firmware)
    
    # Register the 'compile_firmware' service
    hass.services.async_register("ota_arduino", "compile_firmware", handle_compile_firmware)
    
    # Register the 'log_stream' service for streaming logs
    hass.services.async_register("ota_arduino", "log_stream", handle_log_stream)

