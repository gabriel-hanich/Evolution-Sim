class animal:
    def __innit__(self, startingPos, startingHealth, maxHealth, speed, startingEnergy, maxEnergy, efficiency, sensingRange):
        self.pos = startingPos # Where the animal starts on the board (in form [x, y])
        self.health = startingHealth # How much health the animal starts with
        self.maxHealth = maxHealth # The maximum health score an animal can have
        self.speed = speed # How many boxes the animal can move per turn
        self.energy= startingEnergy # How much energy the animal starts with
        self.maxEnergy = maxEnergy # The maximum energy the animal can have
        self.efficiency = efficiency # How efficiently an animal can function (how much or little energy a task takes)
        self.sensingRange = sensingRange # How far the creature can 'sense' food or predators
        self.board = None # The board containing all the animals and food

    def updateBoard(self, board):
        self.board = board

class prey(animal):
    def searchForFood(self):
        print