from smbus2 import SMBus, i2c_msg
import time

i2c_bus = 3
i2c_MCP4728_addresses = [ 0x65, 0x66, 0x67, 0x64 ]
i2c_ADS1015_address = 0x48

def check_valid_chip_channel(func):
    def inner(chip, channel, *args, **kwargs):
        if chip >= len(i2c_MCP4728_addresses):
           raise IndexError
        if channel >= 4:
           raise IndexError
        return func(chip, channel, *args, **kwargs)
    return inner

def _get_flags(high_byte):
    theFlags = {}
    theFlags["vref"] = (high_byte & 1 << 7) > 0
    theFlags["gain"] = (high_byte & 1 << 4) > 0
    theFlags["power_state"] = (high_byte & 0b011 << 5) >> 5
    return theFlags

def _chunk(big_list, chunk_size):
    """Divides a given list into `chunk_size` sized chunks"""
    for i in range(0, len(big_list), chunk_size):
        yield big_list[i : i + chunk_size]

# set output voltage on analog output channels
# Mapping:
# chip# | channels [0:3]
#   0   | [00:03]
#   1   | [IO0,IO1,12,13]
#   2   | [30:33]
#   3   | [40:43]
@check_valid_chip_channel
def setVoltage(chip, channel, voltage):
    voltage = int(voltage*1000)
    voltage = int(voltage/8)
    # [7]:    1     Internal Vref (2.048V)
    # [6:5]: 00     no power down
    # [4]:    1     Gain 2x
    data = [ 0x40|channel<<1, 0x90|((voltage>>8)&0xF), voltage&0xFF ]
    with SMBus(i2c_bus) as bus:
#        hex_string = "".join("%02x " % b for b in data)
#        print("write: "+hex_string)
        msg = i2c_msg.write(i2c_MCP4728_addresses[chip], data)
        bus.i2c_rdwr(msg)


# read voltage on all channels of a chip
def getCurrentSettings(chip):
    if chip >= len(i2c_MCP4728_addresses):
        raise IndexError
    with SMBus(i2c_bus) as bus:
        msg = i2c_msg.read(i2c_MCP4728_addresses[chip],24)
        bus.i2c_rdwr(msg)
        dataRead = list(msg)
#        hex_string = "".join("%02x " % b for b in dataRead)
#        print("write: "+hex_string)
        # stride is 6 because we get 6 bytes for each channel; 3 for the output regs
        # and 3 for the eeprom. Here we only care about the output register so we throw out
        # the eeprom values as 'n/a'
        current_values = []
        # pylint:disable=unused-variable
        for header, high_byte, low_byte, na_1, na_2, na_3 in _chunk(dataRead, 6):
            # pylint:enable=unused-variable
            channel_values = {}
            value = (high_byte & 0x0F) << 8 | low_byte
            voltage = value * 8
            channel_values['voltage'] = voltage / 1000
            channel_values.update(_get_flags(high_byte))
            current_values.append(channel_values)
        return current_values



# ADS1015 read analog voltage on ADC input
# [15]:     1           start conversion
# [14:12]:100+<ch>      convert channel <ch>
# [11:9]: 001           FSR: +-4.096V
# [8]:      1           single shot mode
# [7:5]:  100           1600 SPS (default)
# [4]:      0           Traditional comparator (default)
# [3]:      0           Comperator active low (default)
# [2]:      0           Nonlatching comparator. The ALERT/RDY pin does not latch when asserted (default)
# [1:0]    11           Disable comparator and set ALERT/RDY pin to high-impedance (default)
def _readAnalogChannelRaw(channel):
    if channel >= 4:
        raise IndexError

    with SMBus(i2c_bus) as bus:
#        hex_string = "".join("%02x " % b for b in data)
#        print("write: "+hex_string)
        data = [ 0x01, 0b11000011 | (channel<<4), 0b10000011 ]  # single conversion
        msg = i2c_msg.write(i2c_ADS1015_address, data)
        bus.i2c_rdwr(msg)
        time.sleep(0.1)
        data = [ 0x00 ]                                         # select conversion register
        msg = i2c_msg.write(i2c_ADS1015_address, data)
        bus.i2c_rdwr(msg)
        msg = i2c_msg.read(i2c_ADS1015_address, 2)
        bus.i2c_rdwr(msg)
    bytesRead = list(msg)
    value = (bytesRead[0]<<4) | (bytesRead[1]>>4)
    value /= 500
    return value

def readGPIOVoltage(GPIOChannel):
    if GPIOChannel == 0:
        value = _readAnalogChannelRaw(2)
    elif GPIOChannel == 1:
        value = _readAnalogChannelRaw(3)
    else:
        raise IndexError

    # factor in 68k/10k resistor divider
    value *= 78
    value /= 10
    return value

def readOneWireVoltage():
    return _readAnalogChannelRaw(1)*2

# get current loop input voltage in mA
def readCurrentLoopInput():
    value = _readAnalogChannelRaw(0)
    # with 75R shunt resistor
    value *= 1000/75
    return value
