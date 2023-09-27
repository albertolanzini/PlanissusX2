from Grid import *
from Vegetob import Vegetob
from Constants import *
from gridVisualization import *
from Animals import *
from dailyOperations import *


def daily_actions(grid):
    """
    This function performs the daily actions for each cell in the grid.
    It iterates over each cell in the grid and performs the following actions:
    - If the cell type is 'ground', it triggers the growth of Vegetob in the cell.
    - It ages all the herds and prides in the cell.
    - It then triggers the movement of herds in the cell.
    """
    for row in grid:
        for cell in row:
            
            if cell.type == 'ground':

                # 1 step - Vegetob growth
                cell.vegetob.growing()

                # 2 step - Aging
                for herd in list(cell.herds):
                    herd.age_group()
                    herd.moved = False

                for pride in list(cell.prides):
                    pride.age_group()
                    pride.moved = False
    
    for row in grid:
        for cell in row:

            if cell.type == 'ground':

                for herd in list(cell.herds):
                    herd.move()
                    herd.moved = True

def main():
    grid1 = create_grid(numCellsX, numCellsY)

    populate_grid(Erbast, 100, grid1)
    populate_grid(Carviz, 20, grid1)
    
    groupAnimalsStart(grid1)

    visualizer = GridVisualizer(grid1)

    visualizer.visualize()


if __name__ == '__main__':
    main()
