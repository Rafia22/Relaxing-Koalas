class MenuItem:
    def __init__(self, id, name, price):
        self.id = id
        self.name = self.validate_name(name)
        self.price = self.validate_price(price)

    def validate_name(self, name):
        if not name:
            raise ValueError("Item name cannot be empty.")
        return name

    def validate_price(self, price):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        return price

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }
