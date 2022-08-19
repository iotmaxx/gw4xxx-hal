gw4x00Interfaces = {
    "gpios" : [
        {
            "highside": { "gpiochip": 0, "gpioline": 0 },
            "lowside":  { "gpiochip": 0, "gpioline": 1 },
            "pullup":   { "gpiochip": 0, "gpioline": 2 },
            "input":    { "gpiochip": 0, "gpioline": 3 },
            "adc":      "/sys/bus/iio/devices/iio:device0/in_voltage0_raw"
        },
        {
            "highside": { "gpiochip": 0, "gpioline": 4 },
            "lowside":  { "gpiochip": 0, "gpioline": 5 },
            "pullup":   { "gpiochip": 0, "gpioline": 8 },
            "input":    { "gpiochip": 0, "gpioline": 9 },
            "adc":      "/sys/bus/iio/devices/iio:device0/in_voltage1_raw"
        }
    ],
    "inputs" : [
        { "gpiochip": 0, "gpioline": 10 },
        { "gpiochip": 0, "gpioline": 11 },
        { "gpiochip": 0, "gpioline": 14 },
        { "gpiochip": 0, "gpioline": 15 },
    ],
    "LEDs" : [
        "/sys/class/leds/iotmaxx:green:usr1/",
        "/sys/class/leds/iotmaxx:green:usr2/",
    ],
    "user_button":      { "gpiochip": 2, "gpioline": 27 },
    "sim_enable":       { "gpiochip": 2, "gpioline": 25 },
    "sim_select":       { "gpiochip": 3, "gpioline": 16 },
    "CAN_term_en_n":    { "gpiochip": 3, "gpioline": 12 },
    "GSM_power_ind":    { "gpiochip": 3, "gpioline": 19 },
    "PBSTAT_IRQ_n":     { "gpiochip": 1, "gpioline":  1 },
    "ACT8847_IRQ_n":    { "gpiochip": 2, "gpioline": 26 },
    "RTC_INTA_n":       { "gpiochip": 1, "gpioline": 29 },
}

gw4x00GpioState = { "high", "low", "tri-state", "input" }

