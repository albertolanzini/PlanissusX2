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


def print_prides_and_herds(grid):
    prides = {}
    herds = {}
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell.inhabitants:
                for animal in cell.inhabitants:
                    if isinstance(animal, Carviz):
                        if animal.pride is not None and animal.pride not in prides:
                            prides[animal.pride] = (i, j)
                    elif isinstance(animal, Erbast):
                        if animal.herd is not None and animal.herd not in herds:
                            herds[animal.herd] = (i, j)

    print("Prides:")
    for pride, location in prides.items():
        print(f"Pride ID: {pride.id}, Members: {len(pride.members)}, Cell: {location}")

    print("\nHerds:")
    for herd, location in herds.items():
        print(f"Herd ID: {herd.id}, Members: {len(herd.members)}, Cell: {location}")




