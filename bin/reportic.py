import argparse
from calendar import calendar
import logging
from logging.config import dictConfig
from pickle import TRUE
import sys
from datetime import datetime

__version__ = "0.1.0"
__author__ = "Eugen Maksymenko <eugen.maksymenko@gmx.net>"


# Logging module
DEFAULT_LOGGING_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {'format': '[%(levelname)s] %(funcName)s: %(message)s'},
    },
    'handlers': {
        'default': {
            'level': 'NOTSET',  # will be set later
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        __name__: {
            'handlers': ['default'],
            'level': 'INFO',
            # 'propagate': True
        }
    }
}
#: Map verbosity level (int) to log level
LOGLEVELS = {None: logging.WARNING,  # 0
             0: logging.ERROR,
             1: logging.WARNING,
             2: logging.INFO,
             3: logging.DEBUG,
             }
#: Instantiate our logger
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def parsecli(cliargs=None) -> argparse.Namespace:
    """Parse CLI with :class:`argparse.ArgumentParser` and return parsed result
    :param cliargs: Arguments to parse or None (=use sys.argv)
    :return: parsed CLI result
    """
    parser = argparse.ArgumentParser(description=__doc__,
                                     epilog="Version %s written by %s " % (
                                         __version__, __author__)
                                     )

    parser.add_argument('-v', '--verbose',
                        action='count',
                        default=0,
                        help="increase verbosity level")

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + __version__
                        )
    parser.add_argument("DIR",
                        help="Searches the directory for files"
                        )

    args = parser.parse_args(args=cliargs)
    # Setup logging and the log level according to the "-v" option
    dictConfig(DEFAULT_LOGGING_DICT)
    log.setLevel(LOGLEVELS.get(args.verbose, logging.DEBUG))

    log.debug("CLI result: %s", args)
    return args


def main(cliargs=None) -> int:
    """Entry point for the application script
    :param cliargs: Arguments to parse or None (=use :class:`sys.argv`)
    :return: error code
    """

    try:
        args = parsecli(cliargs)
        cli_menue(args)
        # do some useful things here...
        # If everything was good, return without error:
        log.info("I'm an info message")
        log.debug("I'm a debug message.")
        log.warning("I'm a warning message.")
        log.error("I'm an error message.")
        log.fatal("I'm a really fatal massage!")
        return 0

    # List possible exceptions here and return error codes
    except Exception as error:  # FIXME: add a more specific exception here!
        log.fatal(error)
        # Use whatever return code is appropriate for your specific exception
        return 10


def get_time_strings():
    """Get current time, date and KW as return values"""
    log.info("Cli get_time was executed")
    now = datetime.now()
    date = now.strftime("%d:%m:%Y")
    current_time = now.strftime("%H:%M:%S")
    calendar_week = datetime.date.today().isocalendar()[1]
    return current_time, date, calendar_week,


def check_day_evening(current_time):
    log.info("Cli check_day_evening was executed")
    print(type(current_time))


def cli_menue(args) -> bool:
    """Display User Interface in the Command Line"""
    log.info("Cli menue function call")
    current_time, date, calendar_week = get_time_strings()

    print(f"Good day")
    print(f"Today is {date}")
    print(f"We have the {calendar_week} KW")
    return TRUE


if __name__ == "__main__":
    sys.exit(main())
