from Customer import Customer
from Reservation import Reservation
from Order import Order
from Kitchen import Kitchen
from Table import Table
from MenuItem import MenuItem
from Invoice import Invoice
from Payment import Payment
from datetime import datetime

def print_menu():
    print("\nRestaurant System Menu:")
    print("1. Make a Reservation")
    print("2. Place an Order")
    print("3. View Kitchen Orders")
    print("4. Generate Invoice")
    print("5. Process Payment")
    print("6. Exit")

def validate_input(prompt, validation_func=None):
    while True:
        user_input = input(prompt)
        if validation_func:
            try:
                return validation_func(user_input)
            except ValueError as e:
                print(f"Error: {e}")
        else:
            return user_input

def validate_positive_int(value):
    if not value.isdigit() or int(value) <= 0:
        raise ValueError("Please enter a positive integer.")
    return int(value)

def check_table_availability(reservations, table_id, date, time):
    for reservation in reservations:
        if reservation.table_id == table_id and reservation.date == date and reservation.time == time:
            return False
    return True

def make_reservation(customers, tables, reservations):
    name = validate_input("Enter customer name: ", Reservation.validate_name)
    contact = validate_input("Enter customer contact: ", Reservation.validate_contact)
    date = validate_input("Enter reservation date (YYYY-MM-DD): ", Reservation.validate_date)
    time = validate_input("Enter reservation time (HH:MM): ", Reservation.validate_time)
    guests = validate_input("Enter number of guests: ", Reservation.validate_guests)
    table_id = validate_input("Enter table number: ", validate_positive_int)

    if table_id > len(tables):
        print("Error: Table number does not exist.")
        return

    if not check_table_availability(reservations, table_id, date, time):
        print("Error: Table is already reserved for the specified date and time.")
        return

    table = tables[table_id - 1]
    
    try:
        reservation = Reservation(len(reservations) + 1, name, contact, date, time, guests, table_id)
        customer = Customer(name, contact)
        customer.make_reservation(reservation)
        customers.append(customer)
        reservations.append(reservation)

        reservation.confirm_reservation()
        table.reserve()
        
    except ValueError as e:
        print(f"Error: {e}")

def place_order(customers, menu_items, kitchen):
    customer_name = validate_input("Enter customer name: ")
    customer = next((c for c in customers if c.name == customer_name), None)
    
    if customer:
        if not customer.reservations:
            print("Customer has no reservations.")
            return

        print("Menu Items:")
        for item in menu_items:
            print(f"{item.name} - ${item.price}")
        
        item_names = validate_input("Enter the names of the items to order (comma-separated): ")
        item_names = [name.strip() for name in item_names.split(",")]

        order_items = []
        for name in item_names:
            item = next((item for item in menu_items if item.name == name), None)
            if item:
                order_items.append(item)
            else:
                print(f"Error: '{name}' is not a valid menu item.")
                return
        
        try:
            order = Order(len(customer.orders) + 1, customer, customer.reservations[-1].table_id, order_items)
            customer.place_order(order)
            kitchen.receive_order(order)
        
            print(f"Order placed for {customer.name}")
        except ValueError as e:
            print(f"Error: {e}")
    else:
        print("Customer not found.")

def view_kitchen_orders(kitchen):
    print("Kitchen Orders:")
    for order in kitchen.orders:
        print(f"Customer: {order.customer.name}, Status: {order.status}")
        print("Items:")
        for item in order.items:
            print(f" - {item.name}: ${item.price}")
        print("Total Cost:", order.total_cost)
        print("-" * 20)

def generate_invoice(customers):
    customer_name = validate_input("Enter customer name: ")
    customer = next((c for c in customers if c.name == customer_name), None)
    
    if customer:
        unpaid_orders = [order for order in customer.orders if order.status != 'Paid']
        if unpaid_orders:
            invoice = Invoice(unpaid_orders)
            print(invoice)
            return invoice
        else:
            print(f"All orders for {customer.name} are already paid.")
            return None
    else:
        print("Customer not found.")
        return None

def process_payment(customers, payments):
    customer_name = validate_input("Enter customer name: ")
    customer = next((c for c in customers if c.name == customer_name), None)
    
    if customer:
        unpaid_orders = [order for order in customer.orders if order.status != 'Paid']
        if unpaid_orders:
            invoice = Invoice(unpaid_orders)
            invoice.process_payment(payments)
            print(f"Payment processed for {customer.name}.")
        else:
            print(f"All orders for {customer.name} are already paid.")
    else:
        print("Customer not found.")

def main():
    menu_items = [
        MenuItem(1, "Pizza", 10.0),
        MenuItem(2, "Burger", 8.0),
        MenuItem(3, "Salad", 7.0)
    ]
    tables = [Table(i, 4) for i in range(1, 11)]
    kitchen = Kitchen()
    payments = Payment()
    customers = []
    reservations = []

    while True:
        print_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            make_reservation(customers, tables, reservations)
        elif choice == '2':
            place_order(customers, menu_items, kitchen)
        elif choice == '3':
            view_kitchen_orders(kitchen)
        elif choice == '4':
            generate_invoice(customers)
        elif choice == '5':
            process_payment(customers, payments)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
