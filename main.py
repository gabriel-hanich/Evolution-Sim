import numpy as np
import src.models as entities
import src.boardManagement as boardState
import matplotlib.pyplot as plt
import random
import json 

with open("./settup.json", "r", encoding="utf-8") as setupFile:
    setup = json.load(setupFile)

board = np.empty([setup["board"]["boardSizeX"], setup["board"]["boardSizeY"]], entities.entity)

preyList = []
for i in range(setup["prey"]["preyCount"]):
    # Find a random empty location on the board to spawn the prey
    freeLocations = boardState.findBlankSpaces(board)
    loc = freeLocations[random.randint(0, len(freeLocations) - 1)]
    prey = entities.prey(
        f"prey{i}",
        loc,
        np.random.normal(setup["prey"]["meanMaxHealth"], setup["prey"]["maxHealthVariation"], 1)[0],
        np.random.normal(setup["prey"]["meanSpeed"], setup["prey"]["speedVariation"], 1)[0],
        np.random.normal(setup["prey"]["meanMaxEnergy"], setup["prey"]["maxEnergyVariation"], 1)[0],
        round(np.random.normal(setup["prey"]["meanSensingRange"], setup["prey"]["sensingRangeVariation"], 1)[0])
    )
    board[loc[0]][loc[1]] = prey

    preyList.append(prey)

for prey in preyList:
    prey.updateBoard(board)

boardState.plotBoard(board)