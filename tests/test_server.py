import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import numpy as np
import cv2

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from msc_mcp.server import list_devices, capture_screenshot, get_device_info, install_droidcast

class TestMscMcpServer(unittest.TestCase):
    @patch('msc_mcp.server.adbutils.adb.device')
    def test_get_device_info(self, mock_device_func):
        mock_device = MagicMock()
        mock_device_func.return_value = mock_device
        mock_device.get_properties.return_value = {
            'ro.product.model': 'Pixel 4',
            'ro.build.version.sdk': '30',
            'ro.product.manufacturer': 'Google'
        }
        
        info = get_device_info("emulator-5554")
        self.assertIn("Model: Pixel 4", info)
        self.assertIn("SDK: 30", info)
        self.assertIn("Manufacturer: Google", info)

    @patch('msc_mcp.server.DroidCast')
    def test_install_droidcast(self, mock_droidcast):
        mock_instance = MagicMock()
        mock_droidcast.return_value = mock_instance
        
        result = install_droidcast("emulator-5554")
        
        mock_instance.install.assert_called_once()
        self.assertEqual(result, "DroidCast installed successfully.")

    @patch('msc_mcp.server.adbutils.adb.device_list')
    def test_list_devices(self, mock_device_list):
        # Mock device
        mock_device = MagicMock()
        mock_device.serial = "emulator-5554"
        mock_device_list.return_value = [mock_device]

        devices = list_devices()
        self.assertEqual(devices, ["emulator-5554"])

    @patch('msc_mcp.server.adbutils.adb.device_list')
    def test_list_devices_empty(self, mock_device_list):
        mock_device_list.return_value = []
        devices = list_devices()
        self.assertEqual(devices, [])

    @patch('msc_mcp.server.ADBCap')
    def test_capture_screenshot_adb(self, mock_adb_cap):
        # Mock ADBCap context manager and screencap
        mock_cap_instance = MagicMock()
        mock_adb_cap.return_value = mock_cap_instance
        mock_cap_instance.__enter__.return_value = mock_cap_instance
        
        # Create a dummy image (100x100 black image)
        dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_cap_instance.screencap.return_value = dummy_image

        result = capture_screenshot("emulator-5554", method="adb")
        
        self.assertIsNotNone(result)
        self.assertEqual(result.type, "image")
        self.assertEqual(result.mimeType, "image/png")
        self.assertTrue(len(result.data) > 0)

    @patch('msc_mcp.server.DroidCast')
    def test_capture_screenshot_droidcast(self, mock_droidcast):
        mock_cap_instance = MagicMock()
        mock_droidcast.return_value = mock_cap_instance
        mock_cap_instance.__enter__.return_value = mock_cap_instance
        
        dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_cap_instance.screencap.return_value = dummy_image

        result = capture_screenshot("emulator-5554", method="droidcast")
        
        self.assertIsNotNone(result)
        self.assertEqual(result.type, "image")

    def test_capture_screenshot_invalid_method(self):
        with self.assertRaises(RuntimeError):
            capture_screenshot("emulator-5554", method="invalid")

if __name__ == '__main__':
    unittest.main()
