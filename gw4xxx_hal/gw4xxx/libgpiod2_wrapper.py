from .libgpiod_wrapper_templates import LibgpiodWrapper, LibgpioLineWrapper
import gpiod
from datetime import timedelta
from gpiod.line import Direction, Value, Edge, Bias

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
