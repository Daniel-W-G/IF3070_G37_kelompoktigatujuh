class Vehicle:
    def __init__(self, id: str, width: int, length: int, shipping_fee: float, weight: float, eta: int):
        self.id: str = id
        self.width: int = width
        self.length: int = length
        self.shipping_fee: float = shipping_fee
        self.weight: float = weight
        self.eta: int = eta