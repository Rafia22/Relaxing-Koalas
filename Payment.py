class Payment:
    def __init__(self):
        self.transactions = []

    def record_transaction(self, amount):
        if amount <= 0:
            raise ValueError("Transaction amount must be positive.")
        self.transactions.append(amount)

    def __str__(self):
        return f"Payment: {len(self.transactions)} transactions"
