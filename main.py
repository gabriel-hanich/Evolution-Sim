import src.models as entities
from src.mathFuncs import *
import random
import json

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


turnIcons = ["|", "/", "|", "\\"]
priorLoadingStr = ""

for turnNumber in range(setup["sim"]["length"]):
    for prey in preyList:
        prey.updateVitals()
        if prey.currentGoal == None:
            prey.findNearestFoodSource()
        prey.executeGoal()
    board.plotBoard(False, f"./output/{turnNumber}.png")
    print(f"\r{turnIcons[turnNumber % len(turnIcons)]} Loading {round((turnNumber + 1) / setup['sim']['length'], 3) * 100}%", end="") # Print loading info