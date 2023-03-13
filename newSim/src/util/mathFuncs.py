import numpy as np
import random
import matplotlib.pyplot as plt
from src.entities.entity import Entity

def findFromNormal(mean, deviation)->float:
    return np.random.normal(mean, deviation, 1)[0]

def findFromProbabilities(probabilitiesList)->float:
    probabilities = list(map(lambda prob: prob[1], probabilitiesList))
    if(round(sum(probabilities), 3) != 1):
        raise Exception(f"probabilitiesERROR\nThe sum of the provided probabilities is not equal to 1. The sum is {sum(probabilities)}")

    randVal = random.random()
    priorVal = 0
    for valPair in probabilitiesList:
        if(randVal >= priorVal) and (randVal < priorVal + valPair[1]):
            return valPair
        else:
            priorVal += valPair[1]

def findCirclePoints(pos, radius, maxX, maxY):
    points = []
    for multiplier in [[-1, -1], [-1, 1], [1, -1], [1, 1]]: # Iterate through each of the 4 quadrants (SW, NW, NE, NW)
        for xOffset in range(radius+1):
            for yOffset in range(radius+1):
                point = [pos[0] + (xOffset * multiplier[0]), pos[1] + (yOffset * multiplier[1])]
                if(calculateDistance(pos, point) <= radius) and (point[0] <= maxX) and (point[1] <= maxY):
                    if(point[0] >= 0) and (point[1] >= 0):
                        points.append(point)
    return points

def calculateDistance(pointA, pointB) -> float:
    return ((pointA[0] - pointB[0])** 2 + (pointA[1] - pointB[1])** 2) ** 0.5
