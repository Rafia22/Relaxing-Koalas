import sqlite3

class Customer:
    def __init__(self, name, contact):
        self.name = self.validate_name(name)
        self.contact = self.validate_contact(contact)
        self.reservations = []
        self.orders = []

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
    
    @staticmethod
    def load_customers_from_db():
        customers = []
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, contact FROM customers')
            for row in cursor.fetchall():
                customer = Customer(row[1], row[2])
                customer.id = row[0]
                customers.append(customer)
        return customers

    def make_reservation(self, reservation):
        self.reservations.append(reservation)

    def place_order(self, order):
        self.orders.append(order)
