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

    def getInputLine(self, gpiochip_nr, line_offset, consumer, active_low=False, bias=PULL_NONE):
        pass

    def getInterruptLine(self, gpiochip_nr, line_offset, consumer, active_low=False, edge=BOTH):
        pass

class LibgpioLineWrapper:
    def set_value(self, new_value):
        pass

    def get_value(self):
        pass

    def event_wait(self, sec, nsec):
        pass

    def event_read(self):
        pass
