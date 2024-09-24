import unittest
from ota_arduino.ota_arduino_cli import check_arduino_cli_installed

class TestArduinoCLI(unittest.TestCase):

    def test_check_arduino_cli_installed(self):
        """Test if Arduino CLI is installed."""
        result = check_arduino_cli_installed()
        self.assertIsInstance(result, bool)

if __name__ == '__main__':
    unittest.main()