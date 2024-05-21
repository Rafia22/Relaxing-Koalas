class Order:
    VALID_STATUSES = ["Pending", "In Preparation", "Completed", "Cancelled", "Paid"]

    def __init__(self, id, customer, table_id, items, status="Pending"):
        self.id = id
        self.customer = customer
        self.table_id = table_id
        self.items = self.validate_items(items)
        self.status = self.validate_status(status)

    def validate_items(self, items):
        if not items:
            raise ValueError("Order must contain at least one item.")
        return items

    def validate_status(self, status):
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid order status. Valid statuses are: {', '.join(self.VALID_STATUSES)}.")
        return status

    def update_status(self, status):
        self.status = self.validate_status(status)

    def to_dict(self):
        return {
            "id": self.id,
            "customer": self.customer.name,
            "table_id": self.table_id,
            "items": self.items,
            "status": self.status
        }

    @property
    def total_cost(self):
        return sum(item.price for item in self.items)
