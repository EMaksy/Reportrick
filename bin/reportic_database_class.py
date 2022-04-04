import sqlite3
import string
import reportic
import os


class Database():

    def __init__(self, path: str, sql_data=None):

        self.path = path
        # Initialized in other functions for database connection
        self.connection = None
        # data which is send by user
        self.sql_data = {} if sql_data is None else sql_data
        # Create sql database in a given path
        self.create_databse_path()
        # table entry, trainee and team has been created

    def create_databse_path(self):
        """
        Create a database by a given path
        """
        reportic.log.debug(f"{self.path}")
        try:
            self.connection = sqlite3.connect(f"{self.path}")
            print("Connection to database true")
        except:
            print("Connection to database false")
            quit()

        if self.__create_empty_database() == True:
            return True
        else:
            print("Database connection didnt work")
            return False

    def __create_empty_database(self) -> bool:
        """
        Create tables to given database
        Tables: team, trainee and entry
        :param database:  path
        """
        create_user_table = """
        CREATE TABLE IF NOT EXISTS user(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT ,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        team_name TEXT NOT NULL
        );
        """
        create_entry_table = """
        CREATE TABLE IF NOT EXISTS entry (
        entry_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_text TEXT NOT NULL,
        date TEXT NOT NULL,
        calender_week INTEGER NOT NULL,
        category TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES user(user_id)
        );
        """
        # create table
        try:
            self.__sql_cmd(create_user_table)
            self.__sql_cmd(create_entry_table)
            return True
        except:
            print("Error, Database  was not created")
            return False

    def get_entries_text_by_category_week_year(self, calender_week, year, category):
        """Give a category and it will give you all the entries"""
        sql_search = f"""
        SELECT entry_text FROM entry WHERE STRFTIME('%Y', date)  = "{year}" AND category="{category}" AND calender_week="{calender_week}" ;
        """
        results = list(self.__sql_cmd(sql_search))
        print(len(results))
        self.__close()
        return results

    def set_user_table(self, first_name, last_name, team_name) -> bool:
        # setter sql statements
        reportic.log.debug(self, first_name, last_name, team_name)
        sql_set_data = f"""
        REPLACE INTO
        user (user_id, first_name, last_name, team_name)
        VALUES ("1","{first_name}", "{last_name}" , "{team_name}")
        """
        # sql executes
        try:
            self.__sql_cmd(sql_set_data)
            # self._execute_sql(sql_set_update_data)
            print("set_user_table sql worked")
            self.__close()
            return True
        except:
            print(self.__sql_cmd(sql_set_data))
            print("set_user_table sql error")
            self.__close()
            return False

    def get_user_table(self):
        sql_get_user_data = """
        SELECT  first_name, last_name, team_name FROM user WHERE user_id='1';
        """
        values = self.__sql_cmd(sql_get_user_data)
        reportic.log.debug(f"SQL DATA: {values}")
        values = list(values)
        try:
            first_name, last_name, team_name = values[0][0], values[0][1], values[0][2]
        except:
            first_name, last_name, team_name = "None", "None", "None"

        return first_name, last_name, team_name

    def set_entry_table(self, category, entry_text, kw, date):
        """Add a new entry to database"""
        sql_add_entry = f"""
        INSERT INTO
        entry(entry_text,category,calender_week,date,user_id)        
        VALUES ("{entry_text}","{category}","{kw}","{date}","1")
        """
        self.__sql_cmd(sql_add_entry)
        self.__close()

    def __format_list(self, entry_list):
        """A given list of date is formated"""
        counter = 1
        for x in entry_list:
            print(f"{counter}:{x}")
            counter += 1

    def get_entries_green_week_year(self, calender_week, year):
        """Give all entries for CATEGORY GREEN from a given calender_week and year"""
        sql_search = f"""
        SELECT entry_text FROM entry WHERE STRFTIME('%Y', date)  = "{year}" AND category="GREEN" AND calender_week="{calender_week}";
        """
        sql_list_entry = list(self.__sql_cmd(sql_search))
        self.__format_list(list(self.__sql_cmd(sql_search)))
        results = list(self.__sql_cmd(sql_search))
        # self.__close()
        return results

    def get_entries_red_week_year(self, calender_week, year):
        """Give all entries for CATEGORY RED from a given calender_week and year"""
        sql_search = f"""
        SELECT entry_text FROM entry WHERE STRFTIME('%Y', date)  = "{year}" AND category="RED" AND calender_week="{calender_week}";
        """
        results = list(self.__sql_cmd(sql_search))
        return results

    def get_entries_amber_week_year(self, calender_week, year):
        """Give all entries for CATEGORY AMBER from a given calender_week and year"""
        sql_search = f"""
        SELECT entry_text FROM entry WHERE STRFTIME('%Y', date)  = "{year}" AND category="AMBER" AND calender_week="{calender_week}";
        """
        results = list(self.__sql_cmd(sql_search))
        # self.__close()
        return results

    def get_entries_meeting_week_year(self, calender_week, year):
        """Give all entries for CATEGORY MEETING from a given calender_week and year"""
        sql_search = f"""
        SELECT entry_text FROM entry WHERE STRFTIME('%Y', date)  = "{year}" AND category="MEETING" AND calender_week="{calender_week}" ;
        """
        results = list(self.__sql_cmd(sql_search))
        # self.__close()
        return results

    def get_entries_text_by_category_week_year(self, calender_week, year, category):
        """Give a category and it will give you all the entries"""
        sql_search = f"""
        SELECT entry_text FROM entry WHERE STRFTIME('%Y', date)  = "{year}" AND category="{category}" AND calender_week="{calender_week}" ;
        """
        results = list(self.__sql_cmd(sql_search))
        print(len(results))
        self.__close()
        return results

    def __sql_cmd(self, sql_cmd_string) -> sqlite3.Cursor:
        """
        Execute a query by a given "connection"/database and a sql query
        param:
        str query: A sql command you wish to execute
        """
        cursor = self.connection.cursor()
        sql_result_obj = cursor.execute(sql_cmd_string)
        self.connection.commit()
        return sql_result_obj

    def __close(self):
        """
        Close database manually
        """
        try:

            self.connection.close()
            print("Database closed")
        except:
            print("Database was not closed")


"""
    def _fill_table_sql_cmd(self):
        '''
        Execute a query with all the given information from script
        :param
        '''
        print(
            "Here we will write down all our data to database %s", self.sql_data)
        # trainee_data
        trainee_name = str(self.sql_data.get("name"))
        # print(trainee_name)
        trainee_current_day = self.sql_data.get("current_day")
        trainee_duration = float(self.sql_data.get("duration"))
        trainee_start_year = self.sql_data.get("start_year")
        trainee_end_duration = self.sql_data.get("end_duration_education")
        trainee_number_teams = int(self.sql_data.get("count_teams"))
        # team data
        team_name = self.sql_data.get("team")
        team_number = self.sql_data.get("team_number")
        # team duration
        team_start = self.sql_data.get("team_time_start")
        team_end = self.sql_data.get("team_time_end")
        team_id_fk = "1"

        # sql command
        sql_cmd_trainee = f'''
        INSERT INTO
        trainee (NAME_TRAINEE, START_YEAR, GRADUATION_YEAR, DATABASE_VERSION,
                 NUMBER_OF_TEAMS, DURATION, CREATION_DATE,TEAM_ID)
        VALUES
        ("{trainee_name}", "{trainee_start_year}" , "{trainee_end_duration}",	"{self.VERSION}",
         "{trainee_number_teams}","{trainee_duration}","{trainee_current_day}","{team_id_fk}");
        '''

        sql_cmd_team = f'''
        INSERT INTO
        team (TEAM_NAME,TEAM_NUMBER,TEAM_START,TEAM_END)
        VALUES
        ("{team_name}","{team_number}","{team_start}","{team_end}");
        '''

        # now its time to execute sql command with data and fill the database
        self.__sql_cmd(sql_cmd_team)
        self.__sql_cmd(sql_cmd_trainee)
"""
"""
    def _adapt_changes_to_database(self):
        """
"""

    # We need to collect all the changed data
    print(
        '''Replace old values in database with the new %s''', self.sql_data)
    trainee_name = str(self.sql_data.get("name"))
    # print(trainee_name)
    trainee_current_day = self.sql_data.get("current_day")
    trainee_duration = float(self.sql_data.get("duration"))
    trainee_start_year = self.sql_data.get("start_year")
    trainee_end_duration = self.sql_data.get("end_duration_education")
    trainee_number_teams = int(self.sql_data.get("count_teams"))
    # team data
    team_name = self.sql_data.get("team")
    team_number = self.sql_data.get("team_number")
    # team duration
    team_start = self.sql_data.get("team_time_start")
    team_end = self.sql_data.get("team_time_end")
    team_id_fk = "1"
    team_pk = "1"
    trainee_pk = "1"

    # sql command
    sql_cmd_trainee = f'''
    REPLACE INTO
    trainee (TRAINEE_ID,NAME_TRAINEE, START_YEAR, GRADUATION_YEAR, DATABASE_VERSION,
             NUMBER_OF_TEAMS, DURATION, CREATION_DATE,TEAM_ID)
    VALUES
    ("{trainee_pk}","{trainee_name}", "{trainee_start_year}" , "{trainee_end_duration}",	"{self.VERSION}",
     "{trainee_number_teams}","{trainee_duration}","{trainee_current_day}","{team_id_fk}");
    '''

    sql_cmd_team = f'''
    REPLACE INTO
    team (TEAM_ID,TEAM_NAME,TEAM_NUMBER,TEAM_START,TEAM_END)
    VALUES
    ("{team_pk}","{team_name}","{team_number}","{team_start}","{team_end}");
    '''

    # now its time to execute sql command with data and fill the database
    self.__sql_cmd(sql_cmd_team)
    self.__sql_cmd(sql_cmd_trainee)

    # overwrite sql database with the changes
"""
