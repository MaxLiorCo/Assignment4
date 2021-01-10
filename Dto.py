

class vaccines:
    def __init__(self, id, date, supplier, quantity):
        self.id = id
        self.date = date
        self.supplier = supplier
        self.quantity = quantity

class suppliers:
    def __init__(self, id, name, quantity):
        self.id = id
        self.name = name
        self.quantity = quantity

class clinics:
    def __init__(self, id, name, logistic):
        self.id = id
        self.name = name
        self.logistic = logistic

class logistics:
    def __init__(self, id, name , count_sent, count_received):
        self.id = id
        self.name = name
        self.count_sent = count_sent
        self.count_received = count_received

