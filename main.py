import sqlite3
import sys
from Repository import repo
from sqlite3 import Error


try:
    repo.create_tables()
    repo.register_file(sys.argv[1])
    repo.execute_orders(sys.argv[2])
except Error as e:
    pass
