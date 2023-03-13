from src.entities.entity import Entity

class Food(Entity):
    def __init__(self, board, position, id, energyVal) -> None:
        super().__init__(board, position, id)
        self.energyVal = energyVal