from math import log


class entity:
    def __init__(self, id, startingPos):
        self.position = startingPos
        self.id = id        

    def updateBoard(self, board):
        # Update the internally stored board
        self.board = board

class animal(entity):
    def __init__(self, id, startingPos, maxHealth, speed, maxEnergy, sensingRange):
        self.id = id        
        self.position = startingPos # Where the animal starts on the board (in form [x, y])
        self.health = maxHealth # Assume that the animal starts with 100% health
        self.maxHealth = maxHealth # The maximum health score an animal can have
        self.speed = speed # How many boxes the animal can move per turn
        self.energy= maxEnergy # Assume the animal starts with full energy
        self.maxEnergy = maxEnergy # The maximum energy the animal can have
        self.sensingRange = sensingRange # How far the creature can 'sense' food or predators
        self.board = None # The board containing all the animals and food

        self.efficiency = round(log(self.speed / 3) + 1, 3)
        print("Animal init")



class prey(animal):
    def findFood(self):
        print("Looking for food")