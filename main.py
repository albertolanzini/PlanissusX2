from Grid import *
from Vegetob import Vegetob
from Constants import *
from gridVisualization import *
from Animals import *


def main():
    grid1 = create_grid(numCellsX, numCellsY)
    populate_grid(Erbast, 10, grid1)
    populate_grid(Carviz, 10, grid1)

    visualizer = GridVisualizer(grid1)

    visualizer.visualize()


if __name__ == '__main__':
    main()
