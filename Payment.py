class Payment:
    def __init__(self):
        self.transactions = []

    def record_transaction(self, amount):
        self.transactions.append(amount)

    def __str__(self):
        return f"Payment: {len(self.transactions)} transactions"
