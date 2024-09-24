import os
import logging
import subprocess

_LOGGER = logging.getLogger(__name__)

# Check if Arduino CLI is installed
def check_arduino_cli_installed():
    """Check if Arduino CLI is installed, and install if not."""
    try:
        result = subprocess.run(["arduino-cli", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            _LOGGER.info(f"Arduino CLI is already installed: {result.stdout}")
            return True
        else:
            _LOGGER.error(f"Arduino CLI check failed: {result.stderr}")
            return False
    except FileNotFoundError:
        _LOGGER.warning("Arduino CLI not found, installing...")
        return install_arduino_cli()


def install_arduino_cli():
    """Install Arduino CLI."""
    try:
        # Download and install Arduino CLI
        download_url = "https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Linux_64bit.tar.gz"
        install_dir = "/usr/local/bin"

        subprocess.run(["wget", download_url, "-O", "/tmp/arduino-cli.tar.gz"], check=True)
        subprocess.run(["tar", "-xvf", "/tmp/arduino-cli.tar.gz", "-C", "/tmp/"], check=True)
        subprocess.run(["mv", "/tmp/arduino-cli", f"{install_dir}/arduino-cli"], check=True)

        _LOGGER.info("Arduino CLI installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        _LOGGER.error(f"Failed to install Arduino CLI: {e}")
        return False
    
def validate_firmware(file: str) -> bool:
    """Validate the firmware file extension (hex or bin)."""
    return file.endswith(".hex") or file.endswith(".bin")

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

def report_error(message: str, context: str = "General"):
    """Log and report an error."""
    error_msg = f"Error in {context}: {message}"
    _LOGGER.error(error_msg)
    # Optionally, you can trigger an event in Home Assistant to notify the user
    # hass.bus.fire('ota_arduino_error', {"message": error_msg})