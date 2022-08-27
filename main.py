import src.models as entities
from src.mathFuncs import *
import matplotlib.pyplot as plt
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

predatorList = []
for i in range(setup["predator"]["predatorCount"]):
    locations = board.getEmptyPlaces()
    loc = locations[random.randint(0, len(locations) - 1)]
    predator = entities.predator(
        f"predator{i}", 
        loc, 
        board,
        round(findNormal(setup["predator"]["meanSpeed"], setup["predator"]["speedVariation"]), 4),
        round(findNormal(setup["predator"]["meanSensingRange"], setup["predator"]["sensingRangeVariation"]), 4),
        setup["predator"]["dayCost"]
        )
    predatorList.append(predator)
    board.setEntity(predator, loc)

turnIcons = ["|", "/", "-", "\\"]

# Output data to be saved as .csv 
preyOutputData = np.empty([setup["sim"]["length"], 5]) 
predatorOutputData = np.empty([setup["sim"]["length"], 5]) 

extinctionAlert = False # If the extinction alert has been printed about predators

for turnNumber in range(setup["sim"]["length"]):
    # Actuate the prey
    for preyIndex, prey in enumerate(preyList):
        if not prey.updateVitals():
            preyList.pop(preyIndex)
        else:
            if prey.goalList == []:
                prey.findNearestFoodSource()
            prey.executeGoal()

    # Actuate predators
    for predatorIndex, predator in enumerate(predatorList):
        if not predator.updateVitals():
            predatorList.pop(predatorIndex)
        else:
            if predator.goalList == []:
                predator.findNearestFoodSource()
            preyResults = predator.executeGoal()
            if preyResults["success"] == True and preyResults["goalType"] == "eatprey": # If the predator succesfully ate a prey
                for preyIndex, prey in enumerate(preyList):
                    if prey == preyResults["other"]: # Remove the eaten prey from the list
                        preyList.pop(preyIndex)
                        break

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
    preyBreedCount = 0
    predatorBreedCount = 0

    if (turnNumber + 1) % setup["sim"]["breedTurns"] == 0: 
        # Breed Prey
        currentPreyList = preyList.copy()
        for preyIndex, prey in enumerate(currentPreyList):
            if prey.energy >= setup["prey"]["breedThreshold"]: # If the animal has enough energy to breed
                preyBreedCount += 1
                positions = board.getEmptyPlaces()
                pos = positions[random.randint(0, len(positions) - 1)]
                newPrey = entities.prey(
                    f"prey{setup['prey']['preyCount'] + preyIndex}",
                    pos,
                    board,
                    round(findNormal(prey.speed, setup["prey"]["speedVariation"]), 4),
                    round(findNormal(prey.sensingRange, setup["prey"]["sensingRangeVariation"]), 4),
                    setup["prey"]["dayCost"]
                )    
                preyList.append(newPrey)
                board.setEntity(newPrey, pos)
    
        # Breed Predators
        currentPredatorList = predatorList.copy()
        for predatorIndex, predator in enumerate(currentPredatorList):
            if predator.energy >= setup["predator"]["breedThreshold"]:
                predatorBreedCount += 1
                locations = board.getEmptyPlaces()
                loc = locations[random.randint(0, len(locations) - 1)]
                newPredator = entities.predator(
                    f"predator{setup['predator']['predatorCount'] + predatorIndex}",
                    loc,
                    board,
                    round(findNormal(predator.speed, setup["predator"]["speedVariation"]), 4),
                    round(findNormal(predator.sensingRange, setup["predator"]["sensingRangeVariation"]), 4),
                    setup["predator"]["dayCost"]
                    )

    # Check to see if the board is too 'full'
    freeLoc = len(board.getEmptyPlaces())
    totalLoc = (board.getShape()[0] + 1) * (board.getShape()[1] + 1)
    if (totalLoc - freeLoc) / totalLoc > setup["board"]["fullThreshold"]:
        print(f"\nBoard has reached level deemed 'full' at turn {turnNumber}")
        break

    # Change setup values if configured to do so
    if setup["valChange"]["doChange"]:
        if (turnNumber + 1) % setup["valChange"]["changeTurns"] == 0:
            setup[setup["valChange"]["keyCategory"]][setup["valChange"]["key"]] += setup["valChange"]["changeAmount"]

    # Record the tracked values
    totalPreySpeed = 0
    totalPreySense = 0
    for prey in preyList:
        totalPreySpeed += prey.speed
        totalPreySense += prey.sensingRange
    
    totalPredatorSpeed = 0
    totalPredatorSense = 0
    for predator in predatorList:
        totalPredatorSpeed += predator.speed
        totalPredatorSense += predator.sensingRange

    # Record data 
    preyOutputData[turnNumber][0] = turnNumber
    preyOutputData[turnNumber][1] = len(preyList)
    preyOutputData[turnNumber][4] = preyBreedCount

    predatorOutputData[turnNumber][0] = turnNumber
    predatorOutputData[turnNumber][1] = len(predatorList)
    predatorOutputData[turnNumber][4] = predatorBreedCount

    if len(preyList) == 0:
        print(f"\nThere are no more prey left at turn {turnNumber}")
        preyOutputData[turnNumber][3] = 0
        preyOutputData[turnNumber][2] = 0
        break
    else:
        preyOutputData[turnNumber][2] = totalPreySpeed / len(preyList)
        preyOutputData[turnNumber][3] = totalPreySense / len(preyList)

    if len(predatorList) == 0:
        if not extinctionAlert:
            print(f"\nPredators extinct at turn {turnNumber}")
            extinctionAlert = True
        predatorOutputData[turnNumber][3] = 0
        predatorOutputData[turnNumber][2] = 0
    else:
        predatorOutputData[turnNumber][2] = totalPredatorSpeed / len(predatorList)
        predatorOutputData[turnNumber][3] = totalPredatorSense / len(predatorList)

    print(f"\r{turnIcons[turnNumber % len(turnIcons)]} Loading {round(((turnNumber + 1) / setup['sim']['length']) * 100, 3) }% - Population - {len(preyList)}  ", end="") # Print loading info
np.savetxt("./output/preyData.csv", preyOutputData, delimiter=",")
np.savetxt("./output/predatorData.csv", predatorOutputData, delimiter=",")
print(f"\nDone! generated {turnNumber + 1} days in {round((time.time() - startTime), 3)} seconds")

# Plot stuff
plt.plot(predatorOutputData[:, 2], label="Speed")
plt.plot(predatorOutputData[:, 3], label="Sense")
plt.legend()
plt.show()