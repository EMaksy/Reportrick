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
