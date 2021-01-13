import os
import sqlite3
import atexit
from Dto import *

# For Join query
from datetime import datetime

from Dao import _Vaccines
from Dao import _Suppliers
from Dao import _Clinics
from Dao import _Logistics


# The Repository
class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('./database.db')
        self.vaccines = _Vaccines(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.clinics = _Clinics(self._conn)
        self.logistics = _Logistics(self._conn)
        if os.path.exists("output.txt"):
            os.remove("output.txt")

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE vaccines (
            id          INT         PRIMARY KEY,
            date        DATE        NOT NULL,
            supplier    INT,
            quantity    INT         NOT NULL,
            
            FOREIGN KEY(supplier)   REFERENCES suppliers(id)
        );

        CREATE TABLE suppliers (
            id             INT       PRIMARY KEY,
            name           STRING    NOT NULL,
            logistic       INT,
            
            FOREIGN KEY(logistic)    REFERENCES logistics(id)
        );

        CREATE TABLE clinics (
            id          INT         PRIMARY KEY,
            location    STRING      NOT NULL,
            demand      INT         NOT NULL,
            logistic    INT,

            FOREIGN KEY(logistic)     REFERENCES logistics(id)
        );
        
        CREATE TABLE logistics (
        id              INT         PRIMARY KEY,
        name            STRING      NOT NULL,
        count_sent      INT         NOT NULL,
        count_received  INT         NOT NULL
        );
    """)

    # register file entries to database
    def register_file(self, filePath):
        with open(filePath, 'r') as file_reader:
            firstLine = file_reader.readline()
            # read first line to know the lengths of the insertions for each table
            tableInsertionsLength = [int(num) for num in firstLine.split(',')]
            # NOTICE: last cell in each line is "_\n" but python ignores \n when converting to int, would produce bugs otherwise

            # vaccines
            for i in range(tableInsertionsLength[0]):
                line = file_reader.readline().split(',')
                self.vaccines.insert(
                    Vaccine(int(line[0]), datetime.strptime(line[1], "%Y-%m-%d").date(), int(line[2]), int(line[3])))
                if( i == tableInsertionsLength[0] - 1 ):
                    self.vaccines.order_count = int(line[0]) + 1  # for the case we received a list of id's not beginning from 1
            # suppliers
            for i in range(tableInsertionsLength[1]):
                line = file_reader.readline().split(',')
                self.suppliers.insert(Supplier(int(line[0]), line[1], int(line[2])))
            # clinics
            for i in range(tableInsertionsLength[2]):
                line = file_reader.readline().split(',')
                self.clinics.insert(Clinic(int(line[0]), line[1], int(line[2]), int(line[3])))
            # logistics
            for i in range(tableInsertionsLength[3]):
                line = file_reader.readline().split(',')
                self.logistics.insert(Logistic(int(line[0]), line[1], int(line[2]), int(line[3])))

    # Executing orders from file
    def execute_orders(self, file_path):
        with open(file_path, 'r') as file_reader:
            for line in file_reader:
                result = [x.strip() for x in line.split(',')]  # splits the string where the comma is
                if len(result) == 3:
                    self.receive_shipment(result[0], int(result[1]), result[2])
                else:
                    self.send_shipment(result[0], int(result[1]))

                self.add_summary_line()

    def receive_shipment(self, name, amount, date):
        id = self.vaccines.order_count
        date_to_insert = datetime.strptime(date, "%Y-%m-%d").date()
        supplier = self.suppliers.find_by_name(name)
        vaccine = Vaccine(id, date_to_insert, supplier.id, amount)
        self.vaccines.insert(vaccine)

        self.logistics.update_received(supplier.logistic, amount)

    def send_shipment(self, location, amount):
        self.vaccines.take_from_inventory(amount)  # take the amount needed from the inventory

        self.clinics.update_demand(location, amount)  # update the demand in the clinic which is in the location

        logistic_id_to_update = self.clinics.get_logistics_by_location(location)
        self.logistics.update_sent(logistic_id_to_update, amount)  # update the logistics that sent the vaccines

    def add_summary_line(self):
        with open('./output.txt', 'a') as the_file:
            the_file.write(str(self.vaccines.total_inventory) + "," +
                           str(self.clinics.total_demand) + "," +
                           str(self.logistics.total_received) + "," +
                           str(self.logistics.total_sent) + "\n")


repo = _Repository()
atexit.register(repo._close)