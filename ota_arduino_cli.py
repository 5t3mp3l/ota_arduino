import subprocess
import logging

_LOGGER = logging.getLogger(__name__)

def compile_firmware(sketch_file: str):
    """Compile the Arduino sketch using Arduino CLI."""
    try:
        _LOGGER.info(f"Compiling sketch: {sketch_file}")
        
        # Use Arduino CLI to compile the sketch
        result = subprocess.run(
            ["arduino-cli", "compile", "--fqbn", "arduino:avr:uno", sketch_file],
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

def upload_firmware(sketch_file: str, port: str):
    """Upload compiled firmware using Arduino CLI."""
    try:
        _LOGGER.info(f"Uploading sketch to {port}")
        
        # Use Arduino CLI to upload the firmware
        result = subprocess.run(
            ["arduino-cli", "upload", "-p", port, "--fqbn", "arduino:avr:uno", sketch_file],
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
