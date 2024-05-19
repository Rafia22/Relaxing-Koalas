class Kitchen:
    def __init__(self):
        self.orders = []

    def receive_order(self, order):
        self.orders.append(order)
        order.update_status('In Preparation')

    def complete_order(self, order):
        order.update_status('Completed')

    def __str__(self):
        return f"Kitchen: {len(self.orders)} orders"
