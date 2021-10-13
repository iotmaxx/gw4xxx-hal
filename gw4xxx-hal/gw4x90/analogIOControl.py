from smbus2 import SMBus, i2c_msg

i2c_bus = 3
i2c_MCP4728_addresses = [ 0x65, 0x66, 0x67, 0x64 ]

def check_valid_chip_channel(func):
    def inner(chip, channel, *args, **kwargs):
        if chip >= len(i2c_MCP4728_addresses):
           raise IndexError
        if channel >= 4:
           raise IndexError
        return func(chip, channel, *args, **kwargs)
    return inner

# set output voltage on analog output channels
# Mapping:
# chip# | channels [0:3]
#   0   | [00:03]
#   1   | [IO0,IO1,12,13]
#   2   | [30:33]
#   3   | [40:43]
@check_valid_chip_channel
def setVoltage(chip, channel, voltage):
    voltage = int(voltage*1000)
    voltage = int(voltage/8)
    # [7]:    1     Internal Vref (2.048V)
    # [6:5]: 00     no power down
    # [4]:    1     Gain 2x
    data = [ 0x40|channel<<1, 0x90|((voltage>>8)&0xF), voltage&0xFF ]
    with SMBus(i2c_bus) as bus:
#        hex_string = "".join("%02x " % b for b in data)
#        print("write: "+hex_string)
        msg = i2c_msg.write(i2c_MCP4728_addresses[chip], data)
        bus.i2c_rdwr(msg)

