class Customer:
    def __init__(self, name, contact):
        self.name = self.validate_name(name)
        self.contact = self.validate_contact(contact)
        self.reservations = []
        self.orders = []

    def validate_name(self, name):
        if not name:
            raise ValueError("Customer name cannot be empty.")
        return name

    def validate_contact(self, contact):
        if not contact:
            raise ValueError("Contact cannot be empty.")
        return contact

    def make_reservation(self, reservation):
        self.reservations.append(reservation)

    def place_order(self, order):
        self.orders.append(order)

    def __str__(self):
        return f"Customer: {self.name}, Contact: {self.contact}"
