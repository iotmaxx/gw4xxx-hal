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
import smbus2
import gpiod
import time
#import threading
from gw4xxx_hal.gw4x00.gw4x00_interfaces import gw4x00Interfaces, gw4x00GpioState

# GW4x00 user button
class GW4100UserButton:
    def __init__(self, consumer:str="gw4x00_io"):
        chip = gpiod.Chip('{}'.format(gw4x00Interfaces["user_button"]["gpiochip"]))
        self.gpioline = chip.get_line(gw4x00Interfaces["user_button"]["gpioline"])
        self.gpioline.request(consumer=consumer, type=gpiod.LINE_REQ_EV_BOTH_EDGES, flags=gpiod.LINE_REQ_FLAG_ACTIVE_LOW)
        
    def getState(self) -> int:
        return self.gpioline.get_value()

    def waitForButtonEvent(self, sec=1, nsec=0):
        retVal = 'timeout'
        if self.gpioline.event_wait(sec,nsec):
            event = self.gpioline.event_read()
            if event.type == event.RISING_EDGE:
                retVal = 'pressed'
            else:
                retVal = 'released'
        return retVal

def setLEDon(led, on=True):
    try:
        brightnessFile = gw4x00Interfaces["LEDs"][led]+'brightness'
    except:
        raise IndexError
    with open(brightnessFile,"w") as f:
        if on:
            f.write('255\n')
        else:
            f.write('0\n')

class GW4100USBPower:
    def __init__(self, consumer:str="gw4x00_io"):
        chip = gpiod.Chip('{}'.format(gw4x00Interfaces["usb_power"]["gpiochip"]))
        self.gpioline = chip.get_line(gw4x00Interfaces["usb_power"]["gpioline"])
        self.gpioline.request(consumer=consumer, type=gpiod.LINE_REQ_DIR_OUT, default_val=1)

    def resetUSB(self):
        self.gpioline.set_value(0)
        time.sleep(0.5)
        self.gpioline.set_value(1)
        time.sleep(0.5)


# GW4100 internal I/Os
class GW4100Internal:
    def __init__(self, consumer:str="gw4x00_io"):
        self.gpiolines = {}
#    "sim_enable":       { "gpiochip": 2, "gpioline": 25 },
#    "sim_select":       { "gpiochip": 3, "gpioline": 16 },
#    "CAN_term_en_n":    { "gpiochip": 3, "gpioline": 12 },
#    "GSM_power_ind":    { "gpiochip": 3, "gpioline": 19 },
        for gpioline in ["sim_enable", "sim_select", "CAN_term_en_n", "GSM_power_ind"]:
            chip = gpiod.Chip('{}'.format(gw4x00Interfaces[gpioline]["gpiochip"]))
            self.gpiolines[gpioline] = chip.get_line(gw4x00Interfaces[gpioline]["gpioline"])
        self.gpiolines["CAN_term_en_n"].request(consumer=consumer, type=gpiod.LINE_REQ_DIR_OUT, default_val=0)
#        self.gpiolines["sim_select"].request(consumer=consumer, type=gpiod.LINE_REQ_DIR_OUT, default_val=0)
#        self.gpiolines["sim_enable"].request(consumer=consumer, type=gpiod.LINE_REQ_DIR_OUT, default_val=1)
        self.gpiolines["GSM_power_ind"].request(consumer=consumer, type=gpiod.LINE_REQ_DIR_IN)

    def enableCanTermResistor(self,enable=True):
        self.gpiolines["CAN_term_en_n"].set_value(not enable)

#    def selectMiniNotMicroSIM(miniSIM=True):
#        self.gpiolines["sim_enable"].set_value(0)
#        time.sleep(0.1)
#        self.gpiolines["sim_select"].set_value(not miniSIM)
#        time.sleep(0.1)
#        self.gpiolines["sim_enable"].set_value(1)

    def isGSMOn(self):
        return self.gpiolines["GSM_power_ind"].get_value() == 0

i2c_busses = { "I2C_CTRL" : 2}
i2c_addresses = { "PMIC" : 0x5A, "USB_HUB": 0x08 }
i2c_regs = {
    "PMIC": { "REG3_VSET": 0x30, "REG3_CTRL": 0x32, "REG9_VSET": 0x70, "REG9_CTRL": 0x71 },
    "USB_HUB": { "STAT_CMD": 0xFF }
}

def _antVoltageToCode(voltage):
    if voltage < 600:
        raise ValueError
    elif voltage < 1200:
        code = int((voltage - 600)/25 + 0b000000)
#            print(f"Code {bin(code)}, voltage in: {voltage}, voltage set: {600+(code-0b000000)*25}")
    elif voltage < 2400:
        code = int((voltage - 1200)/50 + 0b011000)
#            print(f"Code {bin(code)}, voltage in: {voltage}, voltage set: {600+(code-0b011000)*50}")
    elif voltage <= 3900:
        code = int((voltage - 2400)/100 + 0b110000)
#            print(f"Code {bin(code)}, voltage in: {voltage}, voltage set: {2400+(code-0b110000)*100}")
    else:
        raise ValueError
    return code

def setGPSAntennaVoltage(voltage=3000):
    with smbus2.SMBus(i2c_busses["I2C_CTRL"]) as bus:
        if voltage == 0:
            data = [ i2c_regs["PMIC"]["REG9_CTRL"], 0x04 ]
            msg = smbus2.i2c_msg.write(i2c_addresses["PMIC"], data)
            bus.i2c_rdwr(msg)
        else:
            data = [ i2c_regs["PMIC"]["REG9_VSET"], _antVoltageToCode(voltage) ]
#            hex_string = "".join("%02x " % b for b in data)
#            print("write: "+hex_string)
            msg = smbus2.i2c_msg.write(i2c_addresses["PMIC"], data)
            bus.i2c_rdwr(msg)
            data = [ i2c_regs["PMIC"]["REG9_CTRL"], 0x80 ]
#            hex_string = "".join("%02x " % b for b in data)
#            print("write: "+hex_string)
            msg = smbus2.i2c_msg.write(i2c_addresses["PMIC"], data)
            bus.i2c_rdwr(msg)

def gsmPowerOn(on=True):
    with smbus2.SMBus(i2c_busses["I2C_CTRL"]) as bus:
            if on:
                data = [ i2c_regs["PMIC"]["REG3_VSET"], 0x3E ]
            else:
                data = [ i2c_regs["PMIC"]["REG3_VSET"], 0x00 ]
#            hex_string = "".join("%02x " % b for b in data)
#            print("write: "+hex_string)
            msg = smbus2.i2c_msg.write(i2c_addresses["PMIC"], data)
            bus.i2c_rdwr(msg)

def readPMICReg(reg):
    with smbus2.SMBus(i2c_busses["I2C_CTRL"]) as bus:
        b = bus.read_byte_data(i2c_addresses["PMIC"], reg)
    return b

def usbHubReset():
    with smbus2.SMBus(i2c_busses["I2C_CTRL"]) as bus:
        data = [ i2c_regs["USB_HUB"]["STAT_CMD"], 0x02 ]
        msg = smbus2.i2c_msg.write(i2c_addresses["PMIC"], data)
        bus.i2c_rdwr(msg)

def usbHubReadReg(reg):
    with smbus2.SMBus(i2c_busses["I2C_CTRL"]) as bus:
        b = bus.read_byte_data(i2c_addresses["USB_HUB"], reg)
    return b
