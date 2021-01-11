from Dto import *


class _Vaccines:
    order_count = 0

    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""
               INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)
           """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])
        self.order_count += 1

    def find(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM vaccines WHERE id = ?
        """, [vaccine_id])
        return Vaccine(*c.fetchone())


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                INSERT INTO suppliers (id, name, logistic) VALUES (?, ?, ?)
        """, [supplier.id, supplier.name, supplier.logistic])

    def find(self, column_name, column_value): # column_name = id or name
        c = self._conn.cursor()
        c.execute("""
                SELECT * FROM suppliers WHERE ? = ?
            """, [column_name, column_value])
        return Supplier(*c.fetchone())


class _Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""
            INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
        """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT * FROM clinics
        """).fetchall()
        return [Clinic(*row) for row in all]


class _Logistics:

    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""
               INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
           """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def find(self, logistic_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM logistics WHERE id = ?
        """, [logistic_id])
        return Logistic(*c.fetchone())
