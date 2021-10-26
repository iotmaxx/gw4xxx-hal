""" 
gw4xxx-hal - IoTmaxx Gateway Hardware Abstraction Layer
Copyright (C) 2021 IoTmaxx GmbH

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from smbus2 import SMBus, i2c_msg
import sys
from gw4xxx.exceptions import ChannelPoweredDownError

i2c_bus = 3
i2c_chip_addresses = [ 0x60, 0x61, 0x62, 0x63 ]

def check_valid_channel(func):
    def inner(channel, *args, **kwargs):
        if channel >= len(i2c_chip_addresses):
           raise IndexError
        return func(channel, *args, **kwargs)
    return inner

# set output current on channel
# channel: the channel to output current on
# current: current [mA] to be set
@check_valid_channel
def setOutputCurrent(channel, current):
    # MCP4716 command:
    # byte 0
    # [7:5]: 010    write volatile memory command
    # [4:3]:  11    Vref pin (buffered) as reference
    # [2:1]:  00    not powered down
    # [0]:     0    gain 1x
    #
    # byte [1:2]: D09 D08 D07 D06 D05 D04 D03 D02 D01 D00 X X X X X X
    currentCode = int(1024 * current / 25)
    data = [ 0x58, (currentCode>>2)&0xFF, (currentCode<<6)&0xFF ]

    with SMBus(i2c_bus) as bus:
#        hex_string = "".join("%02x " % b for b in data)
#        print("write: "+hex_string)
        msg = i2c_msg.write(i2c_chip_addresses[channel], data)
        bus.i2c_rdwr(msg)
#        msg = i2c_msg.read(i2c_chip_addresses[channel], 6)
#        bus.i2c_rdwr(msg)
#        block = list(msg)
#        hex_string = "".join("%02x " % b for b in block)
#        print("read: "+hex_string)

# power down selected channel
@check_valid_channel
def powerDownChannel(channel):
    # MCP4716 command:
    # byte 0
    # [7:5]: 100    write volatile configuration bits
    # [4:3]:  11    Vref pin (buffered) as reference
    # [2:1]:  10    Powered Down - VOUT is loaded with 100 kΩ resistor to ground.
    # [0]:     0    gain 1x
    data = [ 0x9C ]

    with SMBus(i2c_bus) as bus:
        msg = i2c_msg.write(i2c_chip_addresses[channel], data)
        bus.i2c_rdwr(msg)

# get output current on selected channel
@check_valid_channel
def getOutputCurrent(channel):
    with SMBus(i2c_bus) as bus:
        msg = i2c_msg.read(i2c_chip_addresses[channel], 6)
        bus.i2c_rdwr(msg)
    response = list(msg)
    # powered down?
    if (response[0] & 0x6) != 0x0:
        raise ChannelPoweredDownError
    value = response[1]<<2 | response[2]>>6
    return value*25/1024

