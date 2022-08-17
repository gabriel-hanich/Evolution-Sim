import math

class goal:
    def __init__(self, type, startTime, endTime, endLocation):
        self.type = type
        self.startTime = startTime
        self.endTime = endTime
        self.endPos = endLocation

class entity:
    def __init__(self, id, startingPos):
        self.position = startingPos
        self.id = id        
        self.time = 0

    def updateBoard(self, board, time):
        # Update the internally stored board
        self.board = board
        self.time = time

class foodSource(entity):
    def __init__(self, id, startingPos, energyProvided):
        self.id = id
        self.position = startingPos
        self.energy = energyProvided

class animal(entity):
    def __init__(self, id, startingPos, maxHealth, speed, maxEnergy, sensingRange):
        self.id = id        
        self.pos = startingPos # Where the animal starts on the board (in form [x, y])
        self.health = maxHealth # Assume that the animal starts with 100% health
        self.maxHealth = maxHealth # The maximum health score an animal can have
        self.speed = speed # How many boxes the animal can move per turn
        self.energy= maxEnergy # Assume the animal starts with full energy
        self.maxEnergy = maxEnergy # The maximum energy the animal can have
        self.sensingRange = sensingRange # How far the creature can 'sense' food or predators
        
        self.board = None # The board containing all the animals and food
        self.currentGoal = None
        self.time = 0
        self.efficiency = round(math.log(self.speed / 3) + 1, 3)


class prey(animal):
    def moveToFood(self):
        # Find all the boxes within the prey's sensing field
        for multiplier in [[-1, -1], [-1, 1], [1, -1], [1, 1]]: # Iterates through each of the 4 quadrants 
            for xOffset in range(self.sensingRange + 1):
                for yOffset in range(self.sensingRange + 1):
                    currentPos = [self.pos[0] + multiplier[0] * xOffset, self.pos[1] + multiplier[1] * yOffset] # The current position being scanned
                    distance = math.sqrt((self.pos[0] - currentPos[0]) ** 2 + (self.pos[1] - currentPos[1]) ** 2)
                    if distance <= self.sensingRange: # If the location is within scanning distance
                        try:
                            if type(self.board[currentPos[0]][currentPos[1]]) == foodSource:
                                print(f"Found food {round(distance, 3)} blocks away, my speed is {round(self.speed, 3)}, It will take {math.ceil(distance / self.speed)} turns to get there")
                                self.currentDecision = goal("move", self.time, self.time + math.ceil(distance / self.speed), currentPos)
                        except IndexError:
                            pass