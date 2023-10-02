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
        self.lastVisitedCell = None

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

    def get_average_social_attitude(self):
        return sum(member.social_attitude for member in self.members) / self.getSize
    
    def get_average_energy(self):
        return sum(member.energy for member in self.members) / self.getSize

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
        """
        The animals will be sorted in ascending manner and the amount of vegetob per animal will be weighted
        thanks to the energy level, so that the animals with a lower energy inside the herd get more and the 
        others get less.
        When multiple herds are present in the cell, I decided to adopt a First come, first served mechanism
        as it resembles nature better and it creates a more dynamic environment.
        """
    
        vegetob_available = self.cell.get_vegetob_amount()

        # Sort the erbasts based on their energy levels in ascending order
        sorted_members = sorted(self.members, key=lambda erbast: erbast.energy)

        # Calculate the total energy deficit of all erbasts in the herd
        total_deficit = sum([100 - erbast.energy for erbast in sorted_members])


        # Calculate the total amount of vegetob that each erbast should eat
        vegetob_per_erbast = [((100 - erbast.energy) / total_deficit) * vegetob_available if total_deficit else 0 for erbast in sorted_members]

        erbast_vegetob_pairs = zip(sorted_members, vegetob_per_erbast)

        # Distribute the vegetob among the erbasts
        for erbast, vegetob in erbast_vegetob_pairs:
            erbast.eat_vegetob(vegetob)



    def move(self):
        
        neighboring_cells = get_neighboring_cells(self.cell.grid, self.cell)
        neighboring_cells = [i for i in neighboring_cells if i != self.lastVisitedCell]
        
        if neighboring_cells:
            new_cell = evaluate_herd_cell(neighboring_cells)

            if new_cell.count_erbast() == 20:
                return

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
                    if new_cell.count_erbast() == 20:
                        return
                    # print(f"Erbast with id {animal.id} is moving from cell {self.cell.position} to cell {new_cell.position}")
                    self.cell.inhabitants.remove(animal)
                    new_cell.inhabitants.add(animal)

                    self.remove_member(animal)
                    animal.cell = new_cell
                    animal.herd = herd_to_use
                    animal.join_herd(herd_to_use)

                    animal.expend_energy(5)

                self.lastVisitedCell = self.cell
                herd_to_use.lastVisitedCell = self.cell
        
        else:
            pass
            # print("No animals are moving from this herd.")


class Pride(AnimalGroup):
    id_counter = MAX_HERDS

    def __init__(self, max_size=MAX_SIZE):
        super().__init__(max_size)
        self.id = Pride.id_counter
        Pride.id_counter += 1

    def move(self):
        from Animals import Erbast

        # There is no need to move if there is an erbast already in the cell
        if any(isinstance(animal, Erbast) for animal in self.cell.inhabitants):
            return
        
        neighboring_cells = get_neighboring_cells(self.cell.grid, self.cell)
        neighboring_cells = [i for i in neighboring_cells if i != self.lastVisitedCell]

            
    
        if neighboring_cells:
            
            if random.random() > 0.90:
                new_cell = random.choice(neighboring_cells)
            else:
                new_cell = evaluate_pride_cell(neighboring_cells)

            if new_cell.count_carviz() >= 20:
                return

            moving_animals = [animal for animal in list(self.members) if animal.should_move()]
    
            if moving_animals:
                pride_to_use = None
                if new_cell.prides:
                    animals = sorted(moving_animals, key=lambda animal : animal.social_attitude)
                    for pride in new_cell.prides:
                        if animals[0].social_attitude > self.threshold:
                            pride_to_use = pride
                            break

                if pride_to_use is None:
                    pride_to_use = Pride()
                    pride_to_use.cell = new_cell
                    pride_to_use.moved = True
                    pride_to_use.setThreshold(self.threshold)
                    new_cell.prides.append(pride_to_use)
                    
                for animal in moving_animals:
                    if new_cell.count_erbast() == 20:
                        return
                    # print(f"Carviz with id {animal.id} is moving from cell {self.cell.position} to cell {new_cell.position}")
                    self.cell.inhabitants.remove(animal)
                    new_cell.inhabitants.add(animal)

                    self.remove_member(animal)
                    animal.cell = new_cell
                    animal.pride = pride_to_use
                    animal.join_pride(pride_to_use)

                    animal.expend_energy(2)

                self.lastVisitedCell = self.cell
                pride_to_use.lastVisitedCell = self.cell

    def should_join(self, other_pride):
        first = self.get_average_social_attitude()
        second = other_pride.get_average_social_attitude()

        # Difference in average social attitudes
        diff_social_attitude = abs(first - second)

        # The probability of joining is inversely proportional to the difference in social attitude.
        join_probability = 1.0 / (1 + np.exp(-2 * diff_social_attitude))

        return np.random.random() < join_probability
    
    def feed(self, prey):
        """
        The animals will be sorted in ascending manner and the amount of energy per animal will be weighted
        thanks to the energy level, so that the animals with a lower energy inside the pride get more and the 
        others get less.
        """

        # The total energy available from the prey
        prey_energy = prey.energy

        # Sort the animals based on their energy levels in ascending order
        sorted_members = sorted(self.members, key=lambda animal: animal.energy)

        # Calculate the total energy deficit of all animals in the pride
        total_deficit = sum([100 - animal.energy for animal in sorted_members])

        # Calculate the total amount of energy that each animal should get
        energy_per_animal = [(100 - animal.energy) / total_deficit * prey_energy if total_deficit else 0 for animal in sorted_members]

        animal_energy_pairs = zip(sorted_members, energy_per_animal)

        # print(prey_energy)
        # print(animal_energy_pairs)
        

        # Distribute the energy among the animals
        for animal, energy in animal_energy_pairs:
            # print(f"Before feeding: Carviz {animal.id}, energy: {animal.energy}")
            animal.energy += min(energy, 100 - animal.energy)  # Ensure the energy never exceeds 100
            # print(f"After feeding: Carviz {animal.id}, energy: {animal.energy}")

        
    def hunt(self):

        # print(f"Before hunt, herds in cell {self.cell.position}: {[herd.id for herd in self.cell.herds]}")

        if len(self.cell.herds) == 0:
            return

        strongest_erbast = max(self.cell.herds[0].members, key=lambda erbast: erbast.energy)

        attempts = round(self.getSize * (self.get_average_energy() / 100))

        for _ in range(attempts):
            average_energy_pride = self.get_average_energy()
            winning_probability_pride = (average_energy_pride * self.getSize) / ((average_energy_pride * self.getSize) + strongest_erbast.energy)

            if random.random() < winning_probability_pride:
                # print(f"Pride {self.id} successfully hunted Erbast {strongest_erbast.id}")
                # Remove the Erbast from the herd
                self.feed(strongest_erbast)
                strongest_erbast.die()
                break
            else:
                # print(f"Pride {self.id} failed to hunt Erbast {strongest_erbast.id}")
                # Choose a random member to lose energy
                random_member = random.choice(self.members)
                random_member.expend_energy(5)

        # print(f"After hunt, herds in cell {self.cell.position}: {[herd.id for herd in self.cell.herds]}")


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

def evaluate_pride_cell(cells_list):
    # Step 1: Check for number of erbasts in each cell
    min_erbasts = min(cell.count_erbast() for cell in cells_list) if cells_list else 0

    # List of cells with the minimum number of erbasts
    min_erbast_cells = [cell for cell in cells_list if cell.count_erbast() == min_erbasts]

    if min_erbasts > 0:
        # If there are cells with erbasts, return the first one
        return min_erbast_cells[0]
    else:
        # Step 2: If no animals are present, check for the cell with the greatest amount of vegetob
        max_vegetob = max(cell.get_vegetob_amount() for cell in cells_list) if cells_list else 0

        # List of cells with the maximum amount of vegetob
        max_vegetob_cells = [cell for cell in cells_list if cell.get_vegetob_amount() == max_vegetob]

        # Return the first cell with the maximum amount of vegetob
        return max_vegetob_cells[0]