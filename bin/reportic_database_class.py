import sqlite3
import string
import reportic


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

    def create_databse_path(self) -> bool:
        """
        Create a database by a given path
        """
        reportic.log.debug(f"{self.path}")
        try:
            self.connection = sqlite3.connect(f"{self.path}")
            reportic.log.debug("Connection to database true")
        except:
            reportic.log.debug("Connection to database false")
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
        calendar_week INTEGER NOT NULL,
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

    def get_entries_text_by_category_week_year(self, calendar_week, year, category) -> list:
        """Give a category and it will give you all the entries"""
        sql_search = f"""
        SELECT entry_text FROM entry WHERE STRFTIME('%Y', date)  = "{year}" AND category="{category}" AND calendar_week="{calendar_week}" ;
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
        VALUES ("1","{first_name}", "{last_name}", "{team_name}")
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

    def get_user_table(self) -> string:
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
        entry(entry_text,category,calendar_week,date,user_id)        
        VALUES ("{entry_text}","{category}","{kw}","{date}","1")
        """
        self.__sql_cmd(sql_add_entry)
        self.__close()

    def get_entries_green_week_year(self, calendar_week, year) -> list:
        """Give all entries for CATEGORY GREEN from a given calendar_week and year"""
        sql_search = f"""
        SELECT entry_text FROM entry WHERE STRFTIME('%Y', date)  = "{year}" AND category="GREEN" AND calendar_week="{calendar_week}";
        """

        results = list(self.__sql_cmd(sql_search))
        # self.__close()
        return results

    def get_entries_red_week_year(self, calendar_week, year) -> list:
        """Give all entries for CATEGORY RED from a given calendar_week and year"""
        sql_search = f"""
        SELECT entry_text FROM entry WHERE STRFTIME('%Y', date)  = "{year}" AND category="RED" AND calendar_week="{calendar_week}";
        """
        results = list(self.__sql_cmd(sql_search))
        return results

    def get_entries_amber_week_year(self, calendar_week, year) -> list:
        """Give all entries for CATEGORY AMBER from a given calendar_week and year"""
        sql_search = f"""
        SELECT entry_text FROM entry WHERE STRFTIME('%Y', date)  = "{year}" AND category="AMBER" AND calendar_week="{calendar_week}";
        """
        results = list(self.__sql_cmd(sql_search))
        # self.__close()
        return results

    def get_entries_meeting_week_year(self, calendar_week, year) -> list:
        """Give all entries for CATEGORY MEETING from a given calendar_week and year"""
        sql_search = f"""
        SELECT entry_text FROM entry WHERE STRFTIME('%Y', date)  = "{year}" AND category="MEETING" AND calendar_week="{calendar_week}" ;
        """
        results = list(self.__sql_cmd(sql_search))
        # self.__close()
        return results

    def get_entries_text_by_category_week_year(self, calendar_week, year, category) -> list:
        """Give a category and it will give you all the entries"""
        sql_search = f"""
        SELECT entry_text FROM entry WHERE STRFTIME('%Y', date)  = "{year}" AND category="{category}" AND calendar_week="{calendar_week}" ;
        """
        results = list(self.__sql_cmd(sql_search))
        print(len(results))
        self.__close()
        return results

    def delete_entry_by_text_category_year_kw(self, category, year, calendar_week, entry_text):
        """Delete an entrie from database"""
        print("entry was deleted")
        sql_cmd_delete = (f"""
                       DELETE FROM entry
                       WHERE STRFTIME('%Y', date)  = "{year}" AND category="{category}" AND calendar_week="{calendar_week}" AND entry_text="{entry_text}" ;
                       """)
        self.__sql_cmd(sql_cmd_delete)

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
