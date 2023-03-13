import random
import numpy as np
from src.entities.entity import Entity

class Board():
    def __init__(self, sizeX, sizeY) -> None:
        self.boardArray = np.empty((sizeX, sizeY), Entity)

    def findRandomBlank(self)->list:
        blankSpaces = np.argwhere(self.boardArray == None)
        return blankSpaces[random.randint(0, len(blankSpaces) - 1)]

    def placeEntity(self, entity, xVal, yVal):
        if(self.boardArray[xVal][yVal] != None):
            raise Exception(f"placementERROR\nYou are trying to place entity: {entity.id} at location {xVal}, {yVal}. This spot is occupied")
        else:
            self.boardArray[xVal][yVal] = entity

    def clearLocation(self, xVal, yVal):
        if(self.boardArray[xVal][yVal] == None):
            raise Exception(f"clearERROR\nYou are trying to clear {xVal}, {yVal}. There is nothing there already")
        else:
            self.boardArray[xVal][yVal] = None

    def getShape(self) -> tuple:
        return self.boardArray.shape
    
    def getEntity(self, xVal, yVal):
        return self.boardArray[xVal][yVal]