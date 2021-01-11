import sqlite3
import atexit
from Dto import *

# For Join query
from datetime import datetime

from Dao import _Vaccines
from Dao import _Suppliers
from Dao import _Clinics
from Dao import _Logistics


# TODO: remove this shit
class StudentGradeWithName:
    def __init__(self, name, assignment_num, grade):
        self.name = name
        self.assignment_num = assignment_num
        self.grade = grade


# The Repository
class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('./database.db')
        self.vaccines = _Vaccines(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.clinics = _Clinics(self._conn)
        self.logistics = _Logistics(self._conn)

    # take care of it
    def _close(self):
        self._conn.commit()
        self._conn.close()

    # TODO remove this shit
    def get_grades_with_names(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT students.name, grades.assignment_num, grades.grade 
            FROM grades
            JOIN students ON grades.student_id = students.id
        """).fetchall()

        return [StudentGradeWithName(*row) for row in all]

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

    def registerFile(self, filePath):
        with open(filePath, 'r') as file_reader:
            firstLine = file_reader.readline()
            # read first line to know the lengths of the insertions for each table
            tableInsertionsLength = [int(num) for num in firstLine.split(',')]
            # NOTICE: last cell in each line is "*\n" but python ignores \n when converting to int
            for i in range(tableInsertionsLength[0]):
                line = file_reader.readline().split(',')
                self.vaccines.insert(
                    Vaccine(int(line[0]), datetime.strptime(line[1], "%Y-%m-%d").date(), int(line[2]), int(line[3])))
            for i in range(tableInsertionsLength[1]):
                line = file_reader.readline().split(',')
                self.suppliers.insert(Supplier(int(line[0]), line[1], int(line[2])))
            for i in range(tableInsertionsLength[2]):
                line = file_reader.readline().split(',')
                self.clinics.insert(Clinic(int(line[0]), line[1], int(line[2]), int(line[3])))
            for i in range(tableInsertionsLength[3]):
                line = file_reader.readline().split(',')
                self.logistics.insert(Logistic(int(line[0]), line[1], int(line[2]), int(line[3])))

            curser = self._conn.cursor()
            print(curser.execute(""" 
                SELECT * FROM vaccines
            """).fetchall())
            print(curser.execute(""" 
                SELECT * FROM suppliers
            """).fetchall())
            print(curser.execute(""" 
                SELECT * FROM clinics
            """).fetchall())
            print(curser.execute(""" 
                SELECT * FROM logistics
            """).fetchall())

    # ------------------------------------------------------------------------------------------------------------
    # Executing orders
    def executeOrders(self, filePath):
        with open(filePath, 'r') as file_reader:
            for line in file_reader:
                result = [line.strip() for x in line.split(',')] # splits the string where the comma is
                if len(result) == 3:
                    receive_shipment(result[0], result[1], result[2])
                #else:
                    send_shipment(result[0], result[1])

def receive_shipment(self, name, amount, date):
    id = _Vaccines.order_count
    date_to_insert = datetime.strptime(date, "%Y-%m-%d").date()



# Create repository singleton
repo = _Repository()
atexit.register(repo._close())
