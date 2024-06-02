import sys
from unittest import TestCase
from unittest.mock import patch, MagicMock
from io import StringIO


class Test(TestCase):
    def setUp(self):
        print("Real platform: " + sys.platform)

    @patch('sys.platform', new='linux')
    def test_all_in_linux_positive(self):
        method, output = self.call_it(True, True, True, None, None)
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

        method, output = self.call_it(True, True, True, 'libusb', None)
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

        method, output = self.call_it(True, True, True, 'hidapi', None)
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

    @patch('sys.platform', new='linux')
    def test_only_one_lib_linux_positive(self):
        method, output = self.call_it(False, True, True, None, None)
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

        method, output = self.call_it(False, True, True, 'hidapi', None)
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

        method, output = self.call_it(True, False, True, None, None)
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

        method, output = self.call_it(True, False, True, 'libusb', None)
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

    @patch('sys.platform', new='windows')
    def test_windows_positive(self):
        method, output = self.call_it(True, False, True, None, None)
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

        method, output = self.call_it(True, False, True, 'libusb', None)
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

    @patch('sys.platform', new='darwin')
    def test_macos_positive(self):
        method, output = self.call_it(False, True, True, None, None)
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

        method, output = self.call_it(False, True, True, 'hidapi', None)
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)


    #--------------------------------------------------------------------------


    @patch('sys.platform', new='linux')
    def test_all_in_linux_negative(self):
        method, output = self.call_it(True, True, False, None, None)
        self.assertNotIn('device initialized', output)
        self.assertIn('device is not available', output)
        self.assertIsNone(method)

        method, output = self.call_it(True, True, False, 'libusb', None)
        self.assertNotIn('device initialized', output)
        self.assertIn('device is not available', output)
        self.assertIsNone(method)

        method, output = self.call_it(True, True, False, 'hidapi', None)
        self.assertNotIn('device initialized', output)
        self.assertIn('device is not available', output)
        self.assertIsNone(method)

    @patch('sys.platform', new='linux')
    def test_all_out_linux_negative(self):
        method, output = self.call_it(False, False, False, None, None)
        self.assertNotIn('device initialized', output)
        self.assertIn('device is not available', output)
        self.assertIsNone(method)

        method, output = self.call_it(False, False, False, 'libusb', None)
        self.assertNotIn('device initialized', output)
        self.assertIn('is not possible to be used', output)
        self.assertIsNone(method)

        method, output = self.call_it(False, False, False, 'hidapi', None)
        self.assertNotIn('device initialized', output)
        self.assertIn('is not possible to be used', output)
        self.assertIsNone(method)

    @patch('sys.platform', new='windows')
    def test_windows_negative(self):
        method, output = self.call_it(True, False, True, 'hidapi', None)
        self.assertNotIn('device initialized', output)
        self.assertIn('please use method', output)
        self.assertIsNone(method)

    @patch('sys.platform', new='darwin')
    def test_macos_negative(self):
        method, output = self.call_it(False, True, True, 'libusb', None)
        self.assertNotIn('device initialized', output)
        self.assertIn('please use method', output)
        self.assertIsNone(method)


    #--------------------------------------------------------------------------


    def call_it_neg(self, pyusb_available, pyhidapi_available, device_available, method, endpoint):
        method_obj = None
        output = None
        with self.assertRaises(SystemExit):
            method_obj, output = self.call_it(pyusb_available, pyhidapi_available, device_available, method, endpoint)
        return method_obj, output

    def call_it(self, pyusb_available, pyhidapi_available, device_available, method, endpoint):
        method_obj = None
        output = None
        with self.do_import_patch(pyusb_available, pyhidapi_available, device_available) as mock:
            with patch('sys.stdout', new_callable=StringIO) as stdio_mock:
                import lednamebadge
                try:
                    method_obj = lednamebadge.LedNameBadge._find_write_method(method, endpoint)
                except(SystemExit):
                    pass
                output = stdio_mock.getvalue()
        print(output)
        self.assertEqual(pyusb_available, 'pyusb detected' in output)
        self.assertEqual(pyhidapi_available, 'pyhidapi detected' in output)
        return method_obj, output

    def do_import_patch(self, pyusb_available, pyhidapi_available, device_available):
        return patch.dict('sys.modules',
                          {
                              'pyhidapi': self.create_hid_mock(device_available) if pyhidapi_available else None,
                              'usb':      self.create_usb_mock(device_available) if pyusb_available else None,
                              'usb.core': MagicMock() if pyusb_available else None})

    def create_hid_mock(self, device_available):
        device = MagicMock()
        device.path = 'devicepath'

        mock = MagicMock()
        mock.hid_enumerate.return_value = [device] if device_available else None
        mock.hid_open_path.return_value = 'device' if device_available else None
        return mock

    def create_usb_mock(self, device_available):
        mock = MagicMock()
        mock.core = MagicMock()
        mock.core.find.return_value = 'device' if device_available else None
        return mock
