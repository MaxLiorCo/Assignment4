from Dto import *


# must be singletons

class _Vaccines:
    order_count = 0
    total_inventory = 0

    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""
               INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)
           """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])
        self.order_count += 1

    def find(self, id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM vaccines WHERE id = ?
        """, [id])
        return Vaccine(*c.fetchone())


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                INSERT INTO suppliers (id, name, logistic) VALUES (?, ?, ?)
        """, [supplier.id, supplier.name, supplier.logistic])

    def find_by_id(self, id):
        c = self._conn.cursor()
        c.execute("""
                SELECT * FROM suppliers WHERE id = ?
            """, [id])
        return Supplier(*c.fetchone())

    def find_by_name(self, name):
        c = self._conn.cursor()
        c.execute("""
                SELECT * FROM suppliers WHERE name = ?
            """, [name])
        return Supplier(*c.fetchone())


class _Clinics:
    total_demand = 0

    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""
            INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
        """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    # probably change
    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT * FROM clinics
        """).fetchall()
        return [Clinic(*row) for row in all]


class _Logistics:
    total_sent = 0
    total_received = 0

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

    def update_received(self, supplier_id, new_amount):
        self._conn.execute("""
                UPDATE logistics SET received_amount = ? WHERE id = ?""", [new_amount, supplier_id])
