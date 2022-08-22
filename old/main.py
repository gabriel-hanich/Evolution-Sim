from msilib.schema import Error
import numpy as np
import src.models as entities
import src.boardManagement as boardState
from src.mathFuncs import *
import matplotlib.pyplot as plt
import random
import json 

with open("./settup.json", "r", encoding="utf-8") as setupFile:
    setup = json.load(setupFile)

board = np.empty([setup["board"]["boardSizeX"], setup["board"]["boardSizeY"]], entities.entity)

# Distribute food
foodList = []
for i in range(setup["food"]["foodCount"]):
    freeLocations = boardState.findBlankSpaces(board)
    if len(freeLocations) == 0:
        raise Exception(f"BOARD FULL ERROR\nAll the spots on the board are full already. Space ran out on foodSource{i}")
    loc = freeLocations[random.randint(0, len(freeLocations) - 1)]
    foodSource = entities.foodSource(
        f"foodSource{i}", 
        loc, 
        np.random.normal(setup["food"]["meanEnergy"], setup["food"]["energyVariation"], 1)[0]
    )
    foodList.append(foodSource)
    board[loc[0]][loc[1]] = foodSource

# Distribute prey
preyList = []
for i in range(setup["prey"]["preyCount"]):
    # Find a random empty location on the board to spawn the prey
    freeLocations = boardState.findBlankSpaces(board)
    if len(freeLocations) == 0:
        raise Exception(f"BOARD FULL ERROR\nAll the spots on the board are full already. Space ran out on prey{i}")
    loc = freeLocations[random.randint(0, len(freeLocations) - 1)]
    prey = entities.prey(
        f"prey{i}",
        loc,
        findNormal(setup["prey"]["meanMaxHealth"], setup["prey"]["maxHealthVariation"]),
        findNormal(setup["prey"]["meanSpeed"], setup["prey"]["speedVariation"]),
        findNormal(setup["prey"]["meanMaxEnergy"], setup["prey"]["maxEnergyVariation"]),
        round(findNormal(setup["prey"]["meanSensingRange"], setup["prey"]["sensingRangeVariation"])),
    )
    board[loc[0]][loc[1]] = prey

    preyList.append(prey)

# Actually run the simulation
for turnCount in range(setup["sim"]["length"]):
    for preyIndex, prey in enumerate(preyList):
        # Update animal's board
        if not (prey.updateConstants(board, turnCount)):
            # If the animal is dead
            board = prey.getBoard()
            preyList.pop(preyIndex)
            x = 0
            for row in board:
                for item in row:
                    if type(item) == entities.prey:
                        x += 1
            next
        if turnCount == 0:
            # Decision making
            prey.findFood()
            board = prey.getBoard()

        # Goal Execution
        prey.executeGoal()
        board = prey.getBoard()

    boardState.plotBoard(board, False, f"./output/{turnCount}.png")
    print(f"{turnCount} - {len(preyList)} Prey in list and {x} on board")