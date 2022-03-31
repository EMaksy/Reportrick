import sqlite3
import reportic


class Database():

    VERSION = 10

    def __init__(self, path: str, sql_data=None):

        self.path = path
        # Initialized in other functions for database connection
        self.connection = None
        # data which is send by user

        self.sql_data = {} if sql_data is None else sql_data
        # Create sql database in a given path
        self.create()
        # table entry, trainee and team has been created

    def create(self):
        """
        Create a database by a given path
        """
        reportic.log.debug(f"{self.path}")
        self.connection = sqlite3.connect(f"{self.path}")
        print("Connection to database true")

        self._create_empty_database()

    def _create_empty_database(self):
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
        create_calnder_week_table = """
        CREATE TABLE IF NOT EXISTS calender_week (
        calender_week_id INTEGER PRIMARY KEY AUTOINCREMENT,
        calender_week_number INTEGER NOT NULL,
        calender_week_date  TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES user(user_id)
        );
        """
        create_entry_table = """
        CREATE TABLE IF NOT EXISTS entry (
        entry_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_text TEXT NOT NULL,
        category TEXT NOT NULL,
        calender_week_id INTEGER,
        FOREIGN KEY(calender_week_id) REFERENCES calender_week(callender_week_id)
        );
        """

        # create table
        self._execute_sql(create_user_table)
        self._execute_sql(create_calnder_week_table)
        self._execute_sql(create_entry_table)

    def _execute_sql(self, sql_command):
        """
        Execute a query by a given "connection"/database and a sql query
        param:
        str connection: Path to the database
        str query: A sql command you wish to execute
        """
        cursor = self.connection.cursor()
        result = cursor.execute(sql_command)
        self.connection.commit()
        return result

    def _fill_table_sql_cmd(self):
        """
        Execute a query with all the given information from script
        :param
        """
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
        sql_cmd_trainee = f"""
        INSERT INTO
        trainee (NAME_TRAINEE, START_YEAR, GRADUATION_YEAR, DATABASE_VERSION,
                 NUMBER_OF_TEAMS, DURATION, CREATION_DATE,TEAM_ID)
        VALUES
        ("{trainee_name}", "{trainee_start_year}" , "{trainee_end_duration}",	"{self.VERSION}",
         "{trainee_number_teams}","{trainee_duration}","{trainee_current_day}","{team_id_fk}");
        """

        sql_cmd_team = f"""
        INSERT INTO
        team (TEAM_NAME,TEAM_NUMBER,TEAM_START,TEAM_END)
        VALUES
        ("{team_name}","{team_number}","{team_start}","{team_end}");
        """

        # now its time to execute sql command with data and fill the database
        self._execute_sql(sql_cmd_team)
        self._execute_sql(sql_cmd_trainee)

    def _adapt_changes_to_database(self):
        """
        """

        # We need to collect all the changed data
        print(
            """Replace old values in database with the new %s""", self.sql_data)
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
        sql_cmd_trainee = f"""
        REPLACE INTO
        trainee (TRAINEE_ID,NAME_TRAINEE, START_YEAR, GRADUATION_YEAR, DATABASE_VERSION,
                 NUMBER_OF_TEAMS, DURATION, CREATION_DATE,TEAM_ID)
        VALUES
        ("{trainee_pk}","{trainee_name}", "{trainee_start_year}" , "{trainee_end_duration}",	"{self.VERSION}",
         "{trainee_number_teams}","{trainee_duration}","{trainee_current_day}","{team_id_fk}");
        """

        sql_cmd_team = f"""
        REPLACE INTO
        team (TEAM_ID,TEAM_NAME,TEAM_NUMBER,TEAM_START,TEAM_END)
        VALUES
        ("{team_pk}","{team_name}","{team_number}","{team_start}","{team_end}");
        """

        # now its time to execute sql command with data and fill the database
        self._execute_sql(sql_cmd_team)
        self._execute_sql(sql_cmd_trainee)

        # overwrite sql database with the changes

    def set_user_table(self, first_name, last_name, team_name) -> bool:
        # setter sql statements
        reportic.log.debug(self, first_name, last_name, team_name)
        sql_set_data = f"""
        REPLACE INTO
        user (user_id, first_name, last_name, team_name)
        VALUES ("1","{first_name}", "{last_name}" , "{team_name}")
        """
        sql_set_update_data = f"""
        UPDATE user SET first_name = {first_name} last_name = {last_name} team_name = {team_name}
        WHERE user_id=1
        """
        sql_return_message = ""
        # sql executes
        try:
            self._execute_sql(sql_set_data)
            # self._execute_sql(sql_set_update_data)
            print("set_user_table sql worked")
            self.close()
            return True
        except:
            print(self._execute_sql(sql_set_data))
            print("set_user_table sql error")
            print(sql_return_message)
            self.close()
            return False

    def get_user_table(self):
        sql_get_user_data = """
        SELECT  first_name, last_name, team_name FROM user WHERE user_id='1';
        """
        values = self._execute_sql(sql_get_user_data)
        reportic.log.debug(f"SQL DATA: {values}")
        values = list(values)
        try:
            first_name, last_name, team_name = values[0][0], values[0][1], values[0][2]
        except:
            first_name, last_name, team_name = "None", "None", "None"

        return first_name, last_name, team_name

    def close(self):
        """
        Close database manually
        """
        print("Database closed")
        self.connection.close()

    """ def open(self, databasepath):
        if True == self.sqlite3.connect(databasepath):
            return print("Database open")
        else:
            return print("Database is still closed")
    """
