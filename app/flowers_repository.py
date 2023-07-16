from attrs import define


@define
class Flower:
    name: str
    count: int
    cost: int
    id: int = 0


class FlowersRepository:
    flowers: list[Flower]

    def __init__(self):
        self.flowers = []
        self.cart_flowers = []

    # необходимые методы сюда
    def get_all(self):
        return self.flowers
    
    def get_by_id(self, id: int) -> Flower:
        for flower in self.flowers:
            if flower.id == id:
                return flower
        return None

    def save(self, new_flower: Flower):
        new_flower.id = len(self.flowers) + 1
        self.flowers.append(new_flower)

    def add_cart_flowers(self, new_cart_flower: Flower):
        self.cart_flowers.append(new_cart_flower)

    def get_cart_flowers(self):
        return self.cart_flowers
    # конец решения
