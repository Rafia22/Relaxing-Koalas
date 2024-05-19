class Invoice:
    def __init__(self, order):
        self.order = order
        self.amount_due = order.total_cost
        self.is_paid = False

    def process_payment(self, payment):
        self.is_paid = True
        payment.record_transaction(self.amount_due)

    def __str__(self):
        return f"Invoice for {self.order.customer.name}. Amount Due: ${self.amount_due}. Paid: {self.is_paid}"
