from onewire.device import Onewire
from onewire.config import load_cfg
import time

if __name__ == '__main__':
    cfg = load_cfg()
    base_dir = cfg.get('general', 'base_dir')
    onewire = Onewire(base_dir=base_dir)
    onewire.load_device()
    while True:
        for i in onewire.device_list:
            print i.name, i.device_id, i.read()
        time.sleep(1)
