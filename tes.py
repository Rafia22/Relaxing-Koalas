import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import sqlite3
from Customer import Customer
from Reservation import Reservation
from Table import Table
from MenuItem import MenuItem
from Order import Order
from Kitchen import Kitchen
from Invoice import Invoice
from Payment import Payment

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Reservation System")
        
        # Set window size
        self.root.geometry("800x600")

        self.customers = self.load_customers_from_db()
        self.reservations = self.load_reservations_from_db()
        self.tables = [Table(i, 4) for i in range(1, 11)]
        self.menu_items = self.load_menu_items_from_db()
        self.kitchen = Kitchen()
        self.kitchen.orders = self.kitchen.load_orders_from_db()
        self.payments = Payment()

        # Create a content frame for form fields
        self.content_frame = tk.Frame(self.root)
        self.content_frame.grid(row=1, column=0, columnspan=5)

        self.setup_gui()

    def setup_gui(self):
        # Load and resize images using Pillow
        self.reservation_img = ImageTk.PhotoImage(Image.open("images/reservation.png").resize((75, 75), Image.Resampling.LANCZOS))
        self.order_img = ImageTk.PhotoImage(Image.open("images/order.png").resize((75, 75), Image.Resampling.LANCZOS))
        self.kitchen_img = ImageTk.PhotoImage(Image.open("images/kitchen.png").resize((75, 75), Image.Resampling.LANCZOS))
        self.invoice_img = ImageTk.PhotoImage(Image.open("images/invoice.png").resize((75, 75), Image.Resampling.LANCZOS))
        self.payment_img = ImageTk.PhotoImage(Image.open("images/payment.png").resize((75, 75), Image.Resampling.LANCZOS))

        # Create a frame to hold the buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=0, column=0, columnspan=5, pady=20, padx=60)

        # Menu buttons with images
        tk.Button(button_frame, image=self.reservation_img, command=self.show_reservation_form).grid(row=0, column=0, padx=25, pady=5)
        tk.Label(button_frame, text="Book A Table").grid(row=1, column=0)

        tk.Button(button_frame, image=self.order_img, command=self.show_order_form).grid(row=0, column=1, padx=25, pady=5)
        tk.Label(button_frame, text="Place an Order").grid(row=1, column=1)

        tk.Button(button_frame, image=self.kitchen_img, command=self.view_kitchen_orders).grid(row=0, column=2, padx=25, pady=5)
        tk.Label(button_frame, text="View Orders").grid(row=1, column=2)

        tk.Button(button_frame, image=self.invoice_img, command=self.show_invoice_form).grid(row=0, column=3, padx=25, pady=5)
        tk.Label(button_frame, text="Generate Invoice").grid(row=1, column=3)

        tk.Button(button_frame, image=self.payment_img, command=self.show_payment_form).grid(row=0, column=4, padx=25, pady=5)
        tk.Label(button_frame, text="Process Payment").grid(row=1, column=4)

    def clear_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def load_customers_from_db(self):
        customers = []
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, contact FROM customers')
            for row in cursor.fetchall():
                customer = Customer(row[1], row[2])
                customer.id = row[0]
                customers.append(customer)
        return customers

    def load_reservations_from_db(self):
        reservations = []
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, customer_id, date, time, guests, table_id FROM reservations')
            for row in cursor.fetchall():
                reservation = Reservation(row[1], row[2], row[3], row[4], row[5])
                reservation.id = row[0]
                reservations.append(reservation)
        return reservations

    def load_menu_items_from_db(self):
        menu_items = []
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, price FROM menu_items')
            for row in cursor.fetchall():
                menu_item = MenuItem(row[1], row[2])
                menu_item.id = row[0]
                menu_items.append(menu_item)
        return menu_items
    
    

    def show_reservation_form(self):
        self.clear_frame()

        # Customer Name
        tk.Label(self.content_frame, text="Customer Name").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.customer_name_entry = tk.Entry(self.content_frame)
        self.customer_name_entry.grid(row=1, column=1, padx=10, pady=5)

        # Customer Contact
        tk.Label(self.content_frame, text="Customer Contact").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.customer_contact_entry = tk.Entry(self.content_frame)
        self.customer_contact_entry.grid(row=2, column=1, padx=10, pady=5)

        # Reservation Date
        tk.Label(self.content_frame, text="Reservation Date (YYYY-MM-DD)").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.reservation_date_entry = tk.Entry(self.content_frame)
        self.reservation_date_entry.grid(row=3, column=1, padx=10, pady=5)

        # Reservation Time
        tk.Label(self.content_frame, text="Reservation Time (HH:MM)").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        self.reservation_time_entry = tk.Entry(self.content_frame)
        self.reservation_time_entry.grid(row=4, column=1, padx=10, pady=5)

        # Number of Guests
        tk.Label(self.content_frame, text="Number of Guests").grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        self.guests_entry = tk.Entry(self.content_frame)
        self.guests_entry.grid(row=5, column=1, padx=10, pady=5)

        # Table Number
        tk.Label(self.content_frame, text="Table Number").grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)
        self.table_number_entry = tk.Entry(self.content_frame)
        self.table_number_entry.grid(row=6, column=1, padx=10, pady=5)

        # Submit Button
        tk.Button(self.content_frame, text="Make Reservation", command=self.make_reservation).grid(row=7, column=0, columnspan=2, pady=10)

    def make_reservation(self):
        name = self.customer_name_entry.get()
        contact = self.customer_contact_entry.get()
        date = self.reservation_date_entry.get()
        time = self.reservation_time_entry.get()
        guests = self.guests_entry.get()
        table_id = self.table_number_entry.get()

        # Validate and convert guests and table_id
        try:
            guests = int(guests)
        except ValueError:
            messagebox.showerror("Input Error", "Number of guests must be an integer.")
            return

        try:
            table_id = int(table_id)
        except ValueError:
            messagebox.showerror("Input Error", "Table number must be an integer.")
            return

        if table_id > len(self.tables) or table_id < 1:
            messagebox.showerror("Input Error", "Table number does not exist.")
            return

        if not self.check_table_availability(table_id, date, time):
            messagebox.showerror("Input Error", "Table is already reserved for the specified date and time.")
            return

        try:
            customer = Customer(name, contact)
            customer.save_to_db()
            
            reservation = Reservation(customer.id, date, time, guests, table_id)
            reservation.save_to_db()
            
            self.customers = self.load_customers_from_db()  # Refresh customers data
            self.reservations = self.load_reservations_from_db()  # Refresh reservations data
            
            self.tables[table_id - 1].reserve()
            messagebox.showinfo("Success", f"Reservation confirmed for {name}")
            self.clear_frame()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def check_table_availability(self, table_id, date, time):
        for reservation in self.reservations:
            if reservation.table_id == table_id and reservation.date == date and reservation.time == time:
                return False
        return True

    def show_order_form(self):
        self.clear_frame()

        # Display Menu Items in a scrollable frame
        menu_frame = tk.Frame(self.content_frame)
        menu_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(menu_frame, height=150, width=400)
        scrollbar = tk.Scrollbar(menu_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        tk.Label(scrollable_frame, text="Available Menu Items:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        for i, item in enumerate(self.menu_items):
            row = i // 2 + 1
            col = i % 2
            tk.Label(scrollable_frame, text=f"{item.name} - ${item.price:.2f}").grid(row=row, column=col, padx=10, pady=5)

        # Table Number
        tk.Label(self.content_frame, text="Table Number").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.order_table_number_entry = tk.Entry(self.content_frame)
        self.order_table_number_entry.grid(row=1, column=1, padx=10, pady=5)

        # Menu Items Entry
        tk.Label(self.content_frame, text="Menu Items (comma-separated)").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.menu_items_entry = tk.Entry(self.content_frame)
        self.menu_items_entry.grid(row=2, column=1, padx=10, pady=5)

        # Submit Button
        tk.Button(self.content_frame, text="Submit Order", command=self.place_order).grid(row=3, column=0, columnspan=2, pady=10)


    def place_order(self):
        table_number = self.order_table_number_entry.get()
        try:
            table_number = int(table_number)
        except ValueError:
            messagebox.showerror("Input Error", "Table number must be an integer.")
            return

        if table_number > len(self.tables) or table_number < 1:
            messagebox.showerror("Input Error", "Table number does not exist.")
            return

        customer = next((c for c in self.customers if any(res.table_id == table_number for res in self.reservations if res.customer_id == c.id)), None)

        if customer:
            order_items = []
            item_names = self.menu_items_entry.get().split(",")
            for name in item_names:
                item = next((item for item in self.menu_items if item.name.strip().lower() == name.strip().lower()), None)
                if item:
                    order_items.append(item)
                else:
                    messagebox.showerror("Input Error", f"'{name}' is not a valid menu item.")
                    return

            try:
                order = Order(customer.id, table_number, order_items)
                order.save_to_db()
                self.kitchen.receive_order(order)
                self.customers = self.load_customers_from_db()  # Refresh customers data
                self.reservations = self.load_reservations_from_db()  # Refresh reservations data
                messagebox.showinfo("Success", f"Order placed for Table {table_number}")
                self.clear_frame()
            except ValueError as e:
                messagebox.showerror("Input Error", str(e))
        else:
            messagebox.showerror("Input Error", "Customer not found for the given table number.")


    def view_kitchen_orders(self):
        self.clear_frame()

        tk.Label(self.content_frame, text="Kitchen Orders").grid(row=0, column=0, sticky=tk.W)

        for i, order in enumerate(self.kitchen.orders):
            customer_name = next((c.name for c in self.customers if c.id == order.customer_id), "Unknown Customer")
            order_info = f"Customer: {customer_name}, Status: {order.status}\nItems:"
            for item in order.items:
                order_info += f"\n - {item.name}: ${item.price}"
            order_info += f"\nTotal Cost: ${order.total_cost}\n{'-'*20}"

            tk.Label(self.content_frame, text=order_info).grid(row=i + 1, column=0, sticky=tk.W)

            if order.status == 'Paid':
                complete_button = tk.Button(self.content_frame, text="Complete", command=lambda o=order: self.complete_order(o))
                complete_button.grid(row=i + 1, column=1, padx=10, pady=5)

    def complete_order(self, order):
        self.kitchen.complete_order(order)
        # This commented line removes the view but stays in the database.
        # self.kitchen.orders = [o for o in self.kitchen.orders if o.id != order.id]  # Remove completed order
        self.view_kitchen_orders()  # Refresh the view

    def show_invoice_form(self):
        self.clear_frame()

        tk.Label(self.content_frame, text="Table Number").grid(row=1, column=0, sticky=tk.W)
        self.invoice_table_number_entry = tk.Entry(self.content_frame)
        self.invoice_table_number_entry.grid(row=1, column=1)

        tk.Button(self.content_frame, text="Generate Invoice", command=self.generate_invoice).grid(row=2, column=0, columnspan=2, pady=10)


    def generate_invoice(self):
        table_number = self.invoice_table_number_entry.get()
        try:
            table_number = int(table_number)
        except ValueError:
            messagebox.showerror("Input Error", "Table number must be an integer.")
            return

        if table_number > len(self.tables) or table_number < 1:
            messagebox.showerror("Input Error", "Table number does not exist.")
            return

        customer = next((c for c in self.customers if any(res.table_id == table_number for res in self.reservations if res.customer_id == c.id)), None)

        if customer:
            unpaid_orders = [order for order in self.kitchen.orders if order.table_id == table_number and order.status != 'Paid']
            if unpaid_orders:
                invoice = Invoice([order.id for order in unpaid_orders])
                invoice.save_to_db()
                messagebox.showinfo("Invoice", str(invoice))
            else:
                messagebox.showinfo("Invoice", f"All orders for Table {table_number} are already paid.")
        else:
            messagebox.showerror("Input Error", "Customer not found for the given table number.")


    def show_payment_form(self):
        self.clear_frame()

        tk.Label(self.content_frame, text="Table Number").grid(row=1, column=0, sticky=tk.W)
        self.payment_table_number_entry = tk.Entry(self.content_frame)
        self.payment_table_number_entry.grid(row=1, column=1)

        tk.Button(self.content_frame, text="Process Payment", command=self.process_payment).grid(row=2, column=0, columnspan=2, pady=10)


    def process_payment(self):
        table_number = self.payment_table_number_entry.get()
        try:
            table_number = int(table_number)
        except ValueError:
            messagebox.showerror("Input Error", "Table number must be an integer.")
            return

        if table_number > len(self.tables) or table_number < 1:
            messagebox.showerror("Input Error", "Table number does not exist.")
            return

        customer = next((c for c in self.customers if any(res.table_id == table_number for res in self.reservations if res.customer_id == c.id)), None)

        if customer:
            unpaid_orders = [order for order in self.kitchen.orders if order.table_id == table_number and order.status != 'Paid']
            if unpaid_orders:
                invoice = Invoice([order.id for order in unpaid_orders])
                invoice.process_payment()
                self.customers = self.load_customers_from_db()  # Refresh customers data
                self.reservations = self.load_reservations_from_db()  # Refresh reservations data
                self.kitchen.orders = self.kitchen.load_orders_from_db()
                messagebox.showinfo("Success", f"Payment processed for Table {table_number}.")
            else:
                messagebox.showinfo("Success", f"All orders for Table {table_number} are already paid.")
        else:
            messagebox.showerror("Input Error", "Customer not found for the given table number.")



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()