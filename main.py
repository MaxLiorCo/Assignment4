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
    print()
repo.register_file(sys.argv[1])
repo.execute_orders(sys.argv[2])


# inside executeOrders we create output file

# take care of it
def close(self):
    self._conn.commit()
    self._conn.close()


# register to close when program finishes
atexit.register(close())
