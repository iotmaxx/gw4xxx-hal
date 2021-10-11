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

import sys
import os
from struct import *
from crccheck.crc import Crc32
from .exceptions import *

EEPROM_MAGIC            = 0xc4ec31b6
EEPROM_SIZE             = 8*1024
MAIN_BOARD_EEPROM       = '/sys/bus/i2c/devices/2-0050/eeprom'
EXPANSION_BOARD_EEPROM  = '/sys/bus/i2c/devices/3-0050/eeprom'

def hasExpansionBoard():
    return os.path.isfile(EXPANSION_BOARD_EEPROM) 

def readEEPROM(eepromFile):
    if os.path.getsize(eepromFile) < EEPROM_SIZE:
        raise EEPROMSizeError

    with open(eepromFile, "rb") as f:
        eeprom = f.read(EEPROM_SIZE)
        f.close()

    return eeprom

def decodeCommonSection(eeprom):
    commonDataFormat = 'II16sI4s16s16sBIBBI'

    commonData = eeprom[:calcsize(commonDataFormat)]
    u32Magic, u32Checksum, caOverlayName, u32Product, uVersion, caProductName, caSerialNumber, u8Manufacturer, u32TimeOfProduction, u8Tester, u8TestResult, u32TimeOfTest = unpack(commonDataFormat, commonData)
    u8Major, u8Minor, u8Build = unpack('3Bx', uVersion)

    if u32Magic != EEPROM_MAGIC:
        raise WrongMagicError

    dataBlock = eeprom[8:256]
    if Crc32.calc(dataBlock) != u32Checksum:
        raise ChecksumError
 
#     print('Common data:')
# #    print('Magic:               0x{:08x}'.format(u32Magic))
# #    print('Check:               0x{:08x}'.format(u32Checksum))
#     print('OverlayName:         {}'.format(caOverlayName.decode('utf-8', errors='ignore').strip('\x00')))
#     print('Version:             {}.{}.{}'.format(u8Major, u8Minor, u8Build))
#     print('Product:             0x{:08x}'.format(u32Product))
#     print('ProductName:         {}'.format(caProductName.decode('utf-8', errors='ignore').strip('\x00')))
#     print('SerialNumber:        {}'.format(caSerialNumber.decode('utf-8', errors='ignore').strip('\x00')))
#     print('Manufacturer:        0x{:02x}'.format(u8Manufacturer))
#     print('TimeOfProduction:    {}'.format(u32TimeOfProduction))
#     print('Tester:              0x{:02x}'.format(u8Tester))
#     print('TestResult:          0x{:02x}'.format(u8TestResult))
#     print('u32TimeOfTest:       {}'.format(u32TimeOfTest))

    
    theData = {
        "Product" : u32Product,
        "ProductName" : caProductName.decode('utf-8', errors='ignore').strip('\x00'),
        "SerialNumber" : caSerialNumber.decode('utf-8', errors='ignore').strip('\x00'),
        "Version" : [ u8Major, u8Minor, u8Build ],
        "Manufacturer" : u8Manufacturer,
        "TimeOfProduction" : u32TimeOfProduction,
        "Tester" : u8Tester,
        "TestResult" : u8TestResult,
        "TimeOfTest" : u32TimeOfTest,
        "OverlayName" : caOverlayName.decode('utf-8', errors='ignore').strip('\x00')
    }
    
    return theData
#    dataBlock = eeprom[8:256]
#    print("CRC32: 0x{:08x}".format(Crc32.calc(dataBlock)))
#    print()

def decodeGW4x00SpecificSection(eeprom):
    specificDataFormat = 'II6s'

    specificData = eeprom[256:256+calcsize(specificDataFormat)]
    u32Magic, u32Checksum, u8aMac = unpack(specificDataFormat, specificData)

    if u32Magic != EEPROM_MAGIC:
        raise WrongMagicError

    dataBlock = eeprom[256+8:256+256]
    if Crc32.calc(dataBlock) != u32Checksum:
        raise ChecksumError

 #   print('Specific data:')
 #   print('Magic:               0x{:08x}'.format(u32Magic))
 #   print('Check:               0x{:08x}'.format(u32Checksum))
 #   print('MAC:                 {:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(u8aMac[0],u8aMac[1],u8aMac[2],u8aMac[3],u8aMac[4],u8aMac[5]))

#    dataBlock = eeprom[256+8:256+256]
#    print("CRC32: 0x{:08x}".format(Crc32.calc(dataBlock)))

    theData = {
        "MAC" : [ u8aMac[0],u8aMac[1],u8aMac[2],u8aMac[3],u8aMac[4],u8aMac[5] ]
    }

    return theData

def readExpansionBoardEEPROM():
    eepromData = readEEPROM(EXPANSION_BOARD_EEPROM)
    theData = decodeCommonSection(eepromData)

    return theData

def readMainBoardEEPROM():
    eepromData = readEEPROM(MAIN_BOARD_EEPROM)
    theData = decodeCommonSection(eepromData)
    theData.update(decodeGW4x00SpecificSection(eepromData))

    return theData


def readDeviceData():
    theData = { "Main" : readMainBoardEEPROM() }
    if hasExpansionBoard():
        theData["Expansion"] = readExpansionBoardEEPROM()
    return theData