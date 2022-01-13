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
import threading
from gw4xxx_hal.gw4x00.gw4x00_interfaces import gw4x00Interfaces, gw4x00GpioState
#from gw4x00.gw4x00_interfaces import gw4x00Interfaces, gw4x00GpioState

# GW4x00 input control
class GW4100Input:
    def __init__(self, input, consumer:str="gw4x00_io"):
        if input >= len(gw4x00Interfaces["inputs"]):
            raise IndexError
        self.input = input
        chip = gpiod.Chip('{}'.format(gw4x00Interfaces["inputs"][input]["gpiochip"]))
        self.gpioline = chip.get_line(gw4x00Interfaces["inputs"][input]["gpioline"])
#        self.gpioline.request(consumer=consumer, type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_ACTIVE_LOW)
        self.gpioline.request(consumer=consumer, type=gpiod.LINE_REQ_DIR_IN)
       
    def getInput(self) -> int:
        return self.gpioline.get_value()

# GW4x00 counter input control
class GW4100CounterInput:
    def __init__(self, input, consumer:str="gw4x00_io"):
        if input >= len(gw4x00Interfaces["inputs"]):
            raise IndexError
        self.counter = 0
        self.input = input
        chip = gpiod.Chip('{}'.format(gw4x00Interfaces["inputs"][input]["gpiochip"]))
        self.gpioline = chip.get_line(gw4x00Interfaces["inputs"][input]["gpioline"])
        self.gpioline.request(consumer=consumer, type=gpiod.LINE_REQ_EV_RISING_EDGE, flags=gpiod.LINE_REQ_FLAG_ACTIVE_LOW)

    def startCounter(self):
        self.counterThread = threading.Thread(target=self._counterThread)
        self.counterThread.start()

    def _counterThread(self):
        while True:
            if self.gpioline.event_wait(nsec=100000):
                events = self.gpioline.event_read_multiple()
                self.counter += len(events)

    def getCounter(self):
        return self.counter

    def setCounter(self, value=0):
        self.counter = value

    def getInput(self) -> int:
        return self.gpioline.get_value()

# GW4x00 GPIO control
class GW4100Gpio:
    def __init__(self, gpioNr, initState:gw4x00GpioState="input", pullup:bool=False, consumer:str="gw4100_io"):
        if gpioNr >= len(gw4x00Interfaces["gpios"]):
            raise IndexError
        self.gpioNr = gpioNr
        # create storage for outputs
        self.outputs = dict.fromkeys([ "highside", "lowside", "pullup"])
#        config = gpiod.line_request()
        for output in [ "highside", "lowside", "pullup"]:
            chip = gpiod.Chip('{}'.format(gw4x00Interfaces["gpios"][gpioNr][output]["gpiochip"]))
            self.outputs[output] = chip.get_line(gw4x00Interfaces["gpios"][gpioNr][output]["gpioline"])

#            config.consumer = consumer
#            config.request_type = gpiod.line_request.DIRECTION_OUTPUT

            self.outputs[output].request(consumer=consumer, type=gpiod.LINE_REQ_DIR_OUT)
        
        chip = gpiod.Chip('{}'.format(gw4x00Interfaces["gpios"][gpioNr]["input"]["gpiochip"]))
        self.input = chip.get_line(gw4x00Interfaces["gpios"][gpioNr]["input"]["gpioline"])
#        config.consumer = consumer
#        config.request_type = gpiod.line_request.DIRECTION_INPUT
#        config.flags = gpiod.line_request.FLAG_BIAS_PULL_UP
        self.input.request(consumer=consumer, type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)
        self.setOutput(initState)
        self.activatePullup(pullup)

    def activatePullup(self, state):
        if state:
            self.outputs["pullup"].set_value(1)
        else:
            self.outputs["pullup"].set_value(0)

    def getInput(self) -> int:
        return int(self.input.get_value() == 0)

    def setOutput(self, state:gw4x00GpioState):
        if not state in gw4x00GpioState:
            raise ValueError            
        if state == "high":
            self.outputs["lowside"].set_value(0)
            self.outputs["highside"].set_value(1)
        elif state == "low":
            self.outputs["highside"].set_value(0)
            self.outputs["lowside"].set_value(1)
        else:   # input
            self.outputs["highside"].set_value(0)
            self.outputs["lowside"].set_value(0)

    def getOutput(self, output) -> int:
        if not output in [ "highside", "lowside", "pullup"]:
            raise ValueError
        else:
            return self.outputs[output].get_value()

    def getADC(self):
        with open(gw4x00Interfaces["gpios"][self.gpioNr]["adc"]) as f:
            value=float(f.read())/(4095)*1.8*37.5/1.5
            return value
