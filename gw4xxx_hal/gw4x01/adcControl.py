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
import gpiod
import spidev
import time
from smbus2 import SMBus, i2c_msg
from gw4xxx_hal.gw4x01.gw4x01_interfaces import gw4x01Interfaces
from gw4xxx_hal.gw4xxx.exceptions import ChannelPoweredDownError


class GW4x01ADC:
    def __init__(self, consumer:str="gw4x01_adc"):
        self.ChannelSelectIOs = []
        for i in range(2):
            chip = gpiod.Chip('{}'.format(gw4x01Interfaces["ChannelSelectIOs"][i]["gpiochip"]))
            line = chip.get_line(gw4x01Interfaces["ChannelSelectIOs"][i]["gpioline"])
            line.request(consumer=consumer, type=gpiod.LINE_REQ_DIR_OUT, default_val=0)
            self.ChannelSelectIOs.append(line)
        self.spi = spidev.SpiDev()
        self.spi.open(gw4x01Interfaces["SPI"]["bus"], gw4x01Interfaces["SPI"]["device"])
        try:    # ignore error as it is caused by wrong initialization of cs_high, mode setting is applied as expected
            self.spi.mode = gw4x01Interfaces["SPI"]["mode"]
        except:
            pass
        self.spi.max_speed_hz = gw4x01Interfaces["SPI"]["max_speed"]
        self.spi.xfer2([0x06])   # Reset
        time.sleep(0.1)


    def _selectChannel(self, channel):
        if channel >= 4:
            raise IndexError
        selectIOs = [ channel&0x1, (channel>>1)&0x1 ]
        self.ChannelSelectIOs[0].set_value(selectIOs[0])
        self.ChannelSelectIOs[1].set_value(selectIOs[1])

    def readCurrentLoop(self, channel) -> float:
        self._selectChannel(channel)
        # Reg 0:
        # 7-4: 1010: AIN P = AIN2, AIN N = AVSS
        # 3-1: 000:	Gain = 1
        # 0: 	0:		PGA enabled (can be disabled)

        # Reg1: Reset value 0x00

        # Reg2:
        # 7-6: 00: Internal 2.048-V reference selected (default)
        # 5-4: 01: Simultaneous 50-Hz and 60-Hz rejection
        # 3:    0: Switch is always open (default)
        # 2-0: 000: Off (default)

        # Reg3:
        # 7-5: 000: IDAC1 disabled (default)
        # 4-2: 000: IDAC2 disabled (default)
        # 1:     0: Only the dedicated DRDY pin is used to indicate when data are ready (default)
        # 0:     0: Reserved
        self.spi.xfer2([ 0x43, 0xA0, 0x00, 0x10, 0x00 ])
        time.sleep(0.1)
        self.spi.xfer2([0x08])   # Start conversion
        time.sleep(0.1)
        result=self.spi.xfer2([ 0xFF, 0xFF, 0xFF ])

        convResult = (result[0]<<16)+(result[1]<<8)+result[2]

        convResult *= 2048.0
        convResult /= 0xFFFFFF
        convResult /= 75.0
        convResult *= 2

        return convResult

    def readRTDValue(self, channel) -> float:
        self._selectChannel(channel)
        #  		Reg 0:
        #		7-4: 0000: AIN P = AIN0, AIN N = AIN1 (default)
        #		3-1: 000:	Gain = 1
        #		0: 	0:		PGA disabled
        #		Reg1: Reset value 0x00
        #
        #		Reg2:
        #		7-6: 01: External reference selected using dedicated REFP0 and REFN0 inputs
        #		5-4: 01: Simultaneous 50-Hz and 60-Hz rejection
        #		3:    0: Switch is always open (default)
        #		2-0:100: 250 μA
        #
        #		Reg3:
        #		7-5: 100: IDAC1 connected to AIN3/REFN1
        #		4-2: 000: IDAC2 disabled (default)
        #		1:     0: Only the dedicated DRDY pin is used to indicate when data are ready (default)
        #		0:     0: Reserved
        self.spi.xfer2([ 0x43, 0x01, 0x00, 0x54, 0x80 ])
        #    spi.xfer2([ 0x43, 0x00, 0x00, 0x53, 0x80 ])
        time.sleep(0.1)
        result=self.spi.xfer2([ 0xFF, 0xFF, 0xFF ])
        #    print('Result:{:02x}{:02x}{:02x}'.format(result[0], result[1], result[2]))

        #		Reg3:
        #		7-5: 000: IDAC1 disabled (default)
        #		4-2: 000: IDAC2 disabled (default)
        #		1:     0: Only the dedicated DRDY pin is used to indicate when data are ready (default)
        #		0:     0: Reserved
        self.spi.xfer2([ 0x4C, 0x00 ])

        convResult = (result[0]<<16)+(result[1]<<8)+result[2]
        #   print('Result:{:d}'.format(convResult))

        convResult *= 2000.0
        convResult /= 0x7FFFFF
        #   print('Result:{:f}'.format(convResult))

        return convResult

    def read10MOhmsRangeValue(self, channel) -> float:
        self._selectChannel(channel)
        #  		Reg 0:
        #		7-4: 0000: AIN P = AIN0, AIN N = AIN1 (default)
        #		3-1: 000:	Gain = 1
        #		0: 	1:		PGA disabled
        #		Reg1: Reset value 0x00
        #
        #		Reg2:
#        #       7-6: 00: Internal 2.048-V reference selected (default)
        #            11: Analog supply (AVDD – AVSS) used as reference
        #       5-4: 01: Simultaneous 50-Hz and 60-Hz rejection
        #       3:    0: Switch is always open (default)
#        #		2-0:100: 250 μA
        #		2-0:011: 100 μA
        #
        #		Reg3:
        #		7-5: 100: IDAC1 connected to AIN3/REFN1
        #		4-2: 000: IDAC2 disabled (default)
        #		1:     0: Only the dedicated DRDY pin is used to indicate when data are ready (default)
        #		0:     0: Reserved
#        self.spi.xfer2([ 0x43, 0x01, 0x00, 0xC4, 0x80 ])
        self.spi.xfer2([ 0x43, 0x01, 0x00, 0xD1, 0x80 ])
        #    spi.xfer2([ 0x43, 0x00, 0x00, 0x53, 0x80 ])
        time.sleep(0.1)
        result=self.spi.xfer2([ 0xFF, 0xFF, 0xFF ])
        #    print('Result:{:02x}{:02x}{:02x}'.format(result[0], result[1], result[2]))

        #		Reg3:
        #		7-5: 000: IDAC1 disabled (default)
        #		4-2: 000: IDAC2 disabled (default)
        #		1:     0: Only the dedicated DRDY pin is used to indicate when data are ready (default)
        #		0:     0: Reserved
        self.spi.xfer2([ 0x4C, 0x00 ])

        convResult = (result[0]<<16)+(result[1]<<8)+result[2]
        print('Result:{:d} ({:x})'.format(convResult,convResult))

        convResult *= 4500.0
        convResult /= 0x7FFFFF
#        convResult /= 250
        convResult /= 100
        #   print('Result:{:f}'.format(convResult))

        return convResult

    # set output current
    # current: current [mA] to be set
    def setOutputCurrent(self, current):
        # MCP4716 command:
        # byte 0
        # [7:5]: 010    write volatile memory command
        # [4:3]:  11    Vref pin (buffered) as reference
        # [2:1]:  00    not powered down
        # [0]:     0    gain 1x
        #
        # byte [1:2]: D09 D08 D07 D06 D05 D04 D03 D02 D01 D00 X X X X X X
        currentCode = int(1024 * current / 20.2)
        data = [ 0x58, (currentCode>>2)&0xFF, (currentCode<<6)&0xFF ]

        with SMBus(gw4x01Interfaces["I2C"]["bus"]) as bus:
    #        hex_string = "".join("%02x " % b for b in data)
    #        print("write: "+hex_string)
            msg = i2c_msg.write(gw4x01Interfaces["I2C"]["MCP4176Address"], data)
            bus.i2c_rdwr(msg)
    #        msg = i2c_msg.read(i2c_chip_addresses[channel], 6)
    #        bus.i2c_rdwr(msg)
    #        block = list(msg)
    #        hex_string = "".join("%02x " % b for b in block)
    #        print("read: "+hex_string)

    # power down selected channel
    def powerDownChannel(self):
        # MCP4716 command:
        # byte 0
        # [7:5]: 100    write volatile configuration bits
        # [4:3]:  11    Vref pin (buffered) as reference
        # [2:1]:  10    Powered Down - VOUT is loaded with 100 kΩ resistor to ground.
        # [0]:     0    gain 1x
        data = [ 0x9C ]

        with SMBus(gw4x01Interfaces["I2C"]["bus"]) as bus:
            msg = i2c_msg.write(gw4x01Interfaces["I2C"]["MCP4176Address"], data)
            bus.i2c_rdwr(msg)

    # get output current 
    def getOutputCurrent(self):
        with SMBus(gw4x01Interfaces["I2C"]["bus"]) as bus:
            msg = i2c_msg.read(gw4x01Interfaces["I2C"]["MCP4176Address"], 6)
            bus.i2c_rdwr(msg)
        response = list(msg)
        if (response[0] & 0x6) != 0x0:
            raise ChannelPoweredDownError
        value = response[1]<<2 | response[2]>>6
        return value*20.2/1024
