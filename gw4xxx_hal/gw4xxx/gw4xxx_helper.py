""" helper functions for all gateway versions """
import logging
import socket
import shutil
from pathlib import Path

DEFAULT_HOSTNAME = "Gateway"
HOSTNAME_FILE = "hostname"
HOSTS_FILE = "hosts"

CONFIG_ETC_PATH = Path("/config/etc")

log = logging.getLogger(__name__)

def setSerialNumberAsHostname(serialNumber, force=False):
    """ set gateway hostname to it's serial number"""
    if not force:
        hostname = socket.gethostname()
        if hostname != DEFAULT_HOSTNAME:
            log.warning("keeping non default hostname: '%s'", hostname)
            return
    configHostsLines = []
    hostsFile = CONFIG_ETC_PATH / HOSTS_FILE
    hostnameFile = CONFIG_ETC_PATH / HOSTNAME_FILE
#    serialNumber = getGatewaySerialNumber()
    if serialNumber == 'Unknown':
        return
    if not hostnameFile.exists():
        log.error("%s not found.", hostnameFile)
        return
    if not Path(hostsFile).exists():
        log.error("%s not found.", hostsFile)
        return
    with open(hostsFile, "r", encoding='ascii') as f:
        configHostsLines = f.readlines()
    shutil.move(hostsFile,hostsFile.with_suffix('.bak'))
    with open(hostsFile, "w", encoding='ascii') as f:
        for line in configHostsLines:
            tokens = line.split()
            if not tokens[0] == '127.0.1.1':
                f.write(line)
            else:
                tokens[1] = serialNumber
                for idx,url in enumerate(tokens[2:], start=2):
                    urlTokens = url.split('.')
                    if urlTokens[0].lower() == DEFAULT_HOSTNAME.lower():
                        urlTokens[0] = serialNumber
                    tokens[idx] = '.'.join(urlTokens)
                newHostsLine = '\t'.join(tokens)
                f.write(newHostsLine+'\n')
    with open(hostnameFile, "w", encoding='ascii') as f:
        f.write(serialNumber)
