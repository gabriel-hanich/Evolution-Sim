class Entity():
    def __init__(self, board, position, id) -> None:
        self.board = board
        self.id = id
        self.isAlive = True
        self.move(position, False)
        pass

    def move(self, newPosition, clearOldSpot=True):
        if(clearOldSpot):
            self.board.clearPosition(self.position[0], self.position[1])
        self.board.placeEntity(self, newPosition[0], newPosition[1])
        self.position = newPosition