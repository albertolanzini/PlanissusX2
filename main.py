from Grid import *
from Vegetob import Vegetob
from Constants import *
from gridVisualization import *
from Animals import *
from dailyOperations import *


def daily_actions(grid):
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

    populate_grid(Erbast, 10, grid1)
    populate_grid(Carviz, 10, grid1)
    
    groupAnimalsStart(grid1)

    visualizer = GridVisualizer(grid1)

    visualizer.visualize()


if __name__ == '__main__':
    main()
