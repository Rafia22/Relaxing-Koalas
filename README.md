# Relaxing-Koala Restaurant Reservation System

## Introduction

The Relaxing-Koala Restaurant Reservation System is designed to automate the reservation, order management, and payment processing operations for a mid-sized restaurant. The system provides a seamless and integrated platform for managing reservations, orders, kitchen workflows, invoicing, and payments.

## Features

- **Customer Management:** Add and manage customer information.
- **Reservation System:** Make and manage table reservations.
- **Order Handling:** Place and manage orders.
- **Kitchen Management:** View and manage kitchen orders.
- **Payment Processing:** Generate invoices and process payments.

## Prerequisites

- Python 3.x
- SQLite3
- `pip` package manager

## Setup Instructions

### Step 1: Install Dependencies
Install the required Python packages using 'pip':
```pip install customtkinter pillow```

### Step 2: Set Up the Database
Initialize the SQLite Database:
```python3 setup_db.py```
Then insert the data into the database:

```INSERT INTO menu_items (id, name, price) VALUES ```
```(1, 'Margherita Pizza', 8.5),```
```(2, 'Pepperoni Pizza', 9.0),```
```(3, 'BBQ Chicken Pizza', 10.0),```
```(4, 'Veggie Pizza', 8.5),```
```(5, 'Cheeseburger', 7.5),```
```(6, 'Bacon Cheeseburger', 8.5),```
```(7, 'Chicken Sandwich', 7.0),```
```(8, 'Caesar Salad', 6.0),```
```(9, 'Garden Salad', 5.5),```
```(10, 'Spaghetti Carbonara', 9.5),```
```(11, 'Fettuccine Alfredo', 9.0),```
```(12, 'Lasagna', 10.0),```
```(13, 'Garlic Bread', 3.5),```
```(14, 'Mozzarella Sticks', 5.0),```
```(15, 'French Fries', 3.0),```
```(16, 'Onion Rings', 4.0),```
```(17, 'Tiramisu', 5.5),```
```(18, 'Cheesecake', 5.0),```
```(19, 'Chocolate Cake', 5.0),```
```(20, 'Coffee', 2.5),```
```(21, 'Tea', 2.0),```
```(22, 'Soft Drink', 1.5);```

### Step 3: Run the Application
To start the application, run:
```python3 tes.py```