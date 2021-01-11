from Dto import *


# must be singletons

class _Vaccines:
    order_count = 0
    total_inventory = 0

    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self.total_inventory += vaccine.quantity
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

    # removes or updates existing entries
    def take_from_inventory(self, amount):
        c = self._conn.cursor()
        list_of_records = c.execute("""
                    SELECT id, quantity FROM vaccines ORDER BY DATE
                """).fetchall()
        for shipment in list_of_records:
            id = shipment[0]
            quantity = shipment[1]
            if amount >= quantity:  # remove
                amount -= quantity
                self.total_inventory -= amount
                c.execute("""
                    DELETE FROM vaccines WHERE id = ?
                """, [id])
            else:
                quantity -= amount  # we still have more remaining from that shipment
                self.total_inventory -= amount
                amount = 0
                self._conn.execute("""
                                UPDATE vaccines SET quantity = ? WHERE id = ?
                                """, [quantity, id])
                if amount == 0:
                    break


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
        self.total_demand += clinic.demand

    # probably change
    def get_logistics_by_location(self, location):
        c = self._conn.cursor()
        c.execute("""
                SELECT logistic FROM clinics WHERE location = ?
            """, [location])
        return c.fetchone()[0]

    def update_demand(self, location,  amount):
        c = self._conn.cursor()
        c.execute("""
            SELECT demand FROM clinics WHERE location = ? """, [location])
        curr_demand = c.fetchone()
        c.execute("""
            UPDATE clinics SET demand = ? where location = ?""", [curr_demand[0] - amount, location])
        self.total_demand -= amount


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

    def update_received(self, logistic_id, amount_to_add):
        c = self._conn.cursor()
        c.execute("""
            SELECT count_received FROM logistics WHERE id = ?""", [logistic_id])
        current_amount = c.fetchone()[0]
        self._conn.execute("""
                UPDATE logistics SET count_received = ? WHERE id = ?""", [amount_to_add + current_amount, logistic_id])
        self.total_received += amount_to_add

    def update_sent(self, logistic_id, amount_to_add):
        c = self._conn.cursor()
        c.execute("""
                    SELECT count_sent FROM logistics WHERE id = ?""", [logistic_id])
        current_amount = c.fetchone()[0]
        self._conn.execute("""
            UPDATE logistics SET count_received = ? WHERE id = ?""", [amount_to_add + current_amount, logistic_id])
        self.total_sent += amount_to_add
