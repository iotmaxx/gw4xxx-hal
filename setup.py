from setuptools import setup, find_packages

version = {}
with open("gw4xxx_hal/version.py") as fp:
    exec(fp.read(), version)

setup(
    name='gw4xxx-hal',
    version=version['__version__'],
    url='https://github.com/iotmaxx/gw4xxx-hal',
    author='Ralf Glaser',
    author_email='glaser@iotmaxx.de',
    description='IoTmaxx gateway series hardware abstraction layer',
    packages=find_packages(),    
    install_requires=[],
)
