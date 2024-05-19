from Customer import Customer
from Reservation import Reservation
from Order import Order
from Kitchen import Kitchen
from Table import Table
from MenuItem import MenuItem
from Invoice import Invoice
from Payment import Payment

def print_menu():
    print("\nRestaurant System Menu:")
    print("1. Make a Reservation")
    print("2. Place an Order")
    print("3. View Kitchen Orders")
    print("4. Generate Invoice")
    print("5. Process Payment")
    print("6. Exit")

def make_reservation(customers, tables):
    name = input("Enter customer name: ")
    contact = input("Enter customer contact: ")
    date = input("Enter reservation date (YYYY-MM-DD): ")
    time = input("Enter reservation time (HH:MM): ")
    guests = int(input("Enter number of guests: "))
    table_id = int(input("Enter table number: "))
    table = tables[table_id - 1]
    
    customer = Customer(name, contact)
    reservation = Reservation(customer, date, time, guests, table)
    customer.make_reservation(reservation)
    customers.append(customer)
    
    reservation.confirm_reservation()
    table.reserve()
    
    print(f"Reservation confirmed for {customer.name}")

def place_order(customers, menu_items, kitchen):
    customer_name = input("Enter customer name: ")
    customer = next((c for c in customers if c.name == customer_name), None)
    
    if customer:
        print("Menu Items:")
        for item in menu_items:
            print(f"{item.name} - ${item.price}")
        
        item_names = input("Enter the names of the items to order (comma-separated): ").split(", ")
        order_items = [item for item in menu_items if item.name in item_names]
        
        order = Order(customer, order_items)
        customer.place_order(order)
        kitchen.receive_order(order)
        
        print(f"Order placed for {customer.name}")
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
    customer_name = input("Enter customer name: ")
    customer = next((c for c in customers if c.name == customer_name), None)
    
    if customer and customer.orders:
        invoice = Invoice(customer.orders[-1])
        print(f"Invoice for {customer.name}: Amount Due - ${invoice.amount_due}")
        return invoice
    else:
        print("Customer or order not found.")
        return None

def process_payment(customers, payments):
    customer_name = input("Enter customer name: ")
    customer = next((c for c in customers if c.name == customer_name), None)
    
    if customer and customer.orders:
        invoice = Invoice(customer.orders[-1])
        invoice.process_payment(payments)
        print(f"Payment processed for {customer.name}")
    else:
        print("Customer or order not found.")

def main():
    menu_items = [
        MenuItem("Pizza", "Cheese Pizza", 10.0),
        MenuItem("Burger", "Beef Burger", 8.0),
        MenuItem("Salad", "Caesar Salad", 7.0)
    ]
    tables = [Table(i, 4) for i in range(1, 11)]
    kitchen = Kitchen()
    payments = Payment()
    customers = []

    while True:
        print_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            make_reservation(customers, tables)
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
