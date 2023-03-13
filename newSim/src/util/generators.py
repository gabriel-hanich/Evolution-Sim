from src.entities.food import Food
from src.entities.entity import Entity
from src.entities.board import Board
from src.entities.predator import Predator
from src.entities.prey import Prey
from src.util.mathFuncs import findFromNormal


def generateBoard(data):
    return Board(data["board"]["boardX"], data["board"]["boardY"])

def generateAnimal(animalType, consts, id, board)->Entity:
    efficency = findFromNormal(consts["efficiency"]["mean"], consts["efficiency"]["deviance"])
    senseRange = findFromNormal(consts["senseRange"]["mean"], consts["senseRange"]["deviance"])
    moveRange = findFromNormal(consts["moveRange"]["mean"], consts["moveRange"]["deviance"])
    position = board.findRandomBlank()
    if(animalType == "predator"):
        return Predator(board, position, id, efficency, senseRange, moveRange)
    else:
        return Prey(board, position, id, efficency, senseRange, moveRange)

def generateFood(consts, id, board):
    energyValue = findFromNormal(consts["energyVal"]["mean"], consts["energyVal"]["deviance"])
    position = board.findRandomBlank()
    return Food(board, position, id, energyValue)