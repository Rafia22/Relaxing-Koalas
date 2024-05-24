import sqlite3

class Invoice:
    def __init__(self, table_id, order_ids):
        self.table_id = table_id
        self.order_ids = order_ids
        self.amount_due = self.calculate_total_cost()
        self.is_paid = False

    def calculate_total_cost(self):
        total_cost = 0
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            for order_id in self.order_ids:
                cursor.execute('SELECT menu_items.price FROM order_items JOIN menu_items ON order_items.menu_item_id = menu_items.id WHERE order_items.order_id = ?', (order_id,))
                total_cost += sum(row[0] for row in cursor.fetchall())
        return total_cost

    def save_to_db(self):
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO invoices (table_id, amount_due, is_paid) VALUES (?, ?, ?)', (self.table_id, self.amount_due, self.is_paid))
            self.id = cursor.lastrowid
            for order_id in self.order_ids:
                cursor.execute('UPDATE orders SET invoice_id = ? WHERE id = ?', (self.id, order_id))
            conn.commit()

    def process_payment(self):
        self.is_paid = True
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE invoices SET is_paid = 1 WHERE id = ?', (self.id,))
            cursor.execute('UPDATE orders SET status = "Paid" WHERE table_id = ?', (self.table_id,))
            conn.commit()

    @staticmethod
    def load_from_db(invoice_id):
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, table_id, amount_due, is_paid FROM invoices WHERE id = ?', (invoice_id,))
            invoice_data = cursor.fetchone()
            cursor.execute('SELECT id FROM orders WHERE invoice_id = ?', (invoice_id,))
            order_ids = [row[0] for row in cursor.fetchall()]
        invoice = Invoice(invoice_data[1], order_ids)
        invoice.id = invoice_data[0]
        invoice.amount_due = invoice_data[2]
        invoice.is_paid = invoice_data[3]
        return invoice

    def __str__(self):
        return f"Invoice ID: {self.id}, Table ID: {self.table_id}, Amount Due: {self.amount_due}, Paid: {self.is_paid}"
