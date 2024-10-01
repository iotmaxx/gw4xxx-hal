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

EEPROM_MAGIC                    = 0xc4ec31b6
EEPROM_SIZE                     = 8*1024
EEPROM_COMMON_SECTION_SIZE      = 256
EEPROM_SPECIFIC_SECTION_SIZE    = 256
# todo: switch back to correct eeprom path
MAIN_BOARD_EEPROM       = '/sys/bus/i2c/devices/2-0050/eeprom'
#MAIN_BOARD_EEPROM       = '/data/eeprom.file'
EXPANSION_BOARD_EEPROM  = '/sys/bus/i2c/devices/3-0050/eeprom'
#EXPANSION_BOARD_EEPROM  = '/data/expEeprom.file'

GW4xxxCommonSectionContent = { "Product", "ProductName", "SerialNumber", "Version", "Manufacturer", "TimeOfProduction" ,"Tester", "TestResult", "TimeOfTest", "OverlayName" }
GW4x00SpecificSectionContent = { "MAC" }

sectionHeaderFormat = 'II'
commonDataFormat = '16sI4s16s16sBIBBI'
specificDataFormat = '6sI'
versionDataFormat = '3Bx'

gw4100NoEEPROMData = {
    "Product" : 0,
    "ProductName" : "Unknown",
    "SerialNumber" : "Unknown",
    "Version" : [ 0, 0, 0 ],
    "Manufacturer" : 0,
    "TimeOfProduction" : 0,
    "Tester" : 0,
    "TestResult" : 0,
    "TimeOfTest" : 0,
    "OverlayName" : "None",
    "MAC" : [ 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF ]
}

gw4xxxNoEEPROMData = {
    "Product" : 0,
    "ProductName" : "Unknown",
    "SerialNumber" : "Unknown",
    "Version" : [ 0, 0, 0 ],
    "Manufacturer" : 0,
    "TimeOfProduction" : 0,
    "Tester" : 0,
    "TestResult" : 0,
    "TimeOfTest" : 0,
    "OverlayName" : "None",
}

def hasExpansionBoard():
    return os.path.isfile(EXPANSION_BOARD_EEPROM) 

def readEEPROM(eepromFile):
    if os.path.getsize(eepromFile) < EEPROM_SIZE:
        raise EEPROMSizeError

    with open(eepromFile, "rb") as f:
        eeprom = f.read(EEPROM_SIZE)

    return eeprom
  

def decodeCommonSection(eeprom):
    commonData = eeprom[:calcsize(sectionHeaderFormat+commonDataFormat)]
    u32Magic, u32Checksum, caOverlayName, u32Product, uVersion, caProductName, caSerialNumber, u8Manufacturer, u32TimeOfProduction, u8Tester, u8TestResult, u32TimeOfTest = unpack(sectionHeaderFormat+commonDataFormat, commonData)
    u8Major, u8Minor, u8Build = unpack('3Bx', uVersion)

    if u32Magic != EEPROM_MAGIC:
#        print("Wrong magic c")
        raise WrongMagicError

    dataBlock = eeprom[8:256]
    if Crc32.calc(dataBlock) != u32Checksum:
#        print("Wrong check c")
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

    specificData = eeprom[256:256+calcsize(sectionHeaderFormat+specificDataFormat)]
    u32Magic, u32Checksum, u8aMac, u32Padding = unpack(sectionHeaderFormat+specificDataFormat, specificData)

    if u32Magic != EEPROM_MAGIC:
#        print("Wrong magic s")
        raise WrongMagicError

    dataBlock = eeprom[256+8:256+256]
    if Crc32.calc(dataBlock) != u32Checksum:
#        print("Wrong check s")
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
    try:
        theData = decodeCommonSection(eepromData)
#        print(f"Decode: {theData}")
    except (WrongMagicError, ChecksumError) as error:
        theData = gw4xxxNoEEPROMData
    return theData

def readMainBoardEEPROM():
    eepromData = readEEPROM(MAIN_BOARD_EEPROM)
    try:
        theData = decodeCommonSection(eepromData)
        theData.update(decodeGW4x00SpecificSection(eepromData)) 
    except (WrongMagicError, ChecksumError) as error:
        theData = gw4100NoEEPROMData
    return theData

def readDeviceData():
    theData = { "Main" : readMainBoardEEPROM() }
    deviceType = theData['Main']['ProductName']
    if hasExpansionBoard():
        theData["Expansion"] = readExpansionBoardEEPROM()
        deviceType = deviceType[0:4] + theData['Expansion']['ProductName'][-2:]
    theData["device"] = deviceType
    return theData

def writeCommonSection(eepromFile, commonData):
    myData = bytearray(b'\xFF') * EEPROM_COMMON_SECTION_SIZE
    pack_into(commonDataFormat, myData, 8, 
        commonData['OverlayName'].encode(), 
        commonData['Product'], 
        pack(versionDataFormat, commonData['Version'][0], commonData['Version'][1], commonData['Version'][2]), 
        commonData['ProductName'].encode(), 
        commonData['SerialNumber'].encode(), 
        commonData['Manufacturer'], 
        commonData['TimeOfProduction'], 
        commonData['Tester'], 
        commonData['TestResult'], 
        commonData['TimeOfTest']
    )
    u32CRC = Crc32.calc(myData[8:EEPROM_COMMON_SECTION_SIZE])
    pack_into(sectionHeaderFormat, myData, 0, EEPROM_MAGIC, u32CRC)
    with open(eepromFile, "rb+") as f:
        f.write(myData)

def writeGW4x00SpecificSection(eepromFile, specificData):
    myData = bytearray(b'\xFF') * EEPROM_SPECIFIC_SECTION_SIZE
    pack_into(specificDataFormat, myData, 8, 
        bytearray(specificData['MAC']),0
    )
    u32CRC = Crc32.calc(myData[8:EEPROM_SPECIFIC_SECTION_SIZE])
    pack_into(sectionHeaderFormat, myData, 0, EEPROM_MAGIC, u32CRC)
    with open(eepromFile, "rb+") as f:
        f.seek(EEPROM_COMMON_SECTION_SIZE,0)
        f.write(myData)
 
def writeMainBoardEEPROM(commonSection, specificSection=None):
    if commonSection != None:
    # all parameters set -> write whole section
        if GW4xxxCommonSectionContent <= set(commonSection):
            writeCommonSection(MAIN_BOARD_EEPROM, commonSection)    
        else:    # not all parameters set -> update section
            theData = readMainBoardEEPROM()
            theData.update(commonSection)
            writeCommonSection(MAIN_BOARD_EEPROM, theData)    

    if specificSection != None:
        if GW4x00SpecificSectionContent <= set(specificSection):
            writeGW4x00SpecificSection(MAIN_BOARD_EEPROM, specificSection)
        else:   # only one parameter defined so skip this for now
            pass

def writeExpansionBoardEEPROM(commonSection, specificSection=None):
    if commonSection != None:
        # all parameters set -> write whole section
        if GW4xxxCommonSectionContent <= set(commonSection):
#            theData = readExpansionBoardEEPROM()
#            theData.update(commonSection)
#            print(f"write full section {theData}")
            writeCommonSection(EXPANSION_BOARD_EEPROM, commonSection)    
#            writeCommonSection(EXPANSION_BOARD_EEPROM, theData)    
        else:    # not all parameters set -> update section
            theData = readExpansionBoardEEPROM()
            theData.update(commonSection)
#            print(f"update section {theData}")
            writeCommonSection(EXPANSION_BOARD_EEPROM, theData)    

    # no expansion boards with specific section defined yet so ignore parameter

def getDeviceType():
    deviceData = readDeviceData()
    deviceType = deviceData['Main']['ProductName']
    if 'Expansion' in deviceData:
        deviceType = deviceType[0:4] + deviceData['Expansion']['ProductName'][-2:]
    return deviceType

