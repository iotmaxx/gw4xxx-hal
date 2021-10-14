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
    ]
}

gw4x00GpioState = { "high", "low", "tri-state", "input" }

