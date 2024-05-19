class Reservation:
    def __init__(self, id, customer_name, date, time, table_id):
        self.id = id
        self.customer_name = customer_name
        self.date = date
        self.time = time
        self.table_id = table_id

    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "date": self.date,
            "time": self.time,
            "table_id": self.table_id
        }
