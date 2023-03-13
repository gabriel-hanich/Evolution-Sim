from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from src.entities.food import Food
from src.entities.predator import Predator
from src.entities.prey import Prey


def renderBoard(board, outputPath, graphData, display=False, save=True):
    entityTypeLegend = [
            mpatches.Patch(color=graphData["graph"]["foodColor"], label="Food"),
            mpatches.Patch(color=graphData["graph"]["preyColor"], label="Prey"),
            mpatches.Patch(color=graphData["graph"]["predatorColor"], label="Predator"),
        ]
    shape = board.getShape()
    for x in range(shape[0]):
        for y in range(shape[1]):
            entity = board.getEntity(x, y)
            if(entity != None):
                color = "#000000"
                if(type(entity) == Prey):
                    color = graphData["graph"]["preyColor"]
                if(type(entity) == Predator):
                    color = graphData["graph"]["predatorColor"]
                if(type(entity) == Food):
                    color = graphData["graph"]["foodColor"]
                plt.scatter(x, y, color=color)
    plt.xlim(0, shape[0] * 1.05)
    plt.ylim(0, shape[1] * 1.05)
    plt.title("Board status")
    plt.legend(handles=entityTypeLegend, bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    if(display):
        plt.show()
    if(save):
        plt.savefig(outputPath, bbox_inches='tight', dpi=300)