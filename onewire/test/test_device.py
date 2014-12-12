from textwrap import dedent
import unittest

from mock import patch, MagicMock

from onewire import device


class TestUtils(unittest.TestCase):

    def test_spliter(self):
        result = device.spliter('foo-bar')
        self.assertEqual(result[0], 'foo')
        self.assertEqual(result[1], 'bar')


class TestOnewire(unittest.TestCase):

    def setUp(self):
        self.__ow = device.Onewire('/the/base/dir')

    @patch('onewire.device.glob')
    def test_load_device(self, globmock):
        globmock.return_value = [
            '28-00044a6834ff',
            '28-00044ce89bff',
            '28-00044cf537ff',
            '28-00044ef540ff',
            '28-0014128e65ff',
            '28-001412f2aeff',
            'w1_bus_master1',
        ]
        self.__ow.load_device()
        self.assertItemsEqual(
            [(_.device_file, _.device_id) for _ in self.__ow.device_list],
            [
                ('28-00044a6834ff/w1_slave', '00044a6834ff'),
                ('28-00044ce89bff/w1_slave', '00044ce89bff'),
                ('28-00044cf537ff/w1_slave', '00044cf537ff'),
                ('28-00044ef540ff/w1_slave', '00044ef540ff'),
                ('28-0014128e65ff/w1_slave', '0014128e65ff'),
                ('28-001412f2aeff/w1_slave', '001412f2aeff'),
            ]
        )

    @patch('onewire.device.glob')
    def test_find_by_name_none(self, globmock):
        globmock.return_value = [
            '28-00044a6834ff',
            '28-00044ce89bff',
        ]
        self.__ow.load_device()
        result = self.__ow.find_by_name('foo')
        self.assertIsNone(result)

    @unittest.skip('Could not figure out the API from the code')
    @patch('onewire.device.glob')
    def test_find_by_name(self, globmock):
        globmock.return_value = [
            '28-00044a6834ff',
            '28-00044ce89bff',
        ]
        self.__ow.load_device()
        result = self.__ow.find_by_name('foo')
        self.assertIsNone(result)

    @patch('onewire.device.glob')
    def test_find_by_id_none(self, globmock):
        globmock.return_value = [
            '28-00044a6834ff',
            '28-00044ce89bff',
        ]
        self.__ow.load_device()
        result = self.__ow.find_by_id('foo')
        self.assertIsNone(result)

    @patch('onewire.device.glob')
    def test_find_by_id(self, globmock):
        globmock.return_value = [
            '28-00044a6834ff',
            '28-00044ce89bff',
        ]
        self.__ow.load_device()
        result = self.__ow.find_by_id('00044ce89bff')
        self.assertEqual(result.device_id, '00044ce89bff')
        self.assertEqual(result.device_file, '28-00044ce89bff/w1_slave')


class TestDevice(unittest.TestCase):

    def test_device(self):
        dev = device.Device(device_id=123, device_file=234)
        self.assertEqual(dev.device_id, 123)
        self.assertEqual(dev.device_file, 234)


class TestDS1820(unittest.TestCase):

    @patch('onewire.device.open', create=True)
    def test_read_c(self, mock_open):
        obj = device.DS1820(device_id='foo', device_file='bar')
        mocked_file = MagicMock(spec=file)
        mock_open.return_value = mocked_file
        mocked_file.readlines.return_value = [
            '7f 01 55 00 7f ff 0c 10 87 : crc=87 YES',
            '7f 01 55 00 7f ff 0c 10 87 t=23937',
        ]
        result = obj.read()
        self.assertAlmostEqual(result, 23.937)

    @patch('onewire.device.open', create=True)
    def test_read_f(self, mock_open):
        obj = device.DS1820('F', device_id='foo', device_file='bar')
        mocked_file = MagicMock(spec=file)
        mock_open.return_value = mocked_file
        mocked_file.readlines.return_value = [
            '7f 01 55 00 7f ff 0c 10 87 : crc=87 YES',
            '7f 01 55 00 7f ff 0c 10 87 t=23937',
        ]
        result = obj.read()
        self.assertAlmostEqual(result, 75.0866)
