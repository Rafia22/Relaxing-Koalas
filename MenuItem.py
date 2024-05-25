import sqlite3

class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def save_to_db(self):
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO menu_items (name, price) VALUES (?, ?)', 
                           (self.name, self.price))
            self.id = cursor.lastrowid
            conn.commit()

    @staticmethod
    def load_menu_items_from_db():
        menu_items = []
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, price FROM menu_items')
            for row in cursor.fetchall():
                menu_item = MenuItem(row[1], row[2])
                menu_item.id = row[0]
                menu_items.append(menu_item)
        return menu_items