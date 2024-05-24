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
