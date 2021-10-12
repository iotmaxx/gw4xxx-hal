import gw4xxx.gw4xxx_eeprom


gw4100CommonData = {
    'SerialNumber': 'GW00002086',
    'OverlayName': 'none',
    'Version': [ 1, 9, 0 ],
    'Product': 0x1,
    'ProductName': 'GW4100',
    'Manufacturer': 0,
    'Tester': 0,
    'TestResult': 0,
    'TimeOfProduction': 0,
    'TimeOfTest': 0
}
# 'MAC': [48, 73, 80, 231, 163, 124]}
gw4100SpecificData = {
    'MAC': [48, 73, 80, 231, 163, 224]
}

gw4x01CommonData = {
    'Product': 17, 
    'ProductName': 'GW4x01', 
    'SerialNumber': 'none', 
    'Version': [1, 5, 0], 
    'Manufacturer': 2, 
    'TimeOfProduction': 1619450598, 
    'Tester': 0, 
    'TestResult': 1, 
    'TimeOfTest': 1619450598, 
    'OverlayName': 'sensexp01'
}

gw4x01CommonDataTest1 = {
    'Product': 17, 
    'ProductName': 'GW4x01', 
    'SerialNumber': 'abcdef', 
    'Version': [1, 5, 0], 
    'Manufacturer': 2, 
    'TimeOfProduction': 9450598, 
    'Tester': 0, 
    'TestResult': 7, 
    'TimeOfTest': 1619498, 
    'OverlayName': 'sensexp01'
}

gw4x01CommonDataTest2 = {
    'Manufacturer': 2, 
    'TimeOfProduction': 598, 
    'Tester': 0, 
    'TestResult': 3, 
    'TimeOfTest': 1618, 
}

gw4100CommonDataTest1 = {
    'Tester': 3,
    'TestResult': 1,
    'TimeOfProduction': 12345678,
    'TimeOfTest': 123454321
}



print( gw4xxx.gw4xxx_eeprom.readExpansionBoardEEPROM() )

gw4xxx.gw4xxx_eeprom.writeExpansionBoardEEPROM(gw4x01CommonDataTest1)

print( gw4xxx.gw4xxx_eeprom.readExpansionBoardEEPROM() )

gw4xxx.gw4xxx_eeprom.writeExpansionBoardEEPROM(gw4x01CommonDataTest2)

print( gw4xxx.gw4xxx_eeprom.readExpansionBoardEEPROM() )

gw4xxx.gw4xxx_eeprom.writeExpansionBoardEEPROM(gw4x01CommonData)

print( gw4xxx.gw4xxx_eeprom.readExpansionBoardEEPROM() )

