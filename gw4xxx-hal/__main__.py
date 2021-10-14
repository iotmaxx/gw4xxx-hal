import gw4xxx.gw4xxx_eeprom
import gw4x90.analogIOControl
import gw4x90.currentLoopControl
import gw4x90.digitalInputControl
import gw4x00.digitalIOControl
import sys 

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

gw4x99CommonData = {
    'Product': 240, 
    'ProductName': 'GW4x99', 
    'SerialNumber': 'none', 
    'Version': [1, 1, 0], 
    'Manufacturer': 3, 
    'TimeOfProduction': 1609455600, 
    'Tester': 0, 
    'TestResult': 0, 
    'TimeOfTest': 0, 
    'OverlayName': 'none'
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



#print( gw4xxx.gw4xxx_eeprom.readExpansionBoardEEPROM() )

#gw4xxx.gw4xxx_eeprom.writeExpansionBoardEEPROM(gw4x99CommonData)

#print( gw4xxx.gw4xxx_eeprom.readExpansionBoardEEPROM() )

#gw4xxx.gw4xxx_eeprom.writeExpansionBoardEEPROM(gw4x01CommonDataTest2)

#print( gw4xxx.gw4xxx_eeprom.readExpansionBoardEEPROM() )

#gw4xxx.gw4xxx_eeprom.writeExpansionBoardEEPROM(gw4x01CommonData)

#print( gw4xxx.gw4xxx_eeprom.readExpansionBoardEEPROM() )

#gw4x90.currentLoopControl.setOutputCurrent(int(sys.argv[1]),float(sys.argv[2]))

#print(gw4x90.currentLoopControl.getOutputCurrent(int(sys.argv[1])))

#gw4x90.currentLoopControl.powerDownChannel(int(sys.argv[1]))

#print(gw4x90.currentLoopControl.getOutputCurrent(int(sys.argv[1])))

#gw4x90.analogIOControl.setVoltage(1, 2, float(sys.argv[1]))
#print (gw4x90.digitalInputControl.getInput(0))
#gw4x90.currentLoopControl.setOutputCurrent(0,float(sys.argv[1]))
#print(gw4x90.analogIOControl.readCurrentLoopInput())

inputs = []
for i in range(4):
    inputs.append(gw4x00.digitalIOControl.GW4100Input(i))

gw4x90.analogIOControl.setVoltage(2, 0, float(sys.argv[1]))
gw4x90.analogIOControl.setVoltage(2, 1, float(sys.argv[2]))
gw4x90.analogIOControl.setVoltage(2, 2, float(sys.argv[3]))
gw4x90.analogIOControl.setVoltage(2, 3, float(sys.argv[4]))
print('Inputs: {},{},{},{}'.format(inputs[0].getInput(),inputs[1].getInput(),inputs[2].getInput(),inputs[3].getInput()))
