""" 
gw4xxx-hal - IoTmaxx Gateway Hardware Abstraction Layer
Copyright (C) 2021-2025 IoTmaxx GmbH

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
from gpiod.line import Direction, Value, Edge, Bias
from datetime import timedelta

class LibgpiodWrapper:
    RISING = None
    FALLING = None
    BOTH = None
    NONE = None
    PULL_NONE = None
    PULL_UP = None
    PULL_DOWN = None

    def getOutputLine(self, gpiochip_nr, line_offset, initial_value):
        pass

    def getInputLine(self, gpiochip_nr, line_offset, consumer):
        pass

    def getInterruptLine(self, gpiochip_nr, line_offset, consumer, edge=BOTH):
        pass

class Libgpiod2Wrapper(LibgpiodWrapper):
    RISING = Edge.RISING
    FALLING = Edge.FALLING
    BOTH = Edge.BOTH
    NONE = Edge.NONE
    PULL_NONE = Bias.DISABLED
    PULL_UP = Bias.PULL_UP
    PULL_DOWN = Bias.PULL_DOWN

    def getOutputLine(self, gpiochip_nr, line_offset, consumer, initial_value, active_low=False):
        if initial_value:
            value = Value.ACTIVE
        else:
            value = Value.INACTIVE
        lines = gpiod.request_lines(
            f"/dev/gpiochip{gpiochip_nr}",
            consumer=consumer,
            config={
                line_offset: gpiod.LineSettings(
                    direction=Direction.OUTPUT, output_value=value, active_low=active_low
                )
            },
        )
        return Libgpio2LineWrapper(lines, line_offset)

    def getInputLine(self, gpiochip_nr, line_offset, consumer, active_low=False, bias=PULL_NONE):
        lines = gpiod.request_lines(
            f"/dev/gpiochip{gpiochip_nr}",
            consumer=consumer,
            config={line_offset: gpiod.LineSettings(direction=Direction.INPUT, active_low=active_low, bias=bias)},
        )
        return Libgpio2LineWrapper(lines, line_offset)

    def getInterruptLine(self, gpiochip_nr, line_offset, consumer, active_low=False, edge=BOTH):
        lines = gpiod.request_lines(
            f"/dev/gpiochip{gpiochip_nr}",
            consumer=consumer,
            config={line_offset: gpiod.LineSettings(edge_detection=edge, active_low=active_low)},
        )
        return Libgpio2LineWrapper(lines, line_offset)

class LibgpioLineWrapper:
    def set_value(self, new_value):
        pass

    def get_value(self):
        pass

    def event_wait(self, sec, nsec):
        pass

    def event_read(self):
        pass

class Libgpio2Event:
    RISING_EDGE = 1
    FALLING_EDGE = 2
    
    def __init__(self, type):
        self._type = type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

class Libgpio2LineWrapper(LibgpioLineWrapper):
    def __init__(self, lines, line_offset):
        self.lines = lines
        self.line_offset = line_offset

    def set_value(self, new_value):
        if new_value:
            value = Value.ACTIVE
        else:
            value = Value.INACTIVE
        self.lines.set_value(self.line_offset, value)

    def get_value(self):
        value = self.lines.get_value(self.line_offset)
        if value == Value.ACTIVE:
            return 1
        else:
            return 0

    def event_wait(self, sec, nsec):
        wait_time = timedelta(seconds=sec, microseconds=1000*nsec)
        return self.lines.wait_edge_events(timeout=wait_time)

    def event_read(self):
        for event in self.lines.read_edge_events():
            event_type = event.event_type

        if event_type is event.Type.RISING_EDGE:
            return Libgpio2Event(Libgpio2Event.RISING_EDGE)
        else:
            return Libgpio2Event(Libgpio2Event.FALLING_EDGE)

    def event_read_multiple(self):
        events = []
        for event in self.lines.read_edge_events():
            if event.event_type is event.Type.RISING_EDGE:
                events.append(Libgpio2Event(Libgpio2Event.RISING_EDGE))
            else:
                events.append(Libgpio2Event(Libgpio2Event.FALLING_EDGE))
        return events

    def release(self):
        self.lines.release()

def getLibGpiod():
    return Libgpiod2Wrapper()

libgpiod = Libgpiod2Wrapper()
