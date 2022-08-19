from fileinput import close
import math
from turtle import pos, speed
from src.mathFuncs import *

class goal:
    def __init__(self, type, startTime, endTime, endLocation):
        self.type = type
        self.startTime = startTime
        self.endTime = endTime
        self.endPos = endLocation

class entity:
    def __init__(self, id, startingPos):
        self.board = None
        self.position = startingPos
        self.id = id        
        self.time = 0

    def updateConstants(self, board, time):
        # Update the internally constants
        self.board = board
        self.time = time

    def getBoard(self):
        # Get the board 
        return self.board
    
    def scanBoards(self):
        # Find all the boxes within the entities sensing field
        return findCircleInteriorPoints(self.position, self.sensingRange, list(self.board.shape))

class foodSource(entity):
    def __init__(self, id, startingPos, energyProvided):
        self.id = id
        self.position = startingPos
        self.energy = energyProvided

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
        self.currentGoal = None
        self.time = 0
        self.efficiency = round(math.log(self.speed / 3) + 1, 3)

    def executeGoal(self):
        # Execute the current goal for the animal
        if self.currentGoal != None:
            if self.currentGoal.type == "move":
                # Calculate the distance of the move
                distance = findDistance(self.position, self.currentGoal.endPos)
                if distance < self.speed: # If the animal can move to the location in one turn
                    currentMoveTarget = self.currentGoal.endPos
                else:
                    # Find a point that is on the way between the current position and the end location 
                    smallestEndDistance = 1000 
                    for i in range(math.floor(self.speed)):
                        points = findCircleInteriorPoints(self.position, self.speed - i, list(self.board.shape))
                        for point in points:
                            pointOccupier = self.board[point[0]][point[1]]
                            if pointOccupier == None or type(pointOccupier) == foodSource:
                                endDistance = findDistance(point, self.currentGoal.endPos)
                                if endDistance < smallestEndDistance:
                                    smallestEndDistance = endDistance
                                    currentMoveTarget = point
                        if smallestEndDistance < distance:
                            break

                self.board[self.position[0]][self.position[1]] = None
                self.board[currentMoveTarget[0]][currentMoveTarget[1]] = self
                self.position = currentMoveTarget
                 
                if self.position == self.currentGoal.endPos:
                    self.currentGoal = None

class prey(animal):
    # Decision making functions
    def findFood(self):
        # Move to the closest food source 
        coords = self.scanBoards()
        # Find the closest food source
        smallestDistance = self.sensingRange
        closestSource = None
        for position in coords:
            if type(self.board[position[0]][position[1]]) == foodSource:
                distance = findDistance(self.position, position)
                if distance < smallestDistance:
                    smallestDistance = distance
                    closestSource = position
        if closestSource != None:
            self.currentGoal = goal("move", self.time, (self.time + math.ceil(smallestDistance / self.speed)), closestSource)
    
    