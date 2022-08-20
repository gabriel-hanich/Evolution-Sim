import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

class entity:
    def __init__(self, id, position, board) -> None:
        self.id = id
        self.position = position
        self.board = board

class foodSource(entity):
    def __init__(self, id, position, board, energy) -> None:
        super().__init__(id, position, board)
        self.energy = energy

class animal(entity):
    def __init__(self, id, position, board, speed, sensingRange) -> None:
        super().__init__(id, position, board)
        self.health = 1,
        self.energy = 1,
        self.speed = speed
        self.sensingRange = sensingRange


class prey(animal):
    def __init__(self, id, position, board, speed, sensingRange) -> None:
        super().__init__(id, position, board, speed, sensingRange)

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

    def plotBoard(self, showPlot, outputPath):
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

    # Setters
    def setEntity(self, entity, location) -> None:
        # Set an entity to a specific location on the board
        if self.board[location[0]][location[1]] != None:
            raise Exception(f"SET ENTITY ERROR\nThere is already an entity at location {location}\nThis occured when you were setting entity {entity.id}")
        else:
            self.board[location[0]][location[1]] = entity

    # Modifiers

