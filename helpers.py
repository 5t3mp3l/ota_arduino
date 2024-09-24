from pyduinocli import ArduinoCLI

arduino_cli = ArduinoCLI()

def flash_firmware(file_path: str) -> str:
    """Flash the firmware using pyduinocli."""
    try:
        result = arduino_cli.upload(sketch=file_path, port="/dev/ttyUSB0", fqbn="arduino:avr:uno")
        
        if result.success:
            _LOGGER.info(f"Firmware upload successful: {result.output}")
            return result.output
        else:
            _LOGGER.error(f"Flashing failed: {result.error}")
            raise RuntimeError(f"Flashing failed: {result.error}")
    except Exception as e:
        _LOGGER.error(f"Error during flashing: {e}")
        raise RuntimeError(f"Error during flashing: {e}")
