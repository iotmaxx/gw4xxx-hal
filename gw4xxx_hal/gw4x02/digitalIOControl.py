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
from gw4xxx_hal.gw4x02.gw4x02_interfaces import gw4x02Interfaces


# GW4x02 isolated input control
class GW4x02IsoInput:
    def __init__(self, input, consumer:str="gw4x02_io"):
        if input >= len(gw4x02Interfaces["isoInputs"]):
            raise IndexError
        self.input = input
#        config = gpiod.line_request()
#        print(f'request chip {gw4x02Interfaces["isoInputs"][input]["gpiochip"]}, line {gw4x02Interfaces["isoInputs"][input]["gpioline"]}')
        chip = gpiod.Chip('{}'.format(gw4x02Interfaces["isoInputs"][input]["gpiochip"]))
        self.gpioline = chip.get_line(gw4x02Interfaces["isoInputs"][input]["gpioline"])
 #       config.consumer = consumer
 #       config.request_type = gpiod.line_request.DIRECTION_INPUT
#        self.gpioline.request(consumer=consumer, type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_ACTIVE_LOW)
        self.gpioline.request(consumer=consumer, type=gpiod.LINE_REQ_DIR_IN)
       
    def getInput(self) -> int:
        return self.gpioline.get_value()

# GW4x02 isolated input control
class GW4x02IsoOutput:
    def __init__(self, input, consumer:str="gw4x02_io"):
        if input >= len(gw4x02Interfaces["isoOutputs"]):
            raise IndexError
        self.input = input
#        config = gpiod.line_request()
        chip = gpiod.Chip('{}'.format(gw4x02Interfaces["isoOutputs"][input]["gpiochip"]))
        self.gpioline = chip.get_line(gw4x02Interfaces["isoOutputs"][input]["gpioline"])
 #       config.consumer = consumer
 #       config.request_type = gpiod.line_request.DIRECTION_INPUT
#        self.gpioline.request(consumer=consumer, type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_ACTIVE_LOW)
        self.gpioline.request(consumer=consumer, type=gpiod.LINE_REQ_DIR_OUT, default_val=0)
       
    def setOutput(self, value):
        self.gpioline.set_value(value)

    def getOutput(self):
        return self.gpioline.get_value()

