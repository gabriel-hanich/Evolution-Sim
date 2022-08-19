# Assorted math functions
import numpy as np
import math

def findDistance(startPoint, endPoint):
    # Find the distance between two points
    return math.sqrt((startPoint[0] - endPoint[0]) ** 2 + (startPoint[1] - endPoint[1]) ** 2)

def findNormal(mean, deviation):
    # Find a random value from a given normal distribution
    return np.random.normal(mean, deviation, 1)[0]

def findCircleInteriorPoints(centrePoint, radius, northEastBoardCoord):
    # Find all the points within a circle of a centrepoint
    # Where centre point is the centre of the circles, radius is the sensing range and 
    # northEastBoardCoord is the maximum X and Y coordinates
    radius = round(radius)
    coords = []
    for multiplier in [[-1, -1], [-1, 1], [1, -1], [1, 1]]: # Iterates through each of the 4 quadrants 
        for xOffset in range(radius + 1):
            for yOffset in range(radius + 1):
                currentPos = [centrePoint[0] + multiplier[0] * xOffset, centrePoint[1] + multiplier[1] * yOffset] # The current position being scanned
                distance = findDistance(centrePoint, currentPos)
                if distance <= radius: # If the location is within scanning distance
                    if currentPos[0] >= 0 and currentPos[1] >= 0 and currentPos[0] < northEastBoardCoord[0] and currentPos[1] < northEastBoardCoord[1]:
                        coords.append(currentPos)
    return coords



