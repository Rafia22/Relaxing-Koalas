import sqlite3

class Customer:
    def __init__(self, name, contact):
        self.name = self.validate_name(name)
        self.contact = self.validate_contact(contact)

    def save_to_db(self):
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO customers (name, contact) VALUES (?, ?)', (self.name, self.contact))
            self.id = cursor.lastrowid
            conn.commit()

    @staticmethod
    def validate_name(name):
        if not name:
            raise ValueError("Customer name cannot be empty.")
        return name

    @staticmethod
    def validate_contact(contact):
        if not contact.startswith('04'):
            raise ValueError("Contact must be a 10-digit phone number starting with '04'.")
        if len(contact) != 10:
            raise ValueError("Contact must be a 10-digit phone number.")
        if not contact.isdigit():
            raise ValueError("Contact must contain only digits.")
        return contact













# import sqlite3

# class Customer:
#     def __init__(self, name, contact):
#         self.name = self.validate_name(name)
#         self.contact = self.validate_contact(contact)
#         self.reservations = []
#         self.orders = []

#     def save_to_db(self):
#         conn = sqlite3.connect('restaurant.db')
#         cursor = conn.cursor()
#         cursor.execute('INSERT INTO customers (name, contact) VALUES (?, ?)', (self.name, self.contact))
#         conn.commit()
#         self.id = cursor.lastrowid
#         conn.close()

#     def validate_name(self, name):
#         if not name:
#             raise ValueError("Customer name cannot be empty.")
#         return name

#     def validate_contact(self, contact):
#         if not contact:
#             raise ValueError("Contact cannot be empty.")
#         return contact

#     def make_reservation(self, reservation):
#         self.reservations.append(reservation)

#     def place_order(self, order):
#         self.orders.append(order)

#     def __str__(self):
#         return f"Customer: {self.name}, Contact: {self.contact}"
