class Invoice:
    def __init__(self, orders):
        self.orders = orders
        self.amount_due = self.calculate_total_cost()
        self.is_paid = False

    def calculate_total_cost(self):
        return sum(order.total_cost for order in self.orders)

    def process_payment(self, payment):
        self.is_paid = True
        payment.record_transaction(self.amount_due)
        for order in self.orders:
            order.update_status('Paid')

    def __str__(self):
        orders_info = "\n".join([f"Order ID: {order.id}, Items: {[item.name for item in order.items]}, Total: ${order.total_cost}" for order in self.orders])
        return f"Invoice:\n{orders_info}\nAmount Due: ${self.amount_due}. Paid: {self.is_paid}"
