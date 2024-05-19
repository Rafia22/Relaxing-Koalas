class Order:
    def __init__(self, id, table_id, items, status):
        self.id = id
        self.table_id = table_id
        self.items = items
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "table_id": self.table_id,
            "items": self.items,
            "status": self.status
        }
