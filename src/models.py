from re import search
from turtle import distance
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
        self.currentTurn()

class foodSource(entity):
    def __init__(self, id, position, board, energy) -> None:
        super().__init__(id, position, board)
        self.energy = energy

class animal(entity):
    def __init__(self, id, position, board, speed, sensingRange) -> None:
        super().__init__(id, position, board)
        self.energy = 1,
        self.speed = speed
        self.sensingRange = sensingRange

        self.movementCost = round((math.log(self.speed + 1) / 15), 3) # How much energy it costs to move 1 square
        self.currentGoal = None

    def updateVitals(self):
        # Update the energy of the animal,
        # Called at the start of every turn
        self.energy -= (1 - self.efficiency)
        self.updateTurn()
    
    def move(self, newPosition):
        distance = findDistance(self.position, newPosition)
        if distance * self.movementCost >= self.energy:
            raise Exception(f"ANIMAL MOVEMENT ERROR\n{self.id} does not have enough energy to move {distance} blocks")
        else:
            self.board.moveEntity(self, self.position, newPosition)
            self.energy -= distance * self.movementCost
            self.position = newPosition


class prey(animal):
    def __init__(self, id, position, board, speed, sensingRange) -> None:
        super().__init__(id, position, board, speed, sensingRange)
    
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
            self.currentGoal = goal(self.currentTurn, self.position, math.ceil(smallestDistance / self.speed), closestBoard)


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

    def getEntity(self, searchPosition) -> None or entity:
        return self.board[searchPosition[0]][searchPosition[1]]
    
    def getShape(self) -> list:
        return list(self.board.shape)
    # Setters
    def setEntity(self, entity, location) -> None:
        # Set an entity to a specific location on the board
        if self.board[location[0]][location[1]] != None:
            raise Exception(f"SET ENTITY ERROR\nThere is already an entity at location {location}\nThis occured when you were setting entity {entity.id}")
        else:
            self.board[location[0]][location[1]] = entity

    def removeEntityFromLocation(self, location) -> None:
        # Remove an entity from a location on the board
        if self.board[location[0]][location[1]] == None:
            raise Exception(f"REMOVE ENTITY ERROR\nAttempting to delete entity at location {location}. Nothing is at that location")
        else:
            self.board[location[0]][location[1]] = None

    # Modifiers
    def moveEntity(self, entity, oldLocation, newLocation) -> None:
        # Move a board from location to another
        if self.board[oldLocation[0]][oldLocation[1]] == None:
            raise Exception(f"MOVE ENTITY ERROR\nThere is no entity at old location {oldLocation}\n This occured whilst trying to move entity {entity.id}")
        else:
            self.removeEntity(oldLocation)
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
    def __init__(self, startTime, startLocation, endTime, endLocation) -> None:
        self.startTime = startTime
        self.startLocation = startLocation
        self.endTime = endTime
        self.endLocation = endLocation
