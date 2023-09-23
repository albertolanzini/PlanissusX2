import numpy as np
import random
from Vegetob import Vegetob
from Animals import Erbast, Carviz


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
                    vegetob_density = random.randint(20, 80)
                    grid[i][j] = Cells('ground', Vegetob(vegetob_density), grid=grid)
                    grid[i][j].position = (i, j)

    return grid


def populate_grid(animal_class, n, grid):
    for _ in range(n):
        while True:
            i = random.randint(0, len(grid) - 1)
            j = random.randint(0, len(grid[0]) - 1)

            if grid[i][j].type == 'ground':
                energy = random.randint(50, 80)
                lifetime = random.randint(50, 100)

                social_attitude = random.random()

                animal = animal_class(energy, lifetime, social_attitude, grid[i][j])
                grid[i][j].inhabitants.add(animal)
                break

