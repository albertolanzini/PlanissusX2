from Grid import *
from Vegetob import Vegetob
from Constants import *
from gridVisualization import *
from Animals import *
from dailyOperations import *
from Struggle import *
from GUI import *
from utils import count_ground_cells

def create_gui(visualizer):
    app = wx.App(False)
    frame = MainFrame(visualizer)
    frame.Show()
    app.MainLoop()

def daily_actions(grid):
    """
    This function performs the daily actions for each cell in the grid.
    It iterates over each cell in the grid and performs the following actions:
    - If the cell type is 'ground', it triggers the growth of Vegetob in the cell and the spreading of the poisonous vegetob.
    - It then triggers the movement of herds in the cell.
    - It then triggers the grazing of the non-moving herds.
    - It then triggers the merging of the herds and the merging/fighting of the prides.
    - It then triggers the hunt.
    - Finally, it ages all the herds and prides in the cell.
    """

    # 1 step - Growing

    for row in grid:
        for cell in row:
            
            if cell.type == 'ground':

                cell.vegetob.growing()
                
                cell.spread_poison()

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

    for row in grid:
        for cell in row:
            if cell.type == 'ground':
                for animal in list(cell.inhabitants):
                    if animal.dead:
                        cell.inhabitants.remove(animal)

def main():
    # Grid creations
    grid1 = create_grid(numCellsX, numCellsY)

    # Count the ground cells and calculate the max number of Carviz and Erbast to make sure
    # the world does not exceed its limits. This step is necessary to ensure better performance.
    ground_cells = count_ground_cells(grid1)

    nCarvizes = min(nCarviz, ground_cells*MAX_SIZE)
    nErbasts = min(nErbast, ground_cells*MAX_SIZE)

    populate_grid(Erbast, nErbasts, grid1)
    populate_grid(Carviz, nCarvizes, grid1)
    
    groupAnimalsStart(grid1)

    visualizer = GridVisualizer(grid1)
    pub.sendMessage("get.visualizer", visualizer=visualizer)

    create_gui(visualizer)


if __name__ == '__main__':
    main()