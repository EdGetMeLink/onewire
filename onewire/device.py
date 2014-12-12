from os.path import join, split
import glob
import logging
LOG = logging.getLogger(__name__)


def spliter(path):
    '''
    return onewire device id an devie type from a given path name
    :param path: the full path name
    :return: returns device_type, device_id
    '''
    folder, device = split(path)
    return device.split('-')


class Onewire(object):
    '''
    Main Class for Onewire devices
    '''
    def __init__(self, base_dir=None):
        self.device_list = []
        self.base_dir = base_dir

    def load_device(self, base_dir=None):
        '''
        load all devices
        '''
        if base_dir:
            self.base_dir = base_dir
        else:
            if not self.base_dir:
                raise ValueError('base path name not set.')
        for device_path in glob.glob(join(self.base_dir, '*')):
            try:
                _device_type, _device_id = spliter(device_path)
                _device_file = join(device_path, 'w1_slave')
                if FAMILY.get(_device_type):
                    _device = FAMILY[_device_type](
                        device_id=_device_id,
                        device_file=_device_file)
                    self.device_list.append(_device)
            except ValueError:
                LOG.exception(u'Value Error')

    def find_by_name(self, name):
        '''
        find a device by a given name
        if no device is found return None
        '''
        if not name:
            raise ValueError('no valid name given')
        for device in self.device_list:
            if device.name == name:
                return device
        return None

    def find_by_id(self, id):
        '''
        find device by id
        return device or None if not found
        '''
        if not id:
            raise ValueError('no id given')
        for device in self.device_list:
            if device.device_id == id:
                return device
        return None


class Device(object):
    '''
    master device class containing methods valid for all devices
    '''

    def __init__(self, *args, **kwargs):
        self.device_id = kwargs.get('device_id', None)
        self.device_file = kwargs.get('device_file', None)
        self.name = None


class DS1820(Device):
    '''
    DS1820 Digital Thermometer class
    '''
    def __init__(self, unit='C', *args, **kwargs):
        super(DS1820, self).__init__(*args, **kwargs)
        LOG.debug(u'initialising class DS1820')
        self.unit = unit

    def read(self):
        '''
        read temperature data
        '''
        if not self.device_file:
            LOG.debug(u'no device file specified')
            raise ValueError('no device file specified')
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close
        if 'YES' not in lines[0]:
            LOG.debug(u'no valide in device file')
            raise ValueError(u'no valid data in device file')
        tloc = lines[1].find('t=')
        if tloc != -1:
            temp_string = lines[1][tloc + 2:]
            if self.unit == 'C':
                '''
                return celsius value
                '''
                return float(temp_string) / 1000
            if self.unit == 'F':
                '''
                return fahrenheit value
                '''
                return float(temp_string) / 1000 * 9 / 5 + 32


'''
Family code reference
1wire devices show up in system with a name containing a family code
'''
FAMILY = {
    '10': 'DS1920',  # Temperature with alarm trips
    '20': 'DS2450',  # 4-channel A/D converter ADC
    '21': 'DS1921',  # Thermochron temperature logger
    '24': 'DS1904',  # Real-time clock RTC
    '27': 'DS2417',  # RTC with interrupt
    '28': DS1820,  # Digital Thermometer
}
