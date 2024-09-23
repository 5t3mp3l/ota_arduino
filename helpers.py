import os
import logging
import subprocess

_LOGGER = logging.getLogger(__name__)

# Validate firmware file format
def validate_firmware(file: str) -> bool:
    """Validate the firmware file extension (hex or bin)."""
    return file.endswith(".hex") or file.endswith(".bin")


# Flash firmware using Arduino CLI
def flash_firmware(file_path: str) -> str:
    """Handle the logic for flashing firmware via Arduino CLI."""
    try:
        result = subprocess.run(
            ["arduino-cli", "upload", "-p", "/dev/ttyUSB0", "--fqbn", "arduino:avr:uno", file_path],
            check=True, text=True, capture_output=True
        )
        _LOGGER.info(f"Firmware upload successful: {result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        _LOGGER.error(f"Flashing failed: {e}")
        raise RuntimeError(f"Flashing failed: {e}")


# Save firmware file to the provided path
def save_firmware_file(upload_path: str, firmware_data: bytes) -> tuple:
    """Save the uploaded firmware file to the specified path."""
    try:
        with open(upload_path, 'wb') as f:
            f.write(firmware_data)
        _LOGGER.info(f"Firmware file saved at {upload_path}")
        return True, upload_path
    except Exception as e:
        _LOGGER.error(f"Error saving firmware file: {e}")
        return False, str(e)


# Validate sketch file existence
def validate_sketch_file(sketch_file: str) -> bool:
    """Validate that the sketch file exists."""
    if not os.path.isfile(sketch_file):
        _LOGGER.error(f"Sketch file not found: {sketch_file}")
        return False
    _LOGGER.info(f"Sketch file validated: {sketch_file}")
    return True


# Validate the device port used for firmware upload
def validate_device_port(device_port: str) -> bool:
    """Validate the device port for uploading firmware."""
    if not device_port.startswith('/dev/'):
        _LOGGER.error(f"Invalid device port: {device_port}")
        return False
    _LOGGER.info(f"Device port validated: {device_port}")
    return True


# Read firmware logs from a file
def get_firmware_logs(log_file_path: str) -> str:
    """Read and return the firmware compilation/upload logs."""
    try:
        with open(log_file_path, 'r') as log_file:
            logs = log_file.read()
        return logs
    except FileNotFoundError:
        _LOGGER.error(f"Log file not found: {log_file_path}")
        return "No logs available."
    except Exception as e:
        _LOGGER.error(f"Error reading log file: {e}")
        return str(e)
