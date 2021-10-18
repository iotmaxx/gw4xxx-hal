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
from gw4x01.gw4x01_interfaces import gw4x01Interfaces

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
        self.spi.max_speed_hz = gw4x01Interfaces["SPI"]["max_speed"]
        self.spi.mode = gw4x01Interfaces["SPI"]["mode"]
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
