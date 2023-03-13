from src.entities.entity import Entity


class Predator(Entity):
    def __init__(self, board, position, id, efficiency, senseRange, moveRange) -> None:
        super().__init__(board, position, id)
        self.efficiency = efficiency
        self.senseRange = senseRange
        self.moveRange = moveRange

        self.energy = 1

    
    def decideTarget(self):
        # Decide the next target for the prey to go towards
        return

    def makeMove(self):
        target = self.decideTarget()
        # self.move(target)

        # Remove necessary amount of energy
        return