import sqlite3
import os
import sys
from Repository import _Repository
from sqlite3 import Error

args = sys.argv
conn = None

try:
    conn = sqlite3.connect("./database.db")
    repo = _Repository()
    repo.create_tables()
    print()
except Error as e:
    print(e)
finally:
    if conn:
        conn.commit()
        conn.close()
