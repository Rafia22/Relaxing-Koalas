import sqlite3
from Order import Order
from MenuItem import MenuItem

class Kitchen:
    def __init__(self):
        self.orders = self.load_orders_from_db()

    def load_orders_from_db(self):
        orders = []
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, customer_id, table_id, status FROM orders')
            for row in cursor.fetchall():
                order_id = row[0]
                customer_id = row[1]
                table_id = row[2]
                status = row[3]
                cursor.execute('SELECT menu_items.id, menu_items.name, menu_items.price FROM order_items JOIN menu_items ON order_items.menu_item_id = menu_items.id WHERE order_items.order_id = ?', (order_id,))
                items_data = cursor.fetchall()
                items = [MenuItem(item[1], item[2]) for item in items_data]
                
                if items:
                    order = Order(customer_id, table_id, items, status)
                    order.id = order_id
                    orders.append(order)
                else:
                    print(f"Warning: Order ID {order_id} has no items.")
        return orders

    def receive_order(self, order):
        order.update_status('In Preparation')
        self.orders.append(order)


    def complete_order(self, order):
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM orders WHERE id = ?', (order.id,))
            cursor.execute('DELETE FROM order_items WHERE order_id = ?', (order.id,))
            conn.commit()
        self.orders = [o for o in self.orders if o.id != order.id]

    # The commented code is just to change the status. keeps it in the database.
    # def complete_order(self, order):
    #     order.update_status('Completed')
    #     with sqlite3.connect('restaurant.db') as conn:
    #         cursor = conn.cursor()
    #         cursor.execute('UPDATE orders SET status = ? WHERE id = ?', ('Completed', order.id))
    #         conn.commit()
