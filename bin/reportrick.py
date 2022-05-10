import argparse
import logging
from logging.config import dictConfig
import sys
import datetime
from datetime import date
import time
import os
import reportrick_database_class
import reportrick_generate

# GLOBALS
__version__ = "0.1.0"
__author__ = "Eugen Maksymenko <eugen.maksymenko@gmx.net>"
# relative dir for the database
relative_path_to_project = (f"{os.path.dirname(__file__)}/..")
file_dir_database = "/database"
relative_file = "/reportrick_database.sqlite"
DATABASEPATH = relative_path_to_project + file_dir_database + relative_file
# DATE
YEAR = str(date.today().year)
CALENDER_WEEK = str(datetime.date.today().isocalendar()[1])


class MissingSubCommand(ValueError):
    pass


class CategoryError():
    pass


class bcolors:
    """Colors for Terminal output"""
    RED = '\033[31m'
    YELLOW = '\u001b[33m'
    GREEN = '\033[92m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# command list
CMD_LIST = ["Add new entry",
            "Change calendar week or the year",
            "Show work report",
            "Export work report",
            "Configure user data",
            "Exit the program",
            ]

CATEGORY_LIST = ["GREEN", "AMBER", "RED", "MEETING"]

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

    # Add a new sub command with addiotan arguments "ADD a new entry by category"
    subparsers = parser.add_subparsers(help='Available sub commands')
    parser_add = subparsers.add_parser(
        "add", help="adds a new entry to your day")
    parser_add.set_defaults(func=cmd_add)
    parser_add.add_argument(
        "category", type=str, help="Choose a Category [red, amber, green, meeting] in which the entry needs to be added")
    parser_add.add_argument(
        "entry", type=str, help="Add a new entry which describes the activity")

    args = parser.parse_args(args=cliargs)
    # Setup logging and the log level according to the "-v" option
    dictConfig(DEFAULT_LOGGING_DICT)
    log.setLevel(LOGLEVELS.get(args.verbose, logging.DEBUG))

    log.debug("CLI result: %s", args)

    # help for the user when no subcommand was passed
    if "func" not in args:
        # Create directory and create the dabase if no database exists
        if os.path.exists(DATABASEPATH) != True:
            create_database_dir()
            create_database()
        cli_menue()

    # Setup logging and the log level according to the "-v" option
    dictConfig(DEFAULT_LOGGING_DICT)
    log.setLevel(LOGLEVELS.get(args.verbose, logging.DEBUG))
    log.debug("CLI result: %s", args)

    return args


def cmd_add(args):
    """
    Add an entry to the current workreport
    The given args object contains the Category and the Entry which sould be added to the database.
    """
    log.debug("add selected")
    CATEGORY_LIST
    print(args)
    if args.category in CATEGORY_LIST:
        date_obj, date_formatted, calender_week = get_time_strings()
        log.debug(
            f" {args.category}, {args.entry}, Date2: {date_formatted} CalenderWeekNumber: {calender_week}")
        # Opens the database and add adds the entry
        sql_database = reportrick_database_class.Database(DATABASEPATH)
        sql_database.set_entry_table(
            args.category, args.entry, calender_week, date_formatted)
    else:
        print("Wrong category")


def create_database():
    """Create empty database"""
    log.debug("create_database()")
    sql_data = None
    sql_database = reportrick_database_class.Database(DATABASEPATH, sql_data)
    # sql_database.close


def create_database_dir():
    """Create a relative directory for the reportrick database"""
    # log.debug(DATABASEPATH)
    try:
        os.mkdir(f"../{file_dir_database}")
        log.debug(f"Directory  created at{DATABASEPATH}")
    except:
        log.error(f"Path {DATABASEPATH} was not created")


def get_time_strings():
    """Get current time, date and KW as return values"""
    log.debug("get_time_strings() was executed")
    today = date.today()
    formated_date = today.strftime("%Y-%m-%d")
    current_time = time.localtime()
    calendar_week = datetime.date.today().isocalendar()[1]
    return current_time, formated_date, calendar_week,


def check_day_evening(current_time_obj):
    """Function for checking if its day or evening"""
    log.debug("check_day_evening was executed")
    if current_time_obj.tm_hour >= 17:
        return "evening"
    else:
        return "day"


def cli_commands_sub_menue() -> bool:
    """Numbers and outputs elements of all CMDS Strings"""
    log.debug("cli_commands_sub_menue was executed")
    cmd_list_counter = 1
    for x in CMD_LIST:
        print(f"{cmd_list_counter}:{x}")
        cmd_list_counter += 1
    return True


def cli_menue() -> bool:
    """Display User Interface in the Command Line"""
    log.debug("cli_menue() was executed")
    current_time, date, calendar_week = get_time_strings()
    # check if its day or evening

    print(
        f"Good {check_day_evening(current_time)}\nToday is {date}\nCalendar Week: {calendar_week}\n")

    cli_commands_sub_menue()
    # run user input looop
    cli_menue_interface()
    return True


def cli_menue_interface():
    """Handles the user interaction with the command line menu"""

    log.debug("cli_menue_interface() was executed")
    while True:
        menue_selector_number = input("Choose an option: ")
        if menue_selector_number == "6":
            # Ends the programm
            clean_console()
            quit()
        if menue_selector_number == "5":
            # Configuration of the user
            clean_console()
            cli_menue_config_user()

        if menue_selector_number == "4":
            # Creates the report in the required format
            clean_console()
            cli_generate_html_or_pdf()
            cli_menue_return()

        if menue_selector_number == "3":
            # List all entries for this week
            cli_week_report()
        if menue_selector_number == "2":
            # Changes the current year and calenderweek. Also returns back to the main menu
            clean_console()
            cli_change_global_date()
            cli_menue_return()
        if menue_selector_number == "1":
            # Adds new entries to database
            clean_console()
            cli_add_entry()


def cli_generate_html_or_pdf():
    """Ask user if pdf or html should be created"""
    # collect all data for file generation
    list_meetings_enries, list_green_entries, list_amber_entries, list_red_entries, list_team_data, list_user_data, list_time_data, list_user_data = collect_workreport_data()
    # get user data for function call
    while True:

        user_choice = input(
            "Input which file format should be generated?\n1:HTML\n2:PDF\n3:HTML and PDF\n4:Text\n")
        if user_choice == "1" or user_choice == "HTML":
            reportrick_generate.generate_html(list_meetings_enries, list_green_entries, list_amber_entries,
                                              list_red_entries, list_team_data, list_user_data, list_time_data)
            break
        if user_choice == "2" or user_choice == "PDF":
            reportrick_generate.generate_pdf(list_meetings_enries, list_green_entries, list_amber_entries,
                                             list_red_entries, list_team_data, list_user_data, list_time_data)
            break
        if user_choice == "3" or user_choice == "HTML and PDF":
            reportrick_generate.generate_html_and_pdf(list_meetings_enries, list_green_entries, list_amber_entries,
                                                      list_red_entries, list_team_data, list_user_data, list_time_data)
            break
        if user_choice == "4" or user_choice == "TEXT":
            break
        else:
            print("Sorry wrong input")


def collect_workreport_data() -> list:
    """ Collect all required user data for workreport"""

    sql_data = reportrick_database_class.Database(DATABASEPATH)
    first_name, last_name, team_name = sql_data.get_user_table()
    global YEAR, CALENDER_WEEK
    current_calender_week = CALENDER_WEEK
    current_year = YEAR

    list_time_data = [YEAR, CALENDER_WEEK]

    list_user_data = [first_name, last_name]
    list_team_data = [team_name]

    list_meetings_enries = format_list_and_return(list(sql_data.get_entries_meeting_week_year(
        current_calender_week, current_year)))
    list_green_entries = format_list_and_return(list(sql_data.get_entries_green_week_year(
        current_calender_week, current_year)))
    list_amber_entries = format_list_and_return(list(sql_data.get_entries_amber_week_year(
        current_calender_week, current_year)))
    list_red_entries = format_list_and_return(list(sql_data.get_entries_red_week_year(
        current_calender_week, current_year)))

    return list_meetings_enries, list_green_entries, list_amber_entries, list_red_entries, list_team_data, list_user_data, list_time_data, list_user_data


def cli_change_global_date():
    """Change Dates of an workreport"""
    global YEAR, CALENDER_WEEK
    YEAR = input("Enter the year for the workreport  ")
    CALENDER_WEEK = input("Please input the CALENDER WEEK  ")
    print(
        f"Year was changed to {YEAR} and Calender Week was changed to {CALENDER_WEEK}")
    print(YEAR, CALENDER_WEEK)


def cli_menue_config__user_output():
    """
    Output the current first/last name and team on the console
    """
    sql_database = reportrick_database_class.Database(DATABASEPATH)
    first_name, last_name, team_name = reportrick_database_class.Database.get_user_table(
        sql_database)

    print(
        f"Current first Name: {first_name}\nCurrent last  Name: {last_name}\nCurrent Team  Name: {team_name}\n")


def cli_menue_config_user():
    """User input of the config name"""
    # get current user data from database
    sql_database = reportrick_database_class.Database(DATABASEPATH)
    cli_menue_config__user_output()

    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    team_name = input("Enter your Team name: ")
    try:
        sql_database.set_user_table(first_name, last_name, team_name)
        print("Changes have been made to the database")
        clean_console()
        cli_menue_config__user_output()

    except Exception as e:
        log.debug(f"""
                Error message: {e}
                cli_menue_config_user()
                Changes have not been adopted to the database!
                """)
    cli_menue_return()


def format_list_print(entry_list):
    """A given list of date is formated"""
    counter = 1
    for x in entry_list:
        string_x = str(x)
        string_x = string_x.replace(",", "")
        string_x = string_x.replace("('", "")
        string_x = string_x.replace("')", "")
        print(f"{counter}:{string_x}")
        counter += 1


def format_list_and_return(entry_list) -> list:
    """A given list is formed and returned"""
    cleaned_list = []
    for x in entry_list:
        string_x = str(x)
        string_x = string_x.replace(",", "")
        string_x = string_x.replace("('", "")
        string_x = string_x.replace("')", "")
        cleaned_list.append(string_x)
    return cleaned_list


def cli_week_report():
    """List current workreport"""
    sql_data = reportrick_database_class.Database(DATABASEPATH)
    first_name, last_name, team_name = sql_data.get_user_table()

    global YEAR, CALENDER_WEEK
    current_calender_week = CALENDER_WEEK
    current_year = YEAR

    list_green_entries = list(sql_data.get_entries_green_week_year(
        current_calender_week, current_year))
    list_red_entries = list(sql_data.get_entries_red_week_year(
        current_calender_week, current_year))
    list_amber_entries = list(sql_data.get_entries_amber_week_year(
        current_calender_week, current_year))
    list_meetings_enries = list(sql_data.get_entries_meeting_week_year(
        current_calender_week, current_year))

    # clean console
    log.debug("cli_week_report() was executed")
    clean_console()
    print("Weekly Report")
    print(f"KW {datetime.date.today().isocalendar()[1]}")
    print(f"Name: {first_name} {last_name}     Team: {team_name}")
    print(f"{bcolors.RED}Red:{bcolors.ENDC}")
    format_list_print(list_red_entries)
    print(f"{bcolors.GREEN}Green:{bcolors.ENDC}")
    format_list_print(list_green_entries)
    print(f"{bcolors.YELLOW}Amber:{bcolors.ENDC}")
    format_list_print(list_amber_entries)
    print(f"{bcolors.OKBLUE}Meetings:{bcolors.ENDC}")
    format_list_print(list_meetings_enries)
    cli_menue_return_workreport()


def cli_menue_return():
    while True:
        return_to_main_menue = input(
            "Enter 'b' to return to main menue or press 'e' to exit  ")
        if return_to_main_menue == "b":
            # clean and return to main menue
            cli_return_to_cli_menue()
            break
        if return_to_main_menue == "e":
            # clean and end programm
            clean_console()
            quit()


def cli_menue_return_workreport():
    text_options = "Enter 'b' to return to main menue\nPress 'e' to exit\nPress 'd' to delete an entry\n"
    while True:
        return_to_main_menue = input(text_options)
        if return_to_main_menue == "b":
            # clean and return to main menue
            cli_return_to_cli_menue()
            break

        if return_to_main_menue == "d":
            "In which category?"
            category = choose_category()
            print(category)
            year = YEAR
            kw = CALENDER_WEEK
            sql_data = reportrick_database_class.Database(DATABASEPATH)
            # output all enties
            format_list_print(sql_data.get_entries_text_by_category_week_year(
                kw, year, category))
            entry_text = input("Input the message that you want to delete  ")
            print(
                f"Year: {YEAR}, KW:{kw} CATEGORY:{category} entry_txt:{entry_text}")
            sql_data2 = reportrick_database_class.Database(DATABASEPATH)
            sql_data2.delete_entry_by_text_category_year_kw(
                category, year, kw, entry_text)
            log.debug(f"Entry {entry_text} was deleted")
            clean_console()
            cli_week_report()
        if return_to_main_menue == "e":
            # clean and end programm
            clean_console()
            quit()


def clean_console():
    """OS cleans the console window"""
    log.debug("clean_console() was executed")
    os.system('cls' if os.name == 'nt' else 'clear')


def cli_return_to_cli_menue():
    """Return you to the main menue"""
    log.debug("cli_return_to_cli_menue() was executed")
    clean_console()
    cli_menue()


def show_entries_by_category(category):
    """Display all elements by category"""


def choose_category():
    print("Choose a category")
    category_counter = 1
    for x in CATEGORY_LIST:
        print(f"{category_counter}:{CATEGORY_LIST[category_counter-1]} ")
        category_counter += 1

    category_selector = input(
        f"Choose an option between 1 to {category_counter-1} ")
    return CATEGORY_LIST[int(category_selector)-1]


def cli_add_entry():
    """Add new entry to the current Calender Week to the database"""

    clean_console()
    print("Add new entry to the work report")
    entry_text = input("Entry: ")
    category = choose_category()
    print(f"Entry: {entry_text}   Category: {category}")
    # get time and kw
    date_obj, date_formatted, calender_week = get_time_strings()
    log.debug(
        f"Date2: {date_formatted} CalenderWeekNumber: {calender_week}")
    # database handling
    sql_database = reportrick_database_class.Database(DATABASEPATH)
    sql_database.set_entry_table(
        category, entry_text, calender_week, date_formatted)

    cli_menue_return()


def cli_delete_entry_current_week():
    """List all entries of this week  and gives the option to delete them"""


def main(cliargs=None) -> int:
    """Entry point for the application script
    :param cliargs: Arguments to parse or None (=use :class:`sys.argv`)
    :return: error code
    """
    # clean_console()
    try:
        args = parsecli(cliargs)
        # do some useful things here...
        # If everything was good, return without error:
        args.func(args)
        return 0

    except MissingSubCommand as error:
        log.fatal(error)
        return 888


if __name__ == "__main__":
    sys.exit(main())