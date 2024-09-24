import subprocess
import logging
from .helpers import check_arduino_cli_installed

_LOGGER = logging.getLogger(__name__)

def compile_firmware(sketch_file: str, board: str):
    """Compile the Arduino sketch using Arduino CLI."""
    if not check_arduino_cli_installed():
        return False, "Arduino CLI is not installed."

    try:
        _LOGGER.info(f"Compiling sketch: {sketch_file} for board: {board}")
        
        # Use Arduino CLI to compile the sketch
        result = subprocess.run(
            ["arduino-cli", "compile", "--fqbn", board, sketch_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            _LOGGER.error(f"Compilation error: {result.stderr}")
            return False, result.stderr
        _LOGGER.info(f"Compilation successful: {result.stdout}")
        return True, result.stdout
    except Exception as e:
        _LOGGER.error(f"Error compiling firmware: {e}")
        return False, str(e)

def upload_firmware(firmware_file: str, device: str, board: str):
    """Upload compiled firmware using Arduino CLI."""
    if not check_arduino_cli_installed():
        return False, "Arduino CLI is not installed."

    try:
        _LOGGER.info(f"Uploading firmware {firmware_file} to device {device}")
        
        # Use Arduino CLI to upload the firmware
        result = subprocess.run(
            ["arduino-cli", "upload", "-p", device, "--fqbn", board, firmware_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            _LOGGER.error(f"Upload error: {result.stderr}")
            return False, result.stderr
        _LOGGER.info(f"Upload successful: {result.stdout}")
        return True, result.stdout
    except Exception as e:
        _LOGGER.error(f"Error uploading firmware: {e}")
        return False, str(e)
