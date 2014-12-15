from pkg_resources import resource_string

__version__ = resource_string('onewire', 'version.txt').strip().decode('ascii')
