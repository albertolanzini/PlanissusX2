import numpy as np
import random

from Vegetob import Vegetob
from Animals import Erbast, Carviz
from Constants import *
from utils import get_neighboring_cells


class Cells:
    def __init__(self, type, vegetob=None, grid=None):
        self.type = type
        self.vegetob = vegetob
        self.inhabitants = set()
        self.position = None
        self.herds = []
        self.prides = []
        self.grid = grid

    def __repr__(self):
        if self.vegetob is not None:
            vegetob_density = self.vegetob.get_density()
        else:
            vegetob_density = 0
        return f"Cell(type={self.type}, vegetob_density={vegetob_density}, inhabitants={len(self.inhabitants)}, position={self.position})"

    def count_carviz(self):
        return sum(1 for animal in self.inhabitants if isinstance(animal, Carviz))
    
    def count_erbast(self):
        return sum(1 for animal in self.inhabitants if isinstance(animal, Erbast))
        
    def get_vegetob_amount(self):
        return self.vegetob.get_density() if self.vegetob else 0
    
    def spread_poison(self):
        if self.vegetob and self.vegetob.poisonous:
            neighboring_cells = get_neighboring_cells(self.grid, self, radius=1)
            new_poison_cell = random.choice(neighboring_cells)
            if random.random() < 0.03:
                if random.random() < 0.14:
                    # print(f"Cell at position {new_poison_cell.position} has been infected by cell {self.position}")
                    new_poison_cell.vegetob.poisonous = True

def create_grid(numcellsx, numcellsy):
    # Initialize an empty numpy array with the specified dimensions
    grid = np.empty((numcellsx, numcellsy), dtype=object)

    for i in range(numcellsx):
        for j in range(numcellsy):
            if i == 0 or j == 0 or i == numcellsx-1 or j == numcellsy-1:
                # It's an outer cell, make it water
                grid[i][j] = Cells('water')
                grid[i][j].position = (i, j)
            else:
                # It's an inner cell, 20% chance of water, otherwise ground with Vegetob
                if np.random.random() < 0.2:
                    grid[i][j] = Cells('water')
                    grid[i][j].position = (i, j)
                else:
                    vegetob_density = random.randint(60, 80)
                    vegetob = Vegetob(vegetob_density)
                    # The vegetob will be poisonous, but only 1% of the time
                    vegetob.poisonous = np.random.random() < 0.01
                    grid[i][j] = Cells('ground', vegetob, grid=grid)
                    grid[i][j].position = (i, j)

    return grid


def populate_grid(animal_class, n, grid):
    for _ in range(n):
        while True:
            i = random.randint(0, len(grid) - 1)
            j = random.randint(0, len(grid[0]) - 1)

            if grid[i][j].type == 'ground' and sum(isinstance(animal, animal_class) for animal in grid[i][j].inhabitants) < MAX_SIZE:
                energy = random.randint(50, 80)
                lifetime = random.randint(50, 100)

                social_attitude = random.random()

                animal = animal_class(energy, lifetime, social_attitude, grid[i][j])
                grid[i][j].inhabitants.add(animal)
                break

