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

                # Preliminary step to make sure all herds can possibly move
                for herd in cell.herds:
                    herd.moved = False

                for pride in cell.prides:
                    pride.moved = False

    # 2 step - Movement (only herd for now)
    
    for row in grid:
        for cell in row:

            if cell.type == 'ground':

                for herd in list(cell.herds):
                    herd.move()
                    

    # 3 step - Grazing

    for row in grid:
        for cell in row:
            if cell.type == 'ground':
                for herd in cell.herds:
                    if not herd.moved:
                        herd.graze()

    # 4 step - 
    
    for row in grid:
        for cell in row:
            pass

    # 5 step - Aging and (eventually) energy expenditure and spawning

    for row in grid:
        for cell in row:
            if cell.type == 'ground':
                for herd in cell.herds:
                    herd.age_group()
                for pride in cell.prides:
                    pride.age_group()
                

def main():
    grid1 = create_grid(numCellsX, numCellsY)

    populate_grid(Erbast, 4, grid1)
    populate_grid(Carviz, 12, grid1)
    
    groupAnimalsStart(grid1)

    visualizer = GridVisualizer(grid1)

    visualizer.visualize()


if __name__ == '__main__':
    main()
