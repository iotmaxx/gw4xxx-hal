import logging
import time
#from systemd.journal import JournalHandler

logFmt = '%(asctime)s %(levelname)-6s %(threadName)-11s: %(message)s'
logger = logging.getLogger()

ch = logging.StreamHandler()
formatter = logging.Formatter(logFmt)
formatter.converter = time.gmtime

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
#logger.addHandler(JournalHandler())

logger.setLevel(logging.DEBUG)

