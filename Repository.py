import sqlite3

# For Join query
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

    #take care of it
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
        CREATE TABLE students (
            id      INT         PRIMARY KEY,
            name    TEXT        NOT NULL
        );

        CREATE TABLE assignments (
            num                 INT     PRIMARY KEY,
            expected_output     TEXT    NOT NULL
        );

        CREATE TABLE grades (
            student_id      INT     NOT NULL,
            assignment_num  INT     NOT NULL,
            grade           INT     NOT NULL,

            FOREIGN KEY(student_id)     REFERENCES students(id),
            FOREIGN KEY(assignment_num) REFERENCES assignments(num),

            PRIMARY KEY (student_id, assignment_num)
        );
    """)
