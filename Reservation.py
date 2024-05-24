import sqlite3
from datetime import datetime, timedelta

class Reservation:
    def __init__(self, customer_id, date, time, guests, table_id):
        self.customer_id = customer_id
        self.date = self.validate_date(date)
        self.time = self.validate_time(time)
        self.guests = self.validate_guests(guests)
        self.table_id = table_id

    def save_to_db(self):
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO reservations (customer_id, date, time, guests, table_id) VALUES (?, ?, ?, ?, ?)', 
                           (self.customer_id, self.date, self.time, self.guests, self.table_id))
            self.id = cursor.lastrowid
            conn.commit()

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
        print(f"Reservation confirmed for Customer ID {self.customer_id} on {self.date} at {self.time}, Table ID: {self.table_id}")
