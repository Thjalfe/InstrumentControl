from setuptools import setup

setup(
    name='InstrumentControl',
    url='https://github.com/Thjalfe/InstrumentControl',
    packages=['InstrumentControl'],
    install_requires=['pyvisa==1.12.0', 'pythonnet==3.0.1', 'pyserial==3.5', 'numpy>=1.23.3', 'pyserial==3.5', 'ThorlabsPM100==1.2.2', 'pyusb==1.2.1', 'pywin32==304'],
    version='0.1.0',
)
