from re import search
import re
from src.mathFuncs import *
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


class entity:
    def __init__(self, id, position, board) -> None:
        self.id = id
        self.position = position
        self.board = board
        self.currentTurn = 0
    
    def updateTurn(self):
        self.currentTurn += 1

class foodSource(entity):
    def __init__(self, id, position, board, energy) -> None:
        super().__init__(id, position, board)
        self.energy = energy

class animal(entity):
    def __init__(self, id, position, board, speed, sensingRange, dayCost) -> None:
        super().__init__(id, position, board)
        self.energy = 1
        self.speed = speed
        self.sensingRange = sensingRange
        self.dayCost = dayCost

        self.movementCost = round((math.log(self.speed + self.sensingRange) / 40), 3) # How much energy it costs to move 1 square
        self.goalList = []

    def updateVitals(self) -> None:
        # Update the energy of the animal,
        # Called at the start of every turn
        self.energy -= self.movementCost * self.dayCost
        self.updateTurn()
        if self.energy <= 0:
            self.board.removeEntityFromLocation(self.position)
            return False
        else:
            return True
    
    def move(self, newPosition):
        distance = findDistance(self.position, newPosition)
        if distance * self.movementCost >= self.energy:
            raise Exception(f"ANIMAL MOVEMENT ERROR\n{self.id} does not have enough energy to move {distance} blocks")
        else:
            self.board.moveEntity(self, self.position, newPosition)
            self.energy -= distance * self.movementCost
            self.position = newPosition

    def planMove(self, goal):
        # Move animal between two points, at the maximum possible distance allowed by the energy and speed restrictions
        biggestMove = math.floor(self.energy / self.movementCost) # The farthest possible distance the animal can go
        if biggestMove > self.speed:
            biggestMove = self.speed
        endTurnPos = [] # The position the animal will be at the end of the turn
        if findDistance(self.position, goal.endPosition) <= biggestMove:
            endTurnPos = goal.endPosition
            self.goalList.pop(0)
        else:
            smallestDistance = findDistance([0, 0], self.board.getShape())
            # Find the closest point to the end destination that is within the range an animal can move in a turn
            for point in findCircleInteriorPoints(self.position, biggestMove, self.board.getShape()):
                if self.board.getEntity(point) == None:
                    distance = findDistance(point, goal.endPosition)
                    if distance < biggestMove:
                        smallestDistance = distance 
                        endTurnPos = point
        if(endTurnPos == []):
            return # If no suitable location could be found, don't move at all

        if self.board.getEntity(endTurnPos) != None:
            # If the end turn position has an object on it, find a free space that is adgacent
            foundPos = False
            for xOffset in [-1, 0, 1]:
                for yOffset in [-1, 0, 1]:
                    coordinate = [endTurnPos[0] + xOffset, endTurnPos[1] + yOffset]
                    point = self.board.getEntity(coordinate) 
                    distance = findDistance(self.position, coordinate)
                    if point == None and distance <= biggestMove:
                            foundPos = True
                            endTurnPos = coordinate
                            break
                if endTurnPos:
                    break
            if not foundPos:
                endTurnPos = self.position
        self.move(endTurnPos)
    
    def eat(self, target) -> None:
        # Eat the food that is one square away from the prey
        if findDistance(self.position, target) > 1.5: # Ensure the food is close enough to eat
            self.goalList.insert(0, goal("move", self.currentTurn, self.position, math.ceil(findDistance(self.position, target) / self.speed), target))
            return
        else:
            plant = self.board.getEntity(target)
            try:
                self.energy += plant.energy
                if self.energy > 1:
                    self.energy = 1
                self.board.removeEntityFromLocation(target)
            except AttributeError:
                pass
            self.goalList.pop(0)


    def executeGoal(self) -> None:
        if self.goalList == []:
            return

        goal = self.goalList[0]
        if goal.type == "move":
            self.planMove(goal)
        elif goal.type == "eat":
            self.eat(goal.endPosition)        


class prey(animal):
    def __init__(self, id, position, board, speed, sensingRange, dayCost) -> None:
        super().__init__(id, position, board, speed, sensingRange, dayCost)
    
    def findNearestFoodSource(self):
        # Find the nearest food source and create a goal to reach it
        nearbyPlaces = findCircleInteriorPoints(self.position, self.sensingRange, self.board.getShape())
        smallestDistance = findDistance([0, 0], self.board.getShape())
        closestBoard = []
        for position in nearbyPlaces:
            if type(self.board.getEntity(position)) == foodSource:
                if findDistance(self.position, position) < smallestDistance:
                    closestBoard = position
                    smallestDistance = findDistance(self.position, position)
        if closestBoard != []:
            self.goalList.append(goal("move", self.currentTurn, self.position, math.ceil(smallestDistance / self.speed), closestBoard))
            self.goalList.append(goal("eat", math.ceil(smallestDistance / self.speed), closestBoard, math.ceil(smallestDistance / self.speed) + 1, closestBoard))

class predator(animal):
    def __init__(self, id, position, board, speed, sensingRange, dayCost) -> None:
        super().__init__(id, position, board, speed, sensingRange, dayCost)

class board:
    def __init__(self, xSize, ySize) -> None:
        self.board = np.empty([xSize, ySize], entity)
        self.count = 0
    
    # Getters
    def getEmptyPlaces(self) -> list:
        # Get a list of all the places on the board with nothing on them
        empties = []
        for rowIndex, row in enumerate(self.board):
            for itemIndex, item in enumerate(row):
                if item == None:
                    empties.append([rowIndex, itemIndex])
        return empties

    def getEntity(self, searchPosition):
        return self.board[searchPosition[0]][searchPosition[1]]
    
    def getShape(self) -> list:
        return list([self.board.shape[0] - 1, self.board.shape[1] - 1])
    # Setters
    def setEntity(self, entity, location) -> None:
        # Set an entity to a specific location on the board
        if self.board[location[0]][location[1]] != None:
            raise Exception(f"\nSET ENTITY ERROR\nThere is already an entity at location {location}\nThis occured when you were setting entity {entity.id}")
        else:
            self.board[location[0]][location[1]] = entity

    def removeEntityFromLocation(self, location) -> None:
        # Remove an entity from a location on the board
        if self.board[location[0]][location[1]] == None:
            pass
            # print(f"\nREMOVE ENTITY ERROR\nAttempting to delete entity at location {location}. Nothing is at that location")
        else:
            self.board[location[0]][location[1]] = None

    # Modifiers
    def moveEntity(self, entity, oldLocation, newLocation) -> None:
        # Move a board from location to another
        if self.board[oldLocation[0]][oldLocation[1]] == None:
            pass
            # print(f"\nMOVE ENTITY ERROR\nThere is no entity at old location {oldLocation}\n This occured whilst trying to move entity {entity.id}")
        else:
            self.removeEntityFromLocation(oldLocation)
            self.setEntity(entity, newLocation)

    def plotBoard(self, showPlot, outputPath) -> None:
        # Plots the location of all entities on the board on a graph

        # Create legend
        entityTypeLegend = [
            mpatches.Patch(color="#c7502c", label="Entity"),
            mpatches.Patch(color="#48cf6c", label="Food"),
            mpatches.Patch(color="#4489cf", label="Prey"),
            mpatches.Patch(color="#d4243e", label="Predator"),
        ]
        for row in self.board:
            for item in row:
                if item != None:
                    color = "#c7502c"
                    if type(item) == prey:
                        color = "#4489cf"
                    if type(item) == foodSource:
                        color = "#48cf6c"
                    if type(item) == predator:
                        color = "#d4243e"
                    plt.scatter(item.position[0], item.position[1], color=color)

        plt.xlim(0, self.board.shape[0])
        plt.ylim(0, self.board.shape[1])
        plt.title("Board status")
        plt.legend(handles=entityTypeLegend)
        if showPlot:
            plt.show()
        else:
            plt.savefig(outputPath)
            plt.close()

class goal:
    # A goal is something an animal is currently trying to achieve (can span across multiple turns)
    def __init__(self, goalType,  startTime, startLocation, endTime, endLocation) -> None:
        self.type = goalType
        self.startTime = startTime
        self.startPosition = startLocation
        self.endTime = endTime
        self.endPosition = endLocation
