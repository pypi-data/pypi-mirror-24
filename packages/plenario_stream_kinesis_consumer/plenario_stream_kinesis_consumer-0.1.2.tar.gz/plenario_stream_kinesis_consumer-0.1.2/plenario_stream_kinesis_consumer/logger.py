from pygogo import Gogo
from pygogo.formatters import csv_formatter
from pygogo.handlers import file_hdlr

logger = Gogo(
    __name__,
    low_formatter=csv_formatter,
    low_hdlr=file_hdlr('worker.log'),
    high_formatter=csv_formatter,
    high_hdlr=file_hdlr('error.log')
).logger

debug = logger.debug
info = logger.info
warn = logger.warning
error = logger.error
critical = logger.critical
