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
gw4x01Interfaces = {
    "ChannelSelectIOs" : [
        { "gpiochip": 6, "gpioline": 13 },
        { "gpiochip": 6, "gpioline": 10 }
    ],
    "SPI": {
        "bus": 2,
        "device": 0,
        "max_speed": 500000,
        "mode": 0b01
    },
    "I2C": {
        "bus": 3,
        "MCP4176Address": 0x60
    },
    "inputs" : [
        { "gpiochip": 6, "gpioline":  5 },
        { "gpiochip": 6, "gpioline": 11 },
        { "gpiochip": 6, "gpioline":  2 },
        { "gpiochip": 6, "gpioline":  6 },
    ],
    "isoInputs" : [
        { "gpiochip": 5, "gpioline": 16 },
        { "gpiochip": 5, "gpioline": 14 },
        { "gpiochip": 5, "gpioline": 12 },
        { "gpiochip": 5, "gpioline": 17 },
    ],
    "isoOutputs" : [
        { "gpiochip": 5, "gpioline": 18 },
        { "gpiochip": 5, "gpioline": 13 },
    ]    
}
