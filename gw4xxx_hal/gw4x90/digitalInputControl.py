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
#import gpiod
from gw4xxx_hal.gw4xxx.libgpiod_wrapper import libgpiod

inputLines = [ (5, 14), (5, 15) ]

# channels:
# 0: IN12
# 1: IN13
def getInput(channel, consumer:str="gw4x90_in"):
    if channel >= 2:            
        raise IndexError
    
#    config = gpiod.line_request()
    chipNr, lineNr = inputLines[channel]
    line = libgpiod.getInputLine(chipNr, lineNr, consumer, active_low=True)

#    chip = gpiod.Chip('{}'.format(chipNr))
#    line = chip.get_line(lineNr)
 #   config.consumer = "gw4x90_io"
 #   config.request_type = gpiod.line_request.DIRECTION_INPUT
#    line.request(consumer="gw4x90_io", type=gpiod.Line.DIRECTION_INPUT, flags=gpiod.LINE_REQ_FLAG_ACTIVE_LOW)
    value = line.get_value()
    line.release()
    return value


