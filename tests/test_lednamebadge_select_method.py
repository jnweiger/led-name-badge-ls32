import sys
from unittest import TestCase
from unittest.mock import patch, MagicMock
from io import StringIO


class USBError(BaseException):
    pass


class Test(TestCase):
    def setUp(self):
        print("Real platform: " + sys.platform)

    @patch('sys.platform', new='linux')
    def test_list(self):
        method, output = self.call_find(True, True, True, 'list', 'auto')
        self.assertIn("Available write methods:", output)
        self.assertIn("'auto'", output)
        self.assertIn("'hidapi'", output)
        self.assertIn("'libusb'", output)

        method, output = self.call_find(True, True, True, 'hidapi', 'list')
        self.assertIn("Known device ids with method 'hidapi' are:", output)
        self.assertIn("'3-4:5-6': HidApi Test", output)

        method, output = self.call_find(True, True, True, 'libusb', 'list')
        self.assertIn("Known device ids with method 'libusb' are:", output)
        self.assertIn("'3:4:2': LibUsb Test", output)

    @patch('sys.platform', new='linux')
    def test_unknown(self):
        method, output = self.call_find(True, True, True, 'hello', 'auto')
        self.assertIn("Unknown write method 'hello'", output)
        self.assertIn("Available write methods:", output)

    @patch('sys.platform', new='linux')
    def test_all_in_linux_positive(self):
        method, output = self.call_find(True, True, True, 'auto', 'auto')
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

        method, output = self.call_find(True, True, True, 'libusb', 'auto')
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

        method, output = self.call_find(True, True, True, 'hidapi', 'auto')
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

    @patch('sys.platform', new='linux')
    def test_only_one_lib_linux_positive(self):
        method, output = self.call_find(False, True, True, 'auto', 'auto')
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

        method, output = self.call_find(False, True, True, 'hidapi', 'auto')
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

        method, output = self.call_find(True, False, True, 'auto', 'auto')
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

        method, output = self.call_find(True, False, True, 'libusb', 'auto')
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

    @patch('sys.platform', new='windows')
    def test_windows_positive(self):
        method, output = self.call_find(True, False, True, 'auto', 'auto')
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

        method, output = self.call_find(True, False, True, 'libusb', 'auto')
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

    @patch('sys.platform', new='darwin')
    def test_macos_positive(self):
        method, output = self.call_find(False, True, True, 'auto', 'auto')
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

        method, output = self.call_find(False, True, True, 'hidapi', 'auto')
        self.assertIn('device initialized', output)
        self.assertIsNotNone(method)

    @patch('sys.version_info', new=[2])
    def test_python2_positive(self):
        method, output = self.call_find(True, True, True, 'auto', 'auto')
        self.assertIn('device initialized', output)
        self.assertIn('Preferring method libusb', output)
        self.assertIsNotNone(method)


    # -------------------------------------------------------------------------


    @patch('sys.platform', new='linux')
    def test_all_in_linux_negative(self):
        method, output = self.call_find(True, True, False, 'auto', 'auto')
        self.assertNotIn('device initialized', output)
        self.assertIn('device is not available', output)
        self.assertIsNone(method)

        method, output = self.call_find(True, True, False, 'libusb', 'auto')
        self.assertNotIn('device initialized', output)
        self.assertIn('device is not available', output)
        self.assertIsNone(method)

        method, output = self.call_find(True, True, False, 'hidapi', 'auto')
        self.assertNotIn('device initialized', output)
        self.assertIn('device is not available', output)
        self.assertIsNone(method)

    @patch('sys.platform', new='linux')
    def test_all_out_linux_negative(self):
        method, output = self.call_find(False, False, False, 'auto', 'auto')
        self.assertNotIn('device initialized', output)
        self.assertIn('One of the python packages', output)
        self.assertIsNone(method)

        method, output = self.call_find(False, False, False, 'libusb', 'auto')
        self.assertNotIn('device initialized', output)
        self.assertIn('is not possible to be used', output)
        self.assertIsNone(method)

        method, output = self.call_find(False, False, False, 'hidapi', 'auto')
        self.assertNotIn('device initialized', output)
        self.assertIn('is not possible to be used', output)
        self.assertIsNone(method)

    @patch('sys.platform', new='windows')
    def test_windows_negative(self):
        method, output = self.call_find(True, False, True, 'hidapi', 'auto')
        self.assertNotIn('device initialized', output)
        self.assertIn('please use method', output)
        self.assertIsNone(method)

    @patch('sys.platform', new='darwin')
    def test_macos_negative(self):
        method, output = self.call_find(False, True, True, 'libusb', 'auto')
        self.assertNotIn('device initialized', output)
        self.assertIn('please use method', output)
        self.assertIsNone(method)

    @patch('sys.version_info', new=[2])
    def test_python2_negative(self):
        method, output = self.call_find(True, True, True, 'hidapi', 'auto')
        self.assertNotIn('device initialized', output)
        self.assertIn('Please use method', output)
        self.assertIsNone(method)


    # -------------------------------------------------------------------------


    def test_get_methods(self):
        methods, output = self.call_info_methods()
        self.assertDictEqual({
                                 'hidapi': True,
                                 'libusb': True}, methods)

    def test_get_device_ids(self):
        device_ids, output = self.call_info_ids('libusb')
        self.assertDictEqual({
                                 '3:4:2': 'LibUsb Test Manufacturer - LibUsb Test Product (bus=3 dev=4 endpoint=2)'},
                             device_ids)

        device_ids, output = self.call_info_ids('hidapi')
        self.assertDictEqual({
                                 '3-4:5-6': 'HidApi Test Manufacturer - HidApi Test Product (if=0)'},
                             device_ids)


    # -------------------------------------------------------------------------


    def call_find(self, pyusb_available, pyhidapi_available, device_available, method, device_id):
        self.print_test_conditions(pyusb_available, pyhidapi_available, device_available, method, device_id)
        method_obj, output = self.prepare_modules(pyusb_available, pyhidapi_available, device_available,
                                                  lambda m: m._find_write_method(method, device_id))
        self.assertEqual(pyusb_available, 'usb.core detected' in output)
        self.assertEqual(pyhidapi_available, 'pyhidapi detected' in output)
        return method_obj, output

    def call_info_methods(self):
        self.print_test_conditions(True, True, True, '-', '-')
        return self.prepare_modules(True, True, True,
                                    lambda m: m.get_available_methods())

    def call_info_ids(self, method):
        self.print_test_conditions(True, True, True, '-', '-')
        return self.prepare_modules(True, True, True,
                                    lambda m: m.get_available_device_ids(method))

    def prepare_modules(self, pyusb_available, pyhidapi_available, device_available, func):
        result = None
        output = None
        with self.do_import_patch(pyusb_available, pyhidapi_available, device_available) as mock:
            with patch('sys.stdout', new_callable=StringIO) as stdio_mock:
                import lednamebadge
                try:
                    result = func(lednamebadge.LedNameBadge)
                except(SystemExit):
                    pass
                output = stdio_mock.getvalue()
        print(output)
        return result, output

    def print_test_conditions(self, pyusb_available, pyhidapi_available, device_available, method, device_id):
        print("Test condition: os=%s  pyusb=%s  pyhidapi=%s  device=%s  method=%s  device_id=%s" % (
            sys.platform,
            'yes' if pyusb_available else 'no',
            'yes' if pyhidapi_available else 'no',
            'yes' if device_available else 'no',
            method,
            device_id))

    def do_import_patch(self, pyusb_available, pyhidapi_available, device_available):
        patch_obj = patch.dict('sys.modules', {
            'pyhidapi':          self.create_hid_mock(device_available) if pyhidapi_available else None,
            'usb':               self.create_usb_mock(device_available) if pyusb_available else None,
            'usb.core':          MagicMock() if pyusb_available else None,
            'usb.core.USBError': USBError if pyusb_available else None,
            'usb.util':          MagicMock() if pyusb_available else None})
        # Assure fresh reimport of lednamebadge with current mocks
        if 'lednamebadge' in sys.modules:
            del sys.modules['lednamebadge']
        return patch_obj


    def create_hid_mock(self, device_available):
        device = MagicMock()
        device.path = b'3-4:5-6'
        device.manufacturer_string = 'HidApi Test Manufacturer'
        device.product_string = 'HidApi Test Product'
        device.interface_number = 0

        mock = MagicMock()
        mock.hid_enumerate.return_value = [device] if device_available else []
        mock.hid_open_path.return_value = 123456 if device_available else []
        return mock


    def create_usb_mock(self, device_available):
        device = MagicMock()
        device.manufacturer = 'LibUsb Test Manufacturer'
        device.product = 'LibUsb Test Product'
        device.bus = 3
        device.address = 4

        ep = MagicMock()
        ep.bEndpointAddress = 2

        mock = MagicMock()
        mock.core = MagicMock()
        mock.core.find.return_value = [device] if device_available else []
        mock.core.USBError = USBError
        mock.util.find_descriptor.return_value = [ep] if device_available else []
        return mock
