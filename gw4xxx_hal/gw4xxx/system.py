
def getSystemInfo():
    systemInfo = {}
    with open('/sys/bus/soc/devices/soc0/serial_number','r') as f:
        systemInfo['imx7.socid'] = f.readline().strip()
    return systemInfo



