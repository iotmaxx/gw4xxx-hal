#!/bin/python

from gw4xxx_hal.gw4x00.internalIOs import GW4100USBPower
gp = GW4100USBPower()
gp.usbReset()
