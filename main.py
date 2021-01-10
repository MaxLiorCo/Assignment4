import sqlite3
import os
import sys
from Repository import _Repository
from sqlite3 import Error

args = sys.argv
conn = None

conn = sqlite3.connect("./database.db")
repo = _Repository()
repo.create_tables()
repo.registerFile(sys.argv[0])
repo.executeOrders(sys.argv[1])
# inside executeOrders we create output file

