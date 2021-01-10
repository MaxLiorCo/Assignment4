class _Students:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, student):
        self._conn.execute("""
               INSERT INTO students (id, name) VALUES (?, ?)
           """, [student.id, student.name])

    def find(self, student_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name FROM students WHERE id = ?
        """, [student_id])
        return Student(*c.fetchone())

class _Assignments:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, assignment):
        self._conn.execute("""
                INSERT INTO assignments (num, expected_output) VALUES (?, ?)
        """, [assignment.num, assignment.expected_output])

    def find(self, num):
        c = self._conn.cursor()
        c.execute("""
                SELECT num,expected_output FROM assignments WHERE num = ?
            """, [num])

        return Assignment(*c.fetchone())

class _Grades:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, grade):
        self._conn.execute("""
            INSERT INTO grades (student_id, assignment_num, grade) VALUES (?, ?, ?)
        """, [grade.student_id, grade.assignment_num, grade.grade])

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT student_id, assignment_num, grade FROM grades
        """).fetchall()

        return [Grade(*row) for row in all]

