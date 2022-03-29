import sqlite3


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
        self.connection = sqlite3.connect(f"{self.path}")
        print("Connection to database true")
        self._create_empty_database()

    def _create_empty_database(self):
        """
        Create tables to given database
        Tables: team, trainee and entry
        :param database:  path
        """
        create_users_table = """
        CREATE TABLE IF NOT EXISTS team (
        TEAM_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TEAM_NUMBER INTEGER NOT NULL,
        TEAM_NAME TEXT NOT NULL,
        TEAM_START TEXT NOT NULL,
        TEAM_END TEXT NOT NULL
        );
        """
        create_year_table = """
        CREATE TABLE IF NOT EXISTS trainee (
        TRAINEE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME_TRAINEE TEXT,
        START_YEAR TEXT,
        GRADUATION_YEAR INTEGER,
        DATABASE_VERSION TEXT,
        NUMBER_OF_TEAMS TEXT INTEGER,
        DURATION  INTEGER,
        CREATION_DATE TEXT,
        TEAM_ID  INTEGER,
        FOREIGN KEY(TEAM_ID) REFERENCES team(TEAM_ID)
        );
        """
        create_calender_week_table = """
        CREATE TABLE IF NOT EXISTS entry (
        ENTRY_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
        ENTRY_TXT TEXT NOT NULL,
        ENTRY_DATE TEXT NOT NULL,
        DAY_ID INTEGER,
        FOREIGN KEY(DAY_ID) REFERENCES team(DAY_ID)
        );
        """
        create_entry_table = """
        CREATE TABLE IF NOT EXISTS day (
        DAY_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
        DAY_DATE TEXT NOT NULL,
        DAY_FREE INTEGER,
        TRAINEE_ID INTEGER NOT NULL,
        FOREIGN KEY(TRAINEE_ID) REFERENCES trainee(TRAINEE_ID)
        );
        """
        # execute querys
        self._execute_sql(create_users_table)
        self._execute_sql(create_year_table)
        self._execute_sql(create_calender_week_table)
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

    def close(self):
        """
        Close database manually
        """
        print("Database closed")
        self.connection.close()
