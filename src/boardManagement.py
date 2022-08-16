import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import src.models as entities

def plotBoard(board):
    # Plots the location of all entities on the board on a graph

    # Create legend
    entityTypeLegend = [
        mpatches.Patch(color="#c7502c", label="Entity"),
        mpatches.Patch(color="#48cf6c", label="Food"),
        mpatches.Patch(color="#4489cf", label="Prey"),
        mpatches.Patch(color="#d4243e", label="Predator"),
    ]

    for row in board:
        for item in row:
            if item != None:
                color = "#48cf6c"
                if type(item) == entities.prey:
                    color = "#4489cf"
                plt.scatter(item.position[0], item.position[1], color=color)

    plt.xlim(0, board.shape[0])
    plt.ylim(0, board.shape[0])
    plt.title("Board status")
    plt.legend(handles=entityTypeLegend)
    plt.show()

def findBlankSpaces(board):
    # Returns a list of any squares that are empty
    emptyCoords = []
    for rowIndex, row in enumerate(board):
        for itemIndex, item in enumerate(row):
            if item == None:
                emptyCoords.append([rowIndex, itemIndex])
    return emptyCoords

if __name__ == "__main__":
    board = np.empty([100, 100], entities.entity)
    print(findBlankSpaces(board))