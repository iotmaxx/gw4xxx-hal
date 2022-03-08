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

""" GW4x00_internalIOs = {
    "CAN_TERM_EN_n" : { "pin" : 0, "mode" : gpio.IN, "active_low": False  },
    "SIM_ENABLE"    : { "pin" : 0, "mode" : gpio.IN, "active_low": False  },
    "SIM_SEL"       : { "pin" : 0, "mode" : gpio.IN, "active_low": False  },
    "PBSTAT_IRQ_n"  : { "pin" : 0, "mode" : gpio.IN, "active_low": False  },
    "ACT8847_IRQ_n" : { "pin" : 0, "mode" : gpio.IN, "active_low": False  },
    "RTC_INTA_n"    : { "pin" : 0, "mode" : gpio.IN, "active_low": False  },
    "USR_SWITCH_n"  : { "pin" : 0, "mode" : gpio.IN, "active_low": False  },
    "GSM_PWR_IND_n" : { "pin" : 0, "mode" : gpio.IN, "active_low": False  },
}
 """
i2c_busses = { "I2C_CTRL" : 2}
i2c_addresses = { "PMIC" : 0x5A }
i2c_regs = {
    "PMIC": { "REG9_VSET": 0x70, "REG9_CTRL": 0x71 }
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

