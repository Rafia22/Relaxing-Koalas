import sqlite3

class Order:
    VALID_STATUSES = ["Pending", "In Preparation", "Completed", "Cancelled", "Paid"]

    def __init__(self, customer_id, table_id, items, status="Pending"):
        self.customer_id = customer_id
        self.table_id = table_id
        self.items = self.validate_items(items)
        self.status = self.validate_status(status)

    def save_to_db(self):
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO orders (customer_id, table_id, status) VALUES (?, ?, ?)', 
                           (self.customer_id, self.table_id, self.status))
            self.id = cursor.lastrowid
            for item in self.items:
                cursor.execute('INSERT INTO order_items (order_id, menu_item_id) VALUES (?, ?)', 
                               (self.id, item.id))
            conn.commit()

    def validate_items(self, items):
        if not items:
            raise ValueError("Order must contain at least one item.")
        return items

    def validate_status(self, status):
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid order status. Valid statuses are: {', '.join(self.VALID_STATUSES)}.")
        return status

    def update_status(self, status):
        self.status = self.validate_status(status)
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE orders SET status = ? WHERE id = ?', (self.status, self.id))
            conn.commit()

    @property
    def total_cost(self):
        return sum(item.price for item in self.items)
