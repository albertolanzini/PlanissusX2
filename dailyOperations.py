from Animals import *
from Groups import *
from Grid import *


def groupAnimalsStart(grid):
    """This function groups the animals in herds and prides at the start of the simulation.
        Note that it is not meant to handle herds/prides in the same cell once the herds and prides are already present,
         it is just intended as a function to be used only at the start of the simulation."""

    for row in grid:
        for cell in row:
           
            erbast_in_cell = [animal for animal in cell.inhabitants if isinstance(animal, Erbast)]
            carviz_in_cell = [animal for animal in cell.inhabitants if isinstance(animal, Carviz)]

            if erbast_in_cell:
                herd = Herd()
                for erbast in erbast_in_cell:
                    erbast.join_group(herd)

            if carviz_in_cell:
                pride = Pride()
                for carviz in carviz_in_cell:
                    carviz.join_group(pride)





