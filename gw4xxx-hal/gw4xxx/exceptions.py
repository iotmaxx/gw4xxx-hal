class GW4xxxError(Exception):
    """Base class for GW4xxx exceptions"""
    pass

class EEPROMSizeError(GW4xxxError):
    """Raised when the EEPROM size is too small (no expansion board or no overlay loaded)"""
    pass

class WrongMagicError(GW4xxxError):
    """Raised when the EEPROM magic number is wrong (e.g. EEPROM not programmed)"""
    pass

class ChecksumError(GW4xxxError):
    """Raised when the EEPROM checksum number is wrong (e.g. EEPROM not programmed)"""
    pass


