from .helpers import check_arduino_cli_installed, install_arduino_cli
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Setup OTA Arduino integration."""
    if not check_arduino_cli_installed():
        install_arduino_cli()
    setup_api_routes(hass)
    _LOGGER.info("OTA Arduino integration setup completed.")
    return True
