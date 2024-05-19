class Table:
    def __init__(self, table_id, capacity):
        self.table_id = table_id
        self.capacity = capacity
        self.is_reserved = False

    def reserve(self):
        self.is_reserved = True

    def release(self):
        self.is_reserved = False

    def __str__(self):
        return f"Table {self.table_id} for {self.capacity} people. Reserved: {self.is_reserved}"
