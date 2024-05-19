class Customer:
    def __init__(self, name, contact):
        self.name = name
        self.contact = contact
        self.reservations = []
        self.orders = []

    def make_reservation(self, reservation):
        self.reservations.append(reservation)

    def place_order(self, order):
        self.orders.append(order)

    def __str__(self):
        return f"Customer: {self.name}, Contact: {self.contact}"
