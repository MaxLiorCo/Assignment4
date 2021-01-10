import sqlite3
import atexit

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

    def registerFile(filePath):
        file_reader = open(filePath, 'r')
        firstLine = file_reader.readline()
        # read first line to know the lengths of the insertions for each table
        tableInsertionsLength = [int(num) for num in firstLine.split(',')]
        #Lines = file_reader.readlines();
        for i in range(tableInsertionsLength[0]):
            line = file_reader.readline().split(',')
            vaccines.insert(int(line[0]),datetime.strptime)








# ------------------------------------------------------------------------------------------------------------

# Create repository singleton
repo = _Repository()
atexit.register(repo._close())
