import numpy as np
import matplotlib.pyplot
import models as entities

def plotBoard(board):
    for row in board:
        for item in row:
            if item != None:
                color = "#48cf6c"
                if type(item) == entities.prey:
                    color = "#4489cf"
                plt.scatter()
                print(type(item))

if __name__ == "__main__":
    board = np.empty([100, 100], entities.entity)
    rabbit = entities.prey([10, 10], 1, 1, 1, 1, 1, 1, 1)
    board[10, 10] = rabbit
    plotBoard(board)