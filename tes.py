import customtkinter as ctk
from customtkinter import CTkImage
import sqlite3
from tkinter import messagebox
from PIL import Image
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

        ctk.set_appearance_mode("dark")  # Options: "light", "dark"
        ctk.set_default_color_theme("dark-blue")  # Options: "blue", "green", "dark-blue"

        self.customers = self.load_customers_from_db()
        self.reservations = self.load_reservations_from_db()
        self.tables = [Table(i, 4) for i in range(1, 11)]
        self.menu_items = self.load_menu_items_from_db()
        self.kitchen = Kitchen()
        self.kitchen.orders = self.kitchen.load_orders_from_db()
        self.payments = Payment()

        # Create a content frame for form fields
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.grid(row=1, column=0, columnspan=5)

        self.setup_gui()

    def setup_gui(self):
        # Load and resize images using Pillow
        self.reservation_img = CTkImage(Image.open("images/reservation.png"))
        self.order_img = CTkImage(Image.open("images/order.png"))
        self.kitchen_img = CTkImage(Image.open("images/kitchen.png"))
        self.invoice_img = CTkImage(Image.open("images/invoice.png"))
        self.payment_img = CTkImage(Image.open("images/payment.png"))

        # Create a frame to hold the buttons
        button_frame = ctk.CTkFrame(self.root)
        button_frame.grid(row=0, column=0, columnspan=5, pady=20)

        # Menu buttons with images
        ctk.CTkButton(button_frame, image=self.reservation_img, command=self.show_reservation_form, text="Book A Table", compound="top").grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkButton(button_frame, image=self.order_img, command=self.show_order_form, text="Place an Order", compound="top").grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkButton(button_frame, image=self.kitchen_img, command=self.view_kitchen_orders, text="View Orders", compound="top").grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkButton(button_frame, image=self.invoice_img, command=self.show_invoice_form, text="Generate Invoice", compound="top").grid(row=0, column=3, padx=10, pady=5)
        ctk.CTkButton(button_frame, image=self.payment_img, command=self.show_payment_form, text="Process Payment", compound="top").grid(row=0, column=4, padx=10, pady=5)

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

    def clear_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_reservation_form(self):
        self.clear_frame()

        ctk.CTkLabel(self.content_frame, text="Book a Table", font=("Arial", 20)).grid(row=0, column=0, columnspan=2, pady=10)
        # Customer Name
        ctk.CTkLabel(self.content_frame, text="Customer Name").grid(row=1, column=0, sticky=ctk.W, padx=10, pady=5)
        self.customer_name_entry = ctk.CTkEntry(self.content_frame)
        self.customer_name_entry.grid(row=1, column=1, padx=10, pady=5)

        # Customer Contact
        ctk.CTkLabel(self.content_frame, text="Customer Contact").grid(row=2, column=0, sticky=ctk.W, padx=10, pady=5)
        self.customer_contact_entry = ctk.CTkEntry(self.content_frame)
        self.customer_contact_entry.grid(row=2, column=1, padx=10, pady=5)

        # Reservation Date
        ctk.CTkLabel(self.content_frame, text="Reservation Date (YYYY-MM-DD)").grid(row=3, column=0, sticky=ctk.W, padx=10, pady=5)
        self.reservation_date_entry = ctk.CTkEntry(self.content_frame)
        self.reservation_date_entry.grid(row=3, column=1, padx=10, pady=5)

        # Reservation Time
        ctk.CTkLabel(self.content_frame, text="Reservation Time (HH:MM)").grid(row=4, column=0, sticky=ctk.W, padx=10, pady=5)
        self.reservation_time_entry = ctk.CTkEntry(self.content_frame)
        self.reservation_time_entry.grid(row=4, column=1, padx=10, pady=5)

        # Number of Guests
        ctk.CTkLabel(self.content_frame, text="Number of Guests").grid(row=5, column=0, sticky=ctk.W, padx=10, pady=5)
        self.guests_entry = ctk.CTkEntry(self.content_frame)
        self.guests_entry.grid(row=5, column=1, padx=10, pady=5)

        # Table Number
        ctk.CTkLabel(self.content_frame, text="Table Number").grid(row=6, column=0, sticky=ctk.W, padx=10, pady=5)
        self.table_number_entry = ctk.CTkEntry(self.content_frame)
        self.table_number_entry.grid(row=6, column=1, padx=10, pady=5)

        # Submit Button
        ctk.CTkButton(self.content_frame, text="Make Reservation", command=self.make_reservation).grid(row=7, column=0, columnspan=2, pady=10)

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
            
            self.customers.append(customer)
            self.reservations.append(reservation)
            
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
        menu_frame = ctk.CTkScrollableFrame(self.content_frame, width=400, height=200)
        menu_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=ctk.W)

        ctk.CTkLabel(menu_frame, text="Available Menu Items:").pack(anchor=ctk.W)

        for item in self.menu_items:
            ctk.CTkLabel(menu_frame, text=f"{item.name} - ${item.price:.2f}").pack(anchor=ctk.W)

        # Table Number
        ctk.CTkLabel(self.content_frame, text="Table Number").grid(row=1, column=0, sticky=ctk.W, padx=10, pady=5)
        self.order_table_number_entry = ctk.CTkEntry(self.content_frame)
        self.order_table_number_entry.grid(row=1, column=1, padx=10, pady=5)

        # Menu Items Entry
        ctk.CTkLabel(self.content_frame, text="Menu Items (comma-separated)").grid(row=2, column=0, sticky=ctk.W, padx=10, pady=5)
        self.menu_items_entry = ctk.CTkEntry(self.content_frame)
        self.menu_items_entry.grid(row=2, column=1, padx=10, pady=5)

        # Submit Button
        ctk.CTkButton(self.content_frame, text="Submit Order", command=self.place_order).grid(row=3, column=0, columnspan=2, pady=10)


    def place_order(self):
        table_number = self.order_table_number_entry.get()
        item_names = self.menu_items_entry.get().split(",")

        try:
            table_number = int(table_number)
        except ValueError:
            messagebox.showerror("Input Error", "Table number must be an integer.")
            return

        if table_number > len(self.tables) or table_number < 1:
            messagebox.showerror("Input Error", "Table number does not exist.")
            return

        # Ensure customers and reservations are properly loaded from the database
        self.customers = self.load_customers_from_db()
        self.reservations = self.load_reservations_from_db()

        # Find customer with a reservation for the given table number
        customer = next((c for c in self.customers if any(res.table_id == table_number and res.customer_id == c.id for res in self.reservations)), None)
        
        if customer:
            if not any(res.table_id == table_number for res in self.reservations if res.customer_id == customer.id):
                messagebox.showerror("Input Error", "Customer has no reservations.")
                return

            order_items = []
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
                customer.place_order(order)
                self.kitchen.receive_order(order)
                messagebox.showinfo("Success", f"Order placed for Table {table_number}")
                self.clear_frame()
            except ValueError as e:
                messagebox.showerror("Input Error", str(e))
        else:
            messagebox.showerror("Input Error", "Customer not found for the given table number.")


    def view_kitchen_orders(self):
        self.clear_frame()

        orders_by_table = {}

        # Group orders by table and customer
        for order in self.kitchen.orders:
            if order.status == "Completed":
                continue  # Skip completed orders
            if order.table_id not in orders_by_table:
                orders_by_table[order.table_id] = {}
            if order.customer_id not in orders_by_table[order.table_id]:
                orders_by_table[order.table_id][order.customer_id] = []
            orders_by_table[order.table_id][order.customer_id].append(order)

        row_index = 1
        for table_id, customers in orders_by_table.items():
            table_label = f"Table {table_id}"
            ctk.CTkLabel(self.content_frame, text=table_label).grid(row=row_index, column=0, sticky=ctk.W, padx=10, pady=5)
            row_index += 1

            for customer_id, orders in customers.items():
                with sqlite3.connect('restaurant.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('SELECT name FROM customers WHERE id = ?', (customer_id,))
                    customer_name = cursor.fetchone()[0]

                order_info = f"Customer: {customer_name}\nItems:"
                total_cost = 0
                for order in orders:
                    for item in order.items:
                        order_info += f"\n - {item.name}: ${item.price}"
                        total_cost += item.price
                    order_info += f"\nStatus: {order.status}\n{'-'*20}"
                order_info += f"\nTotal Cost: ${total_cost}\n{'-'*20}"
                ctk.CTkLabel(self.content_frame, text=order_info).grid(row=row_index, column=0, sticky=ctk.W, padx=10, pady=5)
                
                if any(order.status == "Paid" for order in orders):
                    complete_button = ctk.CTkButton(self.content_frame, text="Complete", command=lambda orders=orders: self.complete_orders(orders))
                    complete_button.grid(row=row_index, column=1, padx=10, pady=5)

                row_index += 1

    def complete_orders(self, orders):
        for order in orders:
            self.kitchen.complete_order(order)
        
        # Refresh kitchen orders after deletion
        self.kitchen.orders = self.kitchen.load_orders_from_db()
        self.view_kitchen_orders()


    def show_invoice_form(self):
        self.clear_frame()

        # Get table numbers with unpaid orders
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT table_id FROM orders WHERE status != "Paid"')
            table_numbers = [str(row[0]) for row in cursor.fetchall()]

        if not table_numbers:
            table_numbers = ["-"]

        ctk.CTkLabel(self.content_frame, text="Table Number").grid(row=1, column=0, sticky=ctk.W, padx=10, pady=5)
        self.invoice_table_number_combobox = ctk.CTkComboBox(self.content_frame, values=table_numbers)
        self.invoice_table_number_combobox.set("-" if table_numbers == ["-"] else table_numbers[0])
        self.invoice_table_number_combobox.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkButton(self.content_frame, text="Generate Invoice", command=self.generate_invoice).grid(row=2, column=0, columnspan=2, pady=10)



    def generate_invoice(self):
        table_number = self.invoice_table_number_combobox.get()
        if not table_number:
            messagebox.showerror("Input Error", "Please select a table number.")
            return

        table_number = int(table_number)

        unpaid_orders = [order for order in self.kitchen.orders if order.table_id == table_number and order.status != 'Paid']
        if unpaid_orders:
            invoice = Invoice(table_number, [order.id for order in unpaid_orders])
            invoice.save_to_db()
            messagebox.showinfo("Invoice", str(invoice))
        else:
            messagebox.showinfo("Invoice", f"All orders for Table {table_number} are already paid.")


    def show_payment_form(self):
        self.clear_frame()

        # Get table numbers with unpaid invoices
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT table_id FROM invoices WHERE is_paid = 0')
            table_numbers = [str(row[0]) for row in cursor.fetchall()]

        if not table_numbers:
            table_numbers = ["-"]

        ctk.CTkLabel(self.content_frame, text="Table Number").grid(row=1, column=0, sticky=ctk.W, padx=10, pady=5)
        self.payment_table_number_combobox = ctk.CTkComboBox(self.content_frame, values=table_numbers)
        self.payment_table_number_combobox.set("-" if table_numbers == ["-"] else table_numbers[0])
        self.payment_table_number_combobox.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkButton(self.content_frame, text="Process Payment", command=self.process_payment).grid(row=2, column=0, columnspan=2, pady=10)



    def get_unpaid_invoice_ids(self):
        invoice_ids = []
        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM invoices WHERE is_paid = 0')
            invoice_ids = [str(row[0]) for row in cursor.fetchall()]
        return invoice_ids

    def process_payment(self):
        table_number = self.payment_table_number_combobox.get()
        if not table_number:
            messagebox.showerror("Input Error", "Please select a table number.")
            return

        table_number = int(table_number)

        with sqlite3.connect('restaurant.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM invoices WHERE table_id = ? AND is_paid = 0', (table_number,))
            invoice_data = cursor.fetchone()
            
        if invoice_data:
            invoice = Invoice.load_from_db(invoice_data[0])
            invoice.process_payment()
            self.customers = self.load_customers_from_db()  # Refresh customers data
            self.reservations = self.load_reservations_from_db()  # Refresh reservations data
            self.kitchen.orders = self.kitchen.load_orders_from_db()  # Refresh kitchen orders data
            messagebox.showinfo("Success", f"Payment processed for Table {table_number}.")
        else:
            messagebox.showerror("Input Error", "No unpaid invoice found for the selected table.")



if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
