import os

dirname = os.path.dirname(__file__)
filepath = os.path.join(dirname, '/test.sql')
# test
print(f"{dirname}/database/reportic_database.sqlite")
print()
print(filepath)

absolute_path = os.path.dirname(__file__)
absolute_file_dir = "/database/reportic_database.sqlite"
DATABASEPATH = absolute_path+absolute_file_dir
print(DATABASEPATH)
os.mkdir(filepath)

# Python relative path
# Source https://appdividend.com/2021/06/07/python-relative-path/
