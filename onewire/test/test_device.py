import unittest

from onewire import device


class TestDevice(unittest.TestCase):

    def test_spliter(self):
        result = device.spliter('foo-bar')
        self.assertEqual(result[0], 'foo')
        self.assertEqual(result[1], 'bar')
