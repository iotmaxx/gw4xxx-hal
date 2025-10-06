from .libgpiod_wrapper_templates import LibgpiodWrapper
import gpiod

class Libgpiod1Wrapper(LibgpiodWrapper):
    NONE = 0
    RISING = gpiod.LINE_REQ_EV_RISING_EDGE
    FALLING = gpiod.LINE_REQ_EV_FALLING_EDGE
    BOTH = gpiod.LINE_REQ_EV_BOTH_EDGES
    PULL_NONE = gpiod.LINE_REQ_FLAG_BIAS_DISABLE
    PULL_UP = gpiod.LINE_REQ_FLAG_BIAS_PULL_UP
    PULL_DOWN = gpiod.LINE_REQ_FLAG_BIAS_PULL_DOWN
    
    def getOutputLine(self, gpiochip_nr, line_offset, consumer, initial_value, active_low=False):
        chip = gpiod.Chip('{}'.format(gpiochip_nr))
        output = chip.get_line(line_offset)
        if active_low:
            flags = gpiod.LINE_REQ_FLAG_ACTIVE_LOW
        else:
            flags = 0
        output.request(consumer=consumer, type=gpiod.LINE_REQ_DIR_OUT, default_val=initial_value, flags=flags)
        return output

    def getInputLine(self, gpiochip_nr, line_offset, consumer, active_low=False, bias=PULL_NONE):
        chip = gpiod.Chip('{}'.format(gpiochip_nr))
        gpioline = chip.get_line(line_offset)
        if active_low:
            flags = gpiod.LINE_REQ_FLAG_ACTIVE_LOW
        else:
            flags = 0
        flags |= bias
        gpioline.request(consumer=consumer, type=gpiod.LINE_REQ_DIR_IN, flags=flags)
        return gpioline

    def getInterruptLine(self, gpiochip_nr, line_offset, consumer, active_low=False, edge=BOTH):
        chip = gpiod.Chip('{}'.format(gpiochip_nr))
        gpioline = chip.get_line(line_offset)
        if active_low:
            flags = gpiod.LINE_REQ_FLAG_ACTIVE_LOW
        else:
            flags = 0
        gpioline.request(consumer=consumer, type=edge, flags=flags)
        return gpioline
