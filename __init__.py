import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers import service

from .api import setup_api_routes

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the OTA Arduino integration."""

    _LOGGER.info("Setting up OTA Arduino")
    
    # Set up custom services
    await setup_services(hass)
    hass.states.async_set("ota_arduino.status", "Integration loaded")
    # Setup the API routes for handling OTA, compilation, logs
    setup_api_routes(hass)

    return True

async def setup_services(hass: HomeAssistant):
    """Register custom services."""
    hass.services.async_register("ota_arduino", "upload_firmware", handle_upload_firmware)
    hass.services.async_register("ota_arduino", "compile_firmware", handle_compile_firmware)
    hass.services.async_register("ota_arduino", "log_stream", handle_log_stream)


async def async_setup(hass, config):
    """Set up the OTA Arduino component."""
    hass.states.async_set("ota_arduino.status", "Integration loaded")
    hass.services.async_register('ota_arduino', 'upload_firmware', handle_upload_firmware)
    return True
