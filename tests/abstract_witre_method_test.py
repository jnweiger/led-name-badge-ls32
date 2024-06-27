import sys
from unittest import TestCase
from unittest.mock import patch, MagicMock
from io import StringIO


class USBError(BaseException):
    pass


class AbstractWriteMethodTest(TestCase):
    def setUp(self):
        print("Real platform: " + sys.platform)


    # -------------------------------------------------------------------------


    def print_test_conditions(self, pyusb_available, pyhidapi_available, device_available, method, device_id):
        print("Test condition: os=%s  pyusb=%s  pyhidapi=%s  device=%s  method=%s  device_id=%s" % (
            sys.platform,
            'yes' if pyusb_available else 'no',
            'yes' if pyhidapi_available else 'no',
            'yes' if device_available else 'no',
            method,
            device_id))

    def prepare_modules(self, pyusb_available, pyhidapi_available, device_available, func):
        result = None
        output = None
        mocks = None
        with self.do_import_patch(pyusb_available, pyhidapi_available, device_available) as module_mocks:
            with patch('sys.stdout', new_callable=StringIO) as stdio_mock:
                import lednamebadge
                try:
                    result = func(lednamebadge.LedNameBadge)
                    mocks = {'pyhidapi': module_mocks['pyhidapi'], 'usb': module_mocks['usb']}
                except(SystemExit):
                    pass
                output = stdio_mock.getvalue()
        print(output)
        return result, output, mocks

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
