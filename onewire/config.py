'''
Config.py
=========
'''
from config_resolver import Config
import logging


LOG = logging.getLogger(__name__)


def load_cfg():
    '''
    return config
    '''
    config = Config('mds', 'onewire')
    return config
