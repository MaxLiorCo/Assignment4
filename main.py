import sqlite3
import sys
from Repository import repo
from sqlite3 import Error

conn = sqlite3.connect("./database.db")

try:
    repo.create_tables()
except Error as e:
    pass
repo.register_file(sys.argv[1])
repo.execute_orders(sys.argv[2])