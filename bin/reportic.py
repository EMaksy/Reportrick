import argparse
import logging
from logging.config import dictConfig
from pickle import TRUE
import sys
import datetime
from datetime import date

__version__ = "0.1.0"
__author__ = "Eugen Maksymenko <eugen.maksymenko@gmx.net>"


class MissingSubCommand(ValueError):
    pass


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

    args = parser.parse_args(args=cliargs)
    # Setup logging and the log level according to the "-v" option
    dictConfig(DEFAULT_LOGGING_DICT)
    log.setLevel(LOGLEVELS.get(args.verbose, logging.DEBUG))

    log.debug("CLI result: %s", args)

    # help for the user when no subcommand was passed
    if "func" not in args:
        cli_menue()
        # parser.print_help()
        #raise MissingSubCommand("Expected subcommand")

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
        # do some useful things here...
        # If everything was good, return without error:
        return 0

    except MissingSubCommand as error:
        log.fatal(error)
        return 888


def get_time_strings():
    """Get current time, date and KW as return values"""
    log.info("Cli get_time was executed")
    today = date.today()
    formated_date = today.strftime("%d:%m:%Y")
    current_time = today.strftime("%H:%M:%S")
    calendar_week = datetime.date.today().isocalendar()[1]
    return current_time, formated_date, calendar_week,


def check_day_evening(current_time):
    log.info("Cli check_day_evening was executed")
    print(type(current_time))


def cli_menue() -> bool:
    """Display User Interface in the Command Line"""
    log.info("Cli menue function call")
    current_time, date, calendar_week = get_time_strings()

    print(f"Good day ")
    print(f"Today is {date}")
    print(f"We have the {calendar_week} KW")
    return TRUE


if __name__ == "__main__":
    sys.exit(main())
