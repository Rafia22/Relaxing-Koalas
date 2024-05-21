from datetime import datetime, timedelta

class Reservation:
    def __init__(self, id, customer_name, contact, date, time, guests, table_id):
        self.id = id
        self.customer_name = self.validate_name(customer_name)
        self.contact = self.validate_contact(contact)
        self.date = self.validate_date(date)
        self.time = self.validate_time(time)
        self.guests = self.validate_guests(guests)
        self.table_id = table_id

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
    def validate_date(date):
        try:
            reservation_date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

        if reservation_date < datetime.now():
            raise ValueError("Reservation date cannot be in the past.")
        if reservation_date > datetime.now() + timedelta(days=60):
            raise ValueError("Reservation date cannot be more than 2 months in advance.")
        
        return date

    @staticmethod
    def validate_time(time):
        try:
            reservation_time = datetime.strptime(time, '%H:%M').time()
        except ValueError:
            raise ValueError("Invalid time format. Use HH:MM.")

        if not (datetime.strptime('10:00', '%H:%M').time() <= reservation_time <= datetime.strptime('22:00', '%H:%M').time()):
            raise ValueError("Reservation time must be between 10:00 AM and 10:00 PM.")
        
        return time

    @staticmethod
    def validate_guests(guests):
        guests = int(guests)
        if guests <= 0 or guests > 15:
            raise ValueError("Number of guests must be between 1 and 15.")
        return guests

    def confirm_reservation(self):
        print(f"Reservation confirmed for {self.customer_name} on {self.date} at {self.time}, Table ID: {self.table_id}")

    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "contact": self.contact,
            "date": self.date,
            "time": self.time,
            "guests": self.guests,
            "table_id": self.table_id
        }
