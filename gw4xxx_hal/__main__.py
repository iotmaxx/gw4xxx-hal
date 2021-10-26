import gw4xxx.gw4xxx_eeprom
import gw4x90.analogIOControl
import gw4x90.currentLoopControl
import gw4x90.digitalInputControl
import gw4x00.digitalIOControl
import gw4x01.adcControl
import gw4x01.digitalIOControl
import sys 
import threading
import time

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

#print( gw4xxx.gw4xxx_eeprom.readExptheIsoOutputs[0].getInput(),ansionBoardEEPROM() )

#gw4x90.currentLoopControl.setOutputCurrent(int(sys.argv[1]),float(sys.argv[2]))

#print(gw4x90.currentLoopControl.getOutputCurrent(int(sys.argv[1])))

#gw4x90.currentLoopControl.powerDownChannel(int(sys.argv[1]))

#print(gw4x90.currentLoopControl.gettheIsoOutputs[0].getInput(),OutputCurrent(int(sys.argv[1])))

#gw4x90.analogIOControl.setVoltage(1, 2, float(sys.argv[1]))

#print (gw4x90.digitalInputControl.getInput(0))
#gw4x90.currentLoopControl.setOutputCurrent(0,float(sys.argv[1]))
#print(gw4x90.analogIOControl.readCurrentLoopInput())

# GW4100 GPI test start
""" 
inputs = []
for i in range(4):
    inputs.append(gw4x00.digitalIOControl.GW4100Input(i))

gw4x90.analogIOControl.setVoltage(0, 0, float(sys.argv[1]))
gw4x90.analogIOControl.setVoltage(0, 1, float(sys.argv[2]))
gw4x90.analogIOControl.setVoltage(0, 2, float(sys.argv[3]))
gw4x90.analogIOControl.setVoltage(0, 3, float(sys.argv[4]))
print('Inputs: {},{},{},{}'.format(inputs[0].getInput(),inputs[1].getInput(),inputs[2].getInput(),inputs[3].getInput()))
 """
# GW4100 GPI test end

# GW4100 GPIO test start
""" # set analog tester outputs to 0 (mandatory)
gw4x90.analogIOControl.setVoltage(1, 0, 0)
gw4x90.analogIOControl.setVoltage(1, 1, 0)

gpios = []
for i in range(2):
    gpios.append(gw4x00.digitalIOControl.GW4100Gpio(i))

gpios[0].setOutput("high")
gpios[1].setOutput("low")

print('Inputs: {},{}'.format(gw4x90.analogIOControl.readGPIOVoltage(0), gw4x90.analogIOControl.readGPIOVoltage(1) ))

gpios[0].setOutput("low")
gpios[1].setOutput("high")

print('Inputs: {},{}'.format(gw4x90.analogIOControl.readGPIOVoltage(0), gw4x90.analogIOControl.readGPIOVoltage(1) ))

gpios[0].setOutput("tri-state")
gpios[1].setOutput("tri-state")

print('Inputs: {},{}'.format(gw4x90.analogIOControl.readGPIOVoltage(0), gw4x90.analogIOControl.readGPIOVoltage(1) ))

gpios[0].activatePullup(True)
gpios[1].activatePullup(True)

print('Inputs: {},{}'.format(gw4x90.analogIOControl.readGPIOVoltage(0), gw4x90.analogIOControl.readGPIOVoltage(1) ))

gpios[0].activatePullup(False)
gpios[1].activatePullup(False)
gpios[0].setOutput("input")
gpios[1].setOutput("input")

gw4x90.analogIOControl.setVoltage(1, 0, 2)
gw4x90.analogIOControl.setVoltage(1, 1, 10)

print('GW4100 Inputs: {},{}'.format(gpios[0].getInput(),gpios[1].getInput() ))

gw4x90.analogIOControl.setVoltage(1, 0, 8)
gw4x90.analogIOControl.setVoltage(1, 1, 3)

print('GW4100 Inputs: {},{}'.format(gpios[0].getInput(),gpios[1].getInput() ))

gw4x90.analogIOControl.setVoltage(1, 0, 0)
gw4x90.analogIOControl.setVoltage(1, 1, 0)
 """
 # GW4100 GPIO test end

 # GW4101 current loop input tests start
""" 
theType = gw4xxx.gw4xxx_eeprom.getDeviceType()
if theType == 'GW4199':
    print('Tester')
    gw4x90.currentLoopControl.setOutputCurrent(int(sys.argv[1]),float(sys.argv[2]))
elif theType == 'GW4101':
    print('DUT')
    theADCControl = gw4x01.adcControl.GW4x01ADC()
    print(theADCControl.readCurrentLoop(int(sys.argv[1])))
 """
 # GW4101 current loop input tests end

# GW4101 RTD test start
theType = gw4xxx.gw4xxx_eeprom.getDeviceType()
""" 
if theType == 'GW4199':
    print('Tester')
elif theType == 'GW4101':
    print('DUT')
    theADCControl = gw4x01.adcControl.GW4x01ADC()
    for i in range (4):
        print(theADCControl.readRTDValue(i))
 """
 # GW4101 RTD test end

# GW4101 current loop output test start
""" 
theType = gw4xxx.gw4xxx_eeprom.getDeviceType()
if theType == 'GW4199':
    print('Tester')
    print("Current: {}".format(gw4x90.analogIOControl.readCurrentLoopInput()))
    print("1-wire voltage: {}".format(gw4x90.analogIOControl.readOneWireVoltage()))
elif theType == 'GW4101':
    print('DUT')
    theADCControl = gw4x01.adcControl.GW4x01ADC()
    theADCControl.setOutputCurrent(float(sys.argv[1]))
    print("Current: {}".format(theADCControl.getOutputCurrent()))
 """
 # GW4101 current loop output test end

# GW4101 iso input tests start
""" 
theType = gw4xxx.gw4xxx_eeprom.getDeviceType()
if theType == 'GW4199':
    print('Tester')
    gw4x90.analogIOControl.setVoltage(3,0,10)
    gw4x90.analogIOControl.setVoltage(3,1,0)
    gw4x90.analogIOControl.setVoltage(3,2,10)
    gw4x90.analogIOControl.setVoltage(3,3,0)
elif theType == 'GW4101':
    print('DUT')
    theIsoInputs = [
        gw4x01.digitalIOControl.GW4x01IsoInput(0),
        gw4x01.digitalIOControl.GW4x01IsoInput(1),
        gw4x01.digitalIOControl.GW4x01IsoInput(2),
        gw4x01.digitalIOControl.GW4x01IsoInput(3)
    ]
    print("Iso Inputs: {} {} {} {}".format(theIsoInputs[0].getInput(),theIsoInputs[1].getInput(),theIsoInputs[2].getInput(),theIsoInputs[3].getInput() ))
 """
# GW4101 iso input tests end

# GW4101 iso output tests start
""" 
theType = gw4xxx.gw4xxx_eeprom.getDeviceType()
if theType == 'GW4199':
    print('Tester')
    gw4x90.analogIOControl.setVoltage(1,2,0)
    gw4x90.analogIOControl.setVoltage(1,3,0)
    print("Inputs: {} {}".format(gw4x90.digitalInputControl.getInput(0), gw4x90.digitalInputControl.getInput(1)))
    gw4x90.analogIOControl.setVoltage(1,2,0)
    gw4x90.analogIOControl.setVoltage(1,3,0)
    # add GW4101 iso out and digital in
elif theType == 'GW4101':
    print('DUT')
    theIsoOutputs = [
        gw4x01.digitalIOControl.GW4x01IsoOutput(0),
        gw4x01.digitalIOControl.GW4x01IsoOutput(1),
    ]
    theIsoOutputs[0].setOutput(1)
    theIsoOutputs[1].setOutput(1)    
 """
 # GW4101 iso output tests end

# GW4101 digital in tests start
""" 
theType = gw4xxx.gw4xxx_eeprom.getDeviceType()
if theType == 'GW4199':
    print('Tester')
    gw4x90.analogIOControl.setVoltage(2,0,0)
    gw4x90.analogIOControl.setVoltage(2,1,10)
    gw4x90.analogIOControl.setVoltage(2,2,0)
    gw4x90.analogIOControl.setVoltage(2,3,10)
elif theType == 'GW4101':
    print('DUT')
    theInputs = [
        gw4x01.digitalIOControl.GW4x01Input(0),
        gw4x01.digitalIOControl.GW4x01Input(1),
        gw4x01.digitalIOControl.GW4x01Input(2),
        gw4x01.digitalIOControl.GW4x01Input(3)
    ]
    print("Inputs: {} {} {} {}".format(theInputs[0].getInput(),theInputs[1].getInput(),theInputs[2].getInput(),theInputs[3].getInput() ))
 """
 # GW4101 digital in tests end

# GW4100 counter test start
gpio = gw4x00.digitalIOControl.GW4100Gpio(0)
gpi = gw4x00.digitalIOControl.GW4100CounterInput(0)

gpi.startCounter()

def outputThread(numPulses, sleepTime):
    for i in range(numPulses):
        time.sleep(sleepTime/2)
        gpio.setOutput("high")
        time.sleep(sleepTime/2)
        gpio.setOutput("low")

x = threading.Thread(target=outputThread, args=(int(sys.argv[1]),float(sys.argv[2],)))
x.start()
print("Counter start: {}".format(gpi.getCounter()))
time.sleep(0.01)
print("Counter  0.01s: {}".format(gpi.getCounter()))
time.sleep(0.09)
print("Counter  0.1s: {}".format(gpi.getCounter()))
x.join()
print("Counter   end: {}".format(gpi.getCounter()))

# GW4100 counter test end
