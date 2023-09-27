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
            animal.expend_energy(2)
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
            new_cell = evaluate_herd_cell(neighboring_cells)

            moving_animals = [animal for animal in list(self.members) if animal.should_move()]
        
            if moving_animals:
                herd_to_use = None
                if new_cell.herds:
                    animals = sorted(moving_animals, key=lambda animal : animal.social_attitude)
                    for herd in new_cell.herds:
                        if animals[0].social_attitude > self.threshold:
                            herd_to_use = herd
                            break

                    if herd_to_use is None:
                        herd_to_use = Herd()
                        herd_to_use.cell = new_cell
                        herd_to_use.moved = True
                        herd_to_use.setThreshold(self.threshold)
                        new_cell.herds.append(herd_to_use)
                        


                    for animal in moving_animals:
                        print(f"Erbast with id {animal.id} is moving from cell {self.cell.position} to cell {new_cell.position}")
                        self.cell.inhabitants.remove(animal)
                        new_cell.inhabitants.add(animal)

                        self.remove_member(animal)
                        animal.cell = new_cell
                        animal.herd = herd_to_use
                        animal.join_herd(herd_to_use)

                        animal.expend_energy(5)
                    
        else:
            print("No animals are moving from this herd.")





class Pride(AnimalGroup):
    id_counter = MAX_HERDS

    def __init__(self, max_size=MAX_SIZE):
        super().__init__(max_size)
        self.id = Pride.id_counter
        Pride.id_counter += 1


def evaluate_herd_cell(cells_list):
    max_carviz = max(cell.count_carviz() for cell in cells_list) if cells_list else 0
    max_vegetob = max(cell.get_vegetob_amount() for cell in cells_list) if cells_list else 0

    best_score = -float('inf')
    best_cell = None

    for cell in cells_list:
        # We want to pick the cell with the least number of carvizes possible
        carviz_score = max_carviz + 1 - cell.count_carviz()

        vegetob_score = cell.get_vegetob_amount() / (max_vegetob + 1) if max_vegetob else 0

        score = carviz_score * vegetob_score

        if score > best_score:
            best_score = score
            best_cell = cell

    return best_cell
