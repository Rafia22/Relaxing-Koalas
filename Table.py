import sqlite3

class Table:
    VALID_STATUSES = ["Available", "Reserved", "Occupied"]

    def __init__(self, table_id, capacity):
        self.table_id = table_id
        self.capacity = self.validate_capacity(capacity)
        self.status = "Available"

    def validate_capacity(self, capacity):
        if capacity <= 0:
            raise ValueError("Seating capacity must be greater than zero.")
        return capacity

    def reserve(self):
        if self.status == "Available":
            self.status = "Reserved"
        else:
            raise ValueError("Table is already reserved or occupied.")

    def release(self):
        if self.status == "Reserved":
            self.status = "Available"
        else:
            raise ValueError("Table is not reserved.")

    def __str__(self):
        return f"Table {self.table_id} for {self.capacity} people. Status: {self.status}"
    
    def check_table_availability(table_id, date, time):
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM reservations WHERE table_id = ? AND date = ? AND time = ?', (table_id, date, time))
            count = cursor.fetchone()[0]
            return count == 0

