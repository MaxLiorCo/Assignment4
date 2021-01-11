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
    def get_logistics_by_location(self, location):
        c = self._conn.cursor()
        c.execute("""
                SELECT logistic FROM clinics WHERE location = ?
            """, [location])
        return c.fetchone()

    def update_demand(self, location,  amount):
        c = self._conn.cursor()
        c.execute("""
            SELECT demand FROM clinics WHERE location = ? """, [location])
        curr_demand = c.fetchone()
        c.execute("""
            UPDATE clinics SET demand = ? where location = ?""", [amount + curr_demand, location])



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

    def update_received(self, supplier_id, amount_to_add):
        c = self._conn.cursor()
        c.execute("""
            SELECT count_received FROM logistics WHERE id = ?""", [supplier_id])
        current_amount = c.fetchone()
        self._conn.execute("""
                UPDATE logistics SET count_received = ? WHERE id = ?""", [amount_to_add + current_amount, supplier_id])

    def update_sent(self, supplier_id, amount_to_add):
        c = self._conn.cursor()
        c.execute("""
                    SELECT count_sent FROM logistics WHERE id = ?""", [supplier_id])
        current_amount = c.fetchone()
        self._conn.execute("""
            UPDATE logistics SET count_received = ? WHERE id = ?""", [amount_to_add + current_amount, supplier_id])