import sqlite3
import os
import sys
from Repository import _Repository
from sqlite3 import Error

args = sys.argv
conn = None

conn = sqlite3.connect("./database.db")
repo = _Repository()
try:
    repo.create_tables()
except Error as e:
    print("table already exists")
repo.registerFile(sys.argv[1])
#repo.executeOrders(sys.argv[2])
# inside executeOrders we create output file

