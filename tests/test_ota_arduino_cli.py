import pytest
from unittest.mock import patch
from ota_arduino.ota_arduino_cli import compile_firmware, upload_firmware

@patch('ota_arduino.ota_arduino_cli.ArduinoCLI')
def test_compile_firmware(mock_arduino_cli):
    # Mock a successful compile
    mock_arduino_cli().compile.return_value.success = True
    mock_arduino_cli().compile.return_value.output = "Compilation successful"

    success, output = compile_firmware("test_sketch.ino")
    
    assert success
    assert output == "Compilation successful"

@patch('ota_arduino.ota_arduino_cli.ArduinoCLI')
def test_upload_firmware(mock_arduino_cli):
    # Mock a successful upload
    mock_arduino_cli().upload.return_value.success = True
    mock_arduino_cli().upload.return_value.output = "Upload successful"

    success, output = upload_firmware("test_sketch.ino", "/dev/ttyUSB0")
    
    assert success
    assert output == "Upload successful"
