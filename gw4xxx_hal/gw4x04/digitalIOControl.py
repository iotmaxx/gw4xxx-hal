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
# import gpiod
import threading
from gw4xxx_hal.gw4x04.gw4x04_interfaces import gw4x04Interfaces
from gw4xxx_hal.gw4xxx.libgpiod_wrapper import libgpiod

# GW4x04 input control
class GW4x04Input:
    def __init__(self, input, consumer:str="gw4x04_io"):
        if input >= len(gw4x04Interfaces["inputs"]):
            raise IndexError
        self.input = input
        self.gpioline = libgpiod.getInputLine(gw4x04Interfaces["inputs"][input]["gpiochip"], gw4x04Interfaces["inputs"][input]["gpioline"], consumer,  active_low=True)
#        chip = gpiod.Chip('{}'.format(gw4x04Interfaces["inputs"][input]["gpiochip"]))
#        self.gpioline = chip.get_line(gw4x04Interfaces["inputs"][input]["gpioline"])
#        self.gpioline.request(consumer=consumer, type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_ACTIVE_LOW)
       
    def getInput(self) -> int:
        return self.gpioline.get_value()

# GW4x04 counter input control
class GW4x04CounterInput:
    def __init__(self, input, consumer:str="gw4x04_io"):
        if input >= len(gw4x04Interfaces["inputs"]):
            raise IndexError
        self.counter = 0
        self.input = input
        self.gpioline = libgpiod.getInterruptLine(gw4x04Interfaces["inputs"][input]["gpiochip"], gw4x04Interfaces["inputs"][input]["gpioline"], consumer,  active_low=True, edge=libgpiod.RISING)
#        chip = gpiod.Chip('{}'.format(gw4x04Interfaces["inputs"][input]["gpiochip"]))
#        self.gpioline = chip.get_line(gw4x04Interfaces["inputs"][input]["gpioline"])
#        self.gpioline.request(consumer=consumer, type=gpiod.LINE_REQ_EV_RISING_EDGE, flags=gpiod.LINE_REQ_FLAG_ACTIVE_LOW)

    def startCounter(self):
        self.counterThread = threading.Thread(name=f'Gw4x04 input {self.input}', target=self._counterThread, daemon=True)
        self.counterThread.start()

    def _counterThread(self):
        while True:
            if self.gpioline.event_wait(nsec=100000000):
                events = self.gpioline.event_read_multiple()
                self.counter += len(events)

    def getCounter(self):
        return self.counter

    def setCounter(self, value=0):
        self.counter = value

    def getInput(self) -> int:
        return self.gpioline.get_value()

# GW4x04 isolated input control
class GW4x04IsoInput:
    def __init__(self, input, consumer:str="gw4x04_io"):
        if input >= len(gw4x04Interfaces["isoInputs"]):
            raise IndexError
        self.input = input
        self.gpioline = libgpiod.getInputLine(gw4x04Interfaces["isoInputs"][input]["gpiochip"], gw4x04Interfaces["isoInputs"][input]["gpioline"], consumer)
#        chip = gpiod.Chip('{}'.format(gw4x04Interfaces["isoInputs"][input]["gpiochip"]))
#        self.gpioline = chip.get_line(gw4x04Interfaces["isoInputs"][input]["gpioline"])
#        self.gpioline.request(consumer=consumer, type=gpiod.LINE_REQ_DIR_IN)
       
    def getInput(self) -> int:
        return self.gpioline.get_value()

# GW4x04 isolated input control
class GW4x04IsoOutput:
    def __init__(self, output, consumer:str="gw4x04_io"):
        if output >= len(gw4x04Interfaces["isoOutputs"]):
            raise IndexError
        self.output = output
        self.gpioline = libgpiod.getOutputLine(gw4x04Interfaces["isoOutputs"][output]["gpiochip"], gw4x04Interfaces["isoOutputs"][output]["gpioline"], consumer, 0)
#        chip = gpiod.Chip('{}'.format(gw4x04Interfaces["isoOutputs"][input]["gpiochip"]))
#        self.gpioline = chip.get_line(gw4x04Interfaces["isoOutputs"][input]["gpioline"])
#        self.gpioline.request(consumer=consumer, type=gpiod.LINE_REQ_DIR_OUT, default_val=0)
       
    def setOutput(self, value):
        self.gpioline.set_value(value)

    def getOutput(self):
        return self.gpioline.get_value()

