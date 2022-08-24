import string
import src.models as entities
from src.mathFuncs import *
import random
import time
import json

startTime = time.time()
print(f"Initialising sim to run")

with open("./setup.json", "r", encoding="utf-8") as setupFile:
    setup = json.load(setupFile)

board = entities.board(setup["board"]["boardSizeX"], setup["board"]["boardSizeY"])

preyList = []
foodList = []
for i in range(setup["food"]["foodCount"]):
    locations = board.getEmptyPlaces()
    loc = locations[random.randint(0, len(locations) - 1)]
    food = entities.foodSource(f"foodSource{i}",
        loc,
        board,
        round(findNormal(setup["food"]["meanEnergy"], setup["food"]["energyVariation"])))
    board.setEntity(food, loc)
    foodList.append(food)

for i in range(setup["prey"]["preyCount"]):
    locations = board.getEmptyPlaces()
    loc = locations[random.randint(0, len(locations) - 1)]
    prey = entities.prey(f"prey{i+1}", 
        loc,
        board,
        round(findNormal(setup["prey"]["meanSpeed"], setup["prey"]["speedVariation"]), 4),
        round(findNormal(setup["prey"]["meanSensingRange"], setup["prey"]["sensingRangeVariation"]), 4)
    )
    board.setEntity(prey, loc)
    preyList.append(prey)


turnIcons = ["|", "/", "-", "\\"]
# Output data to be saved as .csv 
outputData = np.empty([setup["sim"]["length"] + 1, 3]) 
# outputData[0] = ["Turn Number", "Number of prey", "Average prey energy"]

for turnNumber in range(setup["sim"]["length"]):
    for preyIndex, prey in enumerate(preyList):
        if not prey.updateVitals():
            preyList.pop(preyIndex)
        else:
            if prey.goalList == []:
                prey.findNearestFoodSource()
            prey.executeGoal()
    
    trackVal = 0
    for prey in preyList:
        trackVal += prey.energy

    board.plotBoard(False, f"./output/{turnNumber}.png")
    outputData[turnNumber][0] = turnNumber
    outputData[turnNumber][1] = len(preyList)
    outputData[turnNumber][2] = trackVal / len(preyList)
    if len(preyList) == 0:
        outputData[1] = 0
        break

    print(f"\r{turnIcons[turnNumber % len(turnIcons)]} Loading {round((turnNumber + 1) / setup['sim']['length'], 3) * 100}%", end="") # Print loading info
np.savetxt("./output/dataOut.csv", outputData, delimiter=",")
print(outputData)
print(f"\nDone! generated {turnNumber + 1} days in {round((time.time() - startTime), 3)} seconds")