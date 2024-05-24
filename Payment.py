import sqlite3

class Payment:
    def __init__(self):
        self.transactions = []

    def record_transaction(self, amount):
        if amount <= 0:
            raise ValueError("Transaction amount must be positive.")
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO payments (amount) VALUES (?)', (amount,))
            self.transactions.append(cursor.lastrowid)
            conn.commit()
