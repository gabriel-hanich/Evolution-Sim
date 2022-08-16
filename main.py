import numpy as np
import src.models as entities
import matplotlib.pyplot as plt
import json 

with open("./settup.json", "r", encoding="utf-8") as setupFile:
    setup = json.load(setupFile)

board = np.empty([setup["board"]["boardSizeX"], setup["board"]["boardSizeY"]], entities.entity)

rabbit = entities.prey([0, 0], 1, 1, 1, 1, 1, 1, 1)

rabbit.updateBoard(board)