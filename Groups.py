from Constants import *
import numpy as np
from utils import get_neighboring_cells
import random
from Animals import *

def generate_threshold(mean=0.275, std_dev=0.1, min_val=0, max_val=0.4):
    threshold = np.random.normal(loc=mean, scale=std_dev)
    threshold = np.clip(threshold, min_val, max_val)  # Clip the values to be within the desired range
    return threshold


class AnimalGroup:
    def __init__(self, max_size, threshold=0.0):
        self.members = []
        self.max_size = MAX_SIZE
        self.threshold = threshold
        self.cell = None
        self.moved = False

    def add_member(self, animal):
        if len(self.members) < self.max_size and animal not in self.members:
            if self.threshold < animal.social_attitude:
                self.members.append(animal)

                if self.cell is None:
                    self.cell = animal.cell
                
                return True
        return False

    def remove_member(self, animal):
        if animal in self.members:
            self.members.remove(animal)

        if not self.members and self in self.cell.herds:
            self.cell.herds.remove(self)
        

    @property
    def getSize(self):
        return len(self.members)

    def isFull(self):
        return len(self.members) >= self.max_size

    def setThreshold(self, value):
        self.threshold = value

    def age_group(self):
        i = 0
        while i < len(self.members):
            animal = self.members[i]
            animal.ageing()
            if animal.dead:
                self.remove_member(animal)
            else:
                i += 1


class Herd(AnimalGroup):
    id_counter = 0

    def __init__(self, max_size=MAX_SIZE, threshold=generate_threshold()):
        super().__init__(max_size, threshold)
        self.id = Herd.id_counter
        Herd.id_counter += 1

    def graze(self):
        for erbast in self.members:
            vegetob_available = erbast.get_cell().vegetob.get_density()
            vegetob_per_erbast = vegetob_available/len(self.members)
            erbast.graze(vegetob_per_erbast)


    def move(self):
        
        neighboring_cells = get_neighboring_cells(self.cell.grid, self.cell)
        
        if neighboring_cells:
            new_cell = random.choice(neighboring_cells)

            moving_animals = [animal for animal in list(self.members) if random.random() < MOVE_PROBABILITY]
        
            if moving_animals:
                new_herd = Herd()
                new_herd.cell = new_cell
                new_herd.moved = True
                new_herd.setThreshold(self.threshold)
                new_cell.herds.append(new_herd)

                for animal in moving_animals:
                    print(f"Erbast with id {animal.id} is moving from cell {self.cell.position} to cell {new_cell.position}")
                    self.remove_member(animal)
                    animal.cell = new_cell
                    animal.herd = new_herd
                    new_herd.add_member(animal)
                    
        else:
            print("No animals are moving from this herd.")





class Pride(AnimalGroup):
    id_counter = MAX_HERDS

    def __init__(self, max_size=MAX_SIZE):
        super().__init__(max_size)
        self.id = Pride.id_counter
        Pride.id_counter += 1