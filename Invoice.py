import sqlite3

class Invoice:
    def __init__(self, order_ids):
        self.order_ids = order_ids
        self.amount_due = self.calculate_total_cost()
        self.is_paid = False

    def calculate_total_cost(self):
        total = 0
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            for order_id in self.order_ids:
                cursor.execute('SELECT menu_items.price FROM order_items JOIN menu_items ON order_items.menu_item_id = menu_items.id WHERE order_items.order_id = ?', (order_id,))
                for row in cursor.fetchall():
                    total += row[0]
        return total

    def save_to_db(self):
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            for order_id in self.order_ids:
                cursor.execute('INSERT INTO invoices (order_id, amount_due, is_paid) VALUES (?, ?, ?)', (order_id, self.amount_due, int(self.is_paid)))
            conn.commit()

    def process_payment(self):
        self.is_paid = True
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            for order_id in self.order_ids:
                cursor.execute('UPDATE invoices SET is_paid = 1 WHERE order_id = ?', (order_id,))
                cursor.execute('UPDATE orders SET status = ? WHERE id = ?', ('Paid', order_id))
            conn.commit()

    def __str__(self):
        return f"Invoice: Amount Due - ${self.amount_due}, Paid - {self.is_paid}"

