def validate_firmware_file(file_path: str) -> bool:
    """Validate the firmware file before uploading."""
    if not file_path.endswith('.bin'):
        return False
    return True

def validate_sketch_file(file_path: str) -> bool:
    """Validate the Arduino sketch file before compiling."""
    if not file_path.endswith('.ino'):
        return False
    return True
