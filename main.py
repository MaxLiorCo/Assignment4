import atexit
import sqlite3
import sys
from Repository import _Repository
from sqlite3 import Error

conn = sqlite3.connect("./database.db")
repo = _Repository()
try:
    repo.create_tables()
except Error as e:
    pass
repo.register_file(sys.argv[1])
repo.execute_orders(sys.argv[2])

# inside executeOrders we the create output file


def close():
    conn.commit()
    conn.close()


# register to close when program finishes
atexit.register(close())
