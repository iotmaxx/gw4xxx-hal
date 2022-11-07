import json
import subprocess

def getSystemInfo():
    systemInfo = {}
    with open('/sys/bus/soc/devices/soc0/serial_number','r') as f:
        systemInfo['imx7_socid'] = f.readline().strip()
    systemInfo['IMEI'] = getIMEI()
    return systemInfo

def getIMEI():
    retVal = None
    try:
        modemList = json.loads(subprocess.run("mmcli -J -L".split(), stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1])['modem-list']
        if len(modemList) > 0:         # modem available
            modemInfo = json.loads(subprocess.run(['mmcli','-J','-m',modemList[0]], stdout=subprocess.PIPE).stdout.decode('utf-8'))
            retVal = modemInfo['modem']["generic"]["equipment-identifier"]
    except json.decoder.JSONDecodeError:
        pass
    return retVal

