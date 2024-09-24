import pytest
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web
from ota_arduino.api import handle_upload_firmware, handle_compile_firmware

class TestOtaArduinoAPI(AioHTTPTestCase):
    async def get_application(self):
        """Set up the test application."""
        app = web.Application()
        app.router.add_post('/api/ota_arduino/upload_firmware', handle_upload_firmware)
        app.router.add_post('/api/ota_arduino/compile_firmware', handle_compile_firmware)
        return app

    @unittest_run_loop
    async def test_upload_firmware(self):
        """Test firmware upload API."""
        resp = await self.client.post('/api/ota_arduino/upload_firmware', data={
            'firmware': 'test.hex',
            'device': '/dev/ttyUSB0',
            'board': 'arduino:avr:uno'
        })
        assert resp.status == 200
        result = await resp.json()
        assert 'message' in result
        assert 'successfully' in result['message']

    @unittest_run_loop
    async def test_upload_firmware_missing_data(self):
        """Test upload firmware with missing data."""
        resp = await self.client.post('/api/ota_arduino/upload_firmware', data={
            'device': '/dev/ttyUSB0'
        })
        assert resp.status == 400
        result = await resp.json()
        assert 'message' in result
        assert 'Firmware file, board, or device not provided' in result['message']

    @unittest_run_loop
    async def test_compile_firmware(self):
        """Test firmware compile API."""
        resp = await self.client.post('/api/ota_arduino/compile_firmware', json={
            'sketch_file': 'test.ino',
            'board': 'arduino:avr:uno'
        })
        assert resp.status == 200
        result = await resp.json()
        assert 'message' in result
        assert 'Compilation successful' in result['message']

    @unittest_run_loop
    async def test_compile_firmware_missing_data(self):
        """Test compile firmware with missing data."""
        resp = await self.client.post('/api/ota_arduino/compile_firmware', json={
            'board': 'arduino:avr:uno'
        })
        assert resp.status == 400
        result = await resp.json()
        assert 'message' in result
        assert 'Sketch file or board not provided' in result['message']
