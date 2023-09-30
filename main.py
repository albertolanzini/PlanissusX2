from Grid import *
from Vegetob import Vegetob
from Constants import *
from gridVisualization import *
from Animals import *
from dailyOperations import *
from Struggle import *


def daily_actions(grid):
    """
    This function performs the daily actions for each cell in the grid.
    It iterates over each cell in the grid and performs the following actions:
    - If the cell type is 'ground', it triggers the growth of Vegetob in the cell.
    - It ages all the herds and prides in the cell.
    - It then triggers the movement of herds in the cell.
    """

    # 1 step - Growing

    for row in grid:
        for cell in row:
            
            if cell.type == 'ground':

                cell.vegetob.growing()

                # Preliminary step to make sure all herds can possibly move
                for herd in cell.herds:
                    herd.moved = False

                for pride in cell.prides:
                    pride.moved = False

    # 2 step - Movement
    
    for row in grid:
        for cell in row:

            if cell.type == 'ground':

                for herd in list(cell.herds):
                    herd.move()

    for row in grid:
        for cell in row:
            if cell.type == 'ground':
                
                for pride in list(cell.prides):
                    pride.move()
                    

    # 3 step - Grazing

    for row in grid:
        for cell in row:
            if cell.type == 'ground':
                for herd in cell.herds:
                    if not herd.moved:
                        herd.graze()

    # Preliminary step to remove all possible empty herds/prides leftover

    for row in grid:
        for cell in row:
            if cell.type == 'ground':

                for pride in list(cell.prides):
                    if not pride.members:
                        cell.prides.remove(pride)
    
    # 4.1 : Herd merging and prides fighting

    for row in grid:
        for cell in row:
            if cell.type == 'ground':
                
                # Merge the herds in the cell to make sure it is a single one
                merge_herds(cell)

                # The prides will join or fight until there is only one left in the cell
                evaluate_and_fight_prides(cell)
                

    # 4.2 : Hunt

    for row in grid:
        for cell in row:
            if cell.type == 'ground':
                
                for pride in list(cell.prides):
                    pride.hunt()

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

    populate_grid(Erbast, 100, grid1)
    populate_grid(Carviz, 100, grid1)
    
    groupAnimalsStart(grid1)

    visualizer = GridVisualizer(grid1)

    visualizer.visualize()


if __name__ == '__main__':
    main()