from pyexpat import model
import string
from tkinter import N
from tkinter.messagebox import NO
import src.models as entities
from src.mathFuncs import *
import random
import time
import json


def spawnFood(count, setup, board) -> None:
    for i in range(count):
        locations = board.getEmptyPlaces()
        loc = locations[random.randint(0, len(locations) - 1)]
        food = entities.foodSource(f"foodSource{i}",
            loc,
            board,
            round(findNormal(setup["food"]["meanEnergy"], setup["food"]["energyVariation"])))
        board.setEntity(food, loc)


startTime = time.time()
print(f"Initialising sim to run")

with open("./setup.json", "r", encoding="utf-8") as setupFile:
    setup = json.load(setupFile)

board = entities.board(setup["board"]["boardSizeX"], setup["board"]["boardSizeY"])


spawnFood(setup["food"]["foodCount"], setup, board)

preyList = []
for i in range(setup["prey"]["preyCount"]):
    locations = board.getEmptyPlaces()
    loc = locations[random.randint(0, len(locations) - 1)]
    prey = entities.prey(
        f"prey{i+1}", 
        loc,
        board,
        round(findNormal(setup["prey"]["meanSpeed"], setup["prey"]["speedVariation"]), 4),
        round(findNormal(setup["prey"]["meanSensingRange"], setup["prey"]["sensingRangeVariation"]), 4),
        setup["prey"]["dayCost"]
    )
    board.setEntity(prey, loc)
    preyList.append(prey)


turnIcons = ["|", "/", "-", "\\"]
# Output data to be saved as .csv 
outputData = np.empty([setup["sim"]["length"] + 1, 5]) 
# outputData[0] = ["Turn Number", "Number of prey", "Average prey energy"]

for turnNumber in range(setup["sim"]["length"]):
    # Actuate the prey
    for preyIndex, prey in enumerate(preyList):
        if not prey.updateVitals():
            preyList.pop(preyIndex)
        else:
            if prey.goalList == []:
                prey.findNearestFoodSource()
            prey.executeGoal()

    # Measure how much food there is on the board
    foodCount = 0
    for row in range(board.getShape()[0]):
        for column in range(board.getShape()[1]):
            if type(board.getEntity([row, column])) == entities.foodSource:
                foodCount += 1

    # Spawn new food if there isn't enoughu
    if foodCount < setup["food"]["foodCount"] * setup["food"]["spawnThreshold"]:
        spawnFood(round(setup["food"]["foodCount"] * (1 - setup["food"]["spawnThreshold"])), setup, board)

    # Breed the prey every n turns
    breedCount = 0
    if (turnNumber + 1) % setup["sim"]["breedTurns"] == 0: 
        currentPreyList = preyList.copy()
        for preyIndex, prey in enumerate(currentPreyList):
            if prey.energy >= setup["prey"]["breedThreshold"]: # If the animal has over 0.5 energy
                breedCount += 1
                positions = board.getEmptyPlaces()
                pos = positions[random.randint(0, len(positions) - 1)]
                speed = round(findNormal(prey.speed, setup["prey"]["speedVariation"]), 4)
                sensingRange = round(findNormal(prey.sensingRange, setup["prey"]["sensingRangeVariation"]), 4)
                if speed < 1:
                    speed = 1
                if sensingRange < 1:
                    sensingRange = 1
                newPrey = entities.prey(
                    f"prey{setup['prey']['preyCount'] + preyIndex}",
                    pos,
                    board,
                    speed,
                    sensingRange,
                    setup["prey"]["dayCost"]
                )    
                preyList.append(newPrey)
                board.setEntity(newPrey, pos)
    
    # Record the tracked value
    totalPreySpeed = 0
    totalPreySense = 0
    for prey in preyList:
        totalPreySpeed += prey.speed
        totalPreySense += prey.sensingRange
    
    # Check to see if the board is too 'full'
    freeLoc = len(board.getEmptyPlaces())
    totalLoc = (board.getShape()[0] + 1) * (board.getShape()[1] + 1)
    if (totalLoc - freeLoc) / totalLoc > setup["board"]["fullThreshold"]:
        print(f"\nBoard has reached level deemed 'full' at turn {turnNumber}")
        break

    # board.plotBoard(False, f"./output/{turnNumber}.png")
    outputData[turnNumber][0] = turnNumber
    outputData[turnNumber][1] = len(preyList)
    outputData[turnNumber][4] = breedCount
    if len(preyList) == 0:
        print(f"\nThere are no more prey left at turn {turnNumber}")
        outputData[turnNumber][3] = 0
        outputData[turnNumber][2] = 0
        break
    else:
        outputData[turnNumber][3] = totalPreySense / len(preyList)
        outputData[turnNumber][2] = totalPreySpeed / len(preyList)

    print(f"\r{turnIcons[turnNumber % len(turnIcons)]} Loading {round((turnNumber + 1) / setup['sim']['length'], 3) * 100}% - Population - {len(preyList)}  ", end="") # Print loading info
np.savetxt("./output/dataOut.csv", outputData, delimiter=",")
print(f"\nDone! generated {turnNumber + 1} days in {round((time.time() - startTime), 3)} seconds")