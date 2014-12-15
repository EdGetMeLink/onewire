from setuptools import setup, find_packages
from os.path import join, dirname
PACKAGE = 'onewire'

with open(join(PACKAGE, 'version.txt')) as fptr:
    VERSION = fptr.read().strip()

setup(
    author='Mike Deltgen',
    author_email='mike@deltgen.net',
    name='onewire',
    version=VERSION,
    description='One Wire package',
    url='www.deltgen.net',
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    include_package_data=True,
    license="Private",
    install_requires=[
        'config-resolver >= 4.2.2, <5.0',
    ],
    packages=find_packages(exclude=["tests.*", "tests"]),
)
