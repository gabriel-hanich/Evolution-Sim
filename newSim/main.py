import time
from src.util.generators import generateAnimal, generateBoard, generateFood
from src.util.files import readJSON
from src.util.render import renderBoard
from src.util.mathFuncs import findCirclePoints


def generate(generalData, preyData, predatorData, foodData):
    board = generateBoard(kGeneralData)
    preyList, predatorList, foodList = [], [], []
    for i in range(generalData["general"]["preyCount"]):
        preyList.append(generateAnimal("prey", preyData, f"P{'0' * (5 - len(str(i+1)))}{i+1}", board))
    for k in range(generalData["general"]["predatorCount"]):
        preyList.append(generateAnimal("predator", predatorData, f"C{'0' * (5 - len(str(k+1)))}{k+1}", board))
    for j in range(generalData["general"]["startingFoodCount"]):
        foodList.append(generateFood(foodData, f"F{'0' * (5 - len(str(j+1)))}{j+1}", board))
    return board, preyList, predatorList, foodList

def runPeriod(periodNumber, generalData, foodData, board, preyList, predatorList, foodList)-> None:
    # Run the simulation for one day
    for i in range(generalData["general"]["foodReplenish"]):
        foodList.append(generateFood(foodData, f"F{'0' * (5 - len(str(i+1+len(foodList))))}{i+1+len(foodList)}", board))
    
    for prey in preyList:
        if(prey.isAlive):
            prey.makeMove()
    for predator in predatorList:
        if(predator.isAlive):
            predator.makeMove()


    return

def render(board, outputPath, graphData, display=False, save=True):
    renderBoard(board, outputPath, graphData, display, save)
    return

if __name__ == "__main__":
    startTime = time.time()
    kGeneralData = readJSON("./data/general.json")
    kPreyData = readJSON("./data/prey.json")
    kPredatorData = readJSON("./data/predator.json")
    kFoodData = readJSON("./data/food.json")

    board, preyList, predatorList, foodList = generate(kGeneralData, kPreyData, kPredatorData, kFoodData)
    print(f"Generated Data in {round(time.time() - startTime, 3)}s")
    for period in range(kGeneralData["general"]["periods"]):
        print(f'\rLoading Period {period+1}/{kGeneralData["general"]["periods"]}', end="")
        runPeriod((period+1), kGeneralData, kFoodData, board, preyList, predatorList, foodList)
        # render(board, f"./output/imgs/{period + 1}.png", kGeneralData)
    print(f"\nCode succesfully executed in {round(time.time() - startTime, 3)}s")