from src.entities.food import Food
from src.entities.entity import Entity
from src.util.mathFuncs import calculateDistance, findCirclePoints, findFromProbabilities

class Prey(Entity):
    def __init__(self, board, position, id, efficiency, senseRange, moveRange) -> None:
        super().__init__(board, position, id)
        self.efficiency = efficiency
        self.senseRange = round(senseRange)
        self.moveRange = moveRange

        self.energy = 1

    def __str__(self) -> str:
        return f"PREY {self.id}\nCurrently Located at: x:{self.position[0]} y:{self.position[1]}\nEnergy: {self.energy}\nEfficiency, Sense, Move: {[self.efficiency, self.senseRange, self.moveRange]}"

    def makeMove(self):
        target = self.decideTarget()
        print(target)
        # self.move(target)

        # Remove necessary amount of energy
        return

    def decideTarget(self):
        # Decide the next target for the prey to go towards
        scanPoints = findCirclePoints(self.position, self.senseRange, (self.board.getShape()[0] - 1), (self.board.getShape()[1] - 1))
        foodSources = []
        totalDistance = 0
        for point in scanPoints:
            if(type(self.board.getEntity(point[0], point[1])) == Food):
                distance = calculateDistance(point, self.position)
                foodSources.append([point, distance])
                totalDistance += distance
        totalInvertedDistance = 0
        for point in foodSources:
            totalInvertedDistance += totalDistance - point[1]
        for point in foodSources:
            chance = (totalDistance - point[1]) / totalInvertedDistance
            point[1] = chance

        if(len(foodSources) == 1):
            return foodSources[0][0]
        elif(len(foodSources) == 0):
            return
        else:
            return findFromProbabilities(foodSources)[0]

