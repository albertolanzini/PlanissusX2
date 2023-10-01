from Constants import *
from Groups import Pride, Herd
import random
import math

class Animal:
    def __init__(self, energy, lifetime, social_attitude, cell):
        self.energy = energy
        self.lifetime = lifetime
        self.age = 0
        self.social_attitude = social_attitude
        self.cell = cell  # The cell where this animal currently is
        self.dead = False

    def ageing(self):
        # print(f"Aging animal with id {self.id}")
        self.age += 1
        if self.age % 10 == 0 and self.age != 0:
            self.expend_energy(5) # value to be later determined
        if self.age > self.lifetime:
            self.die()

    def get_energy(self):
        return self.energy

    def get_cell(self):
        return self.cell

    def die(self):
        if self.should_spawn_offspring():
            # print(f"Erbast {self.id} has spawned two erbasts")
            self.spawn_offspring()
        self.leave_group()
        self.dead = True

    def leave_group(self):
        pass

    def join_group(self, group):
        pass

    def expend_energy(self, amount):
        self.energy -= amount
        if self.energy <= 0:
            self.die()

    def spawn_offspring(self):
        # Generate lifetime for the offspring using standard deviation
        mean_lifetime = self.lifetime
        std_dev_lifetime = mean_lifetime * 0.1  # Assuming standard deviation is 10% of the mean
        lifetime1 = max(0, min(round(random.gauss(mean_lifetime, std_dev_lifetime)), 100))
        lifetime2 = (2 * self.lifetime) - lifetime1

        # Generate energy for the offspring with a fixed value between 35 and 60
        energy1 = random.randint(35, 60)
        energy2 = random.randint(35, 60)

        offspring1 = self.__class__(
            energy=energy1,
            lifetime=lifetime1,
            social_attitude=self.social_attitude,
            cell=self.cell
        )

        offspring2 = self.__class__(
            energy=energy2,
            lifetime=lifetime2,
            social_attitude=self.social_attitude,
            cell=self.cell
        )

        if isinstance(self, Erbast):
            # print(f"Erbast {self.id} spawned two offsprings")
            # print(f"Before adding, herd members: {[erbast.id for erbast in self.herd.members]}")
            if self.herd.getSize < self.herd.max_size:
                offspring1.join_group(self.herd)
                self.cell.inhabitants.add(offspring1)
            if self.herd.getSize < self.herd.max_size:
                offspring2.join_group(self.herd)
                self.cell.inhabitants.add(offspring2)
            # print(f"Spawned offspring 1 with ID: {offspring1.id}, energy: {offspring1.energy}, lifetime: {offspring1.lifetime}, herd: {offspring1.herd.id}")
            # print(f"Spawned offspring 2 with ID: {offspring2.id}, energy: {offspring2.energy}, lifetime: {offspring2.lifetime}, herd: {offspring2.herd.id}")
            # print(f"After adding, herd members: {[erbast.id for erbast in self.herd.members]}")
        elif isinstance(self, Carviz):
            # print(f"Carviz {self.id} spawned two offsprings")
            # print(f"Before adding, pride members: {[carviz.id for carviz in self.pride.members]}")
            if self.pride.getSize < self.pride.max_size:
                offspring1.join_group(self.pride)
                self.cell.inhabitants.add(offspring1)
            if self.pride.getSize < self.pride.max_size:
                offspring2.join_group(self.pride)
                self.cell.inhabitants.add(offspring2)
            # print(f"After adding, pride members: {[carviz.id for carviz in self.pride.members]}")

        # print(f"Before adding, cell inhabitants: {[animal.id for animal in self.cell.inhabitants]}")
        # print(f"After adding, cell inhabitants: {[animal.id for animal in self.cell.inhabitants]}")

    def should_spawn_offspring(self):
        if self.energy <= 0:
            return False

        energy_threshold = 20
        age_lower_threshold = 20

        energy_factor = 1 / (1 + math.exp(-self.energy + energy_threshold))
        age_factor = 1 / (1 + math.exp(-self.age + age_lower_threshold))

        probability = energy_factor * age_factor

        return random.random() < probability

        

class Carviz(Animal):
    id_counter = 0  # Class variable to ensure unique ids for each Carviz

    def __init__(self, energy, lifetime, social_attitude, cell):
        super().__init__(energy, lifetime, social_attitude, cell)
        self.id = Carviz.id_counter
        Carviz.id_counter += 1
        self.pride = None

    def join_group(self, group):
        self.leave_group()
        if isinstance(group, Pride):
            self.join_pride(group)

    def join_pride(self, pride):
        if self.pride is not None:
            self.pride.remove_member(self)
        pride.cell = self.cell
        if not pride.add_member(self):
            self.leave_pride()
            new_pride = Pride()
            new_pride.setThreshold(0)
            new_pride.add_member(self)
            self.pride = new_pride
            new_pride.cell = self.cell
            new_pride.cell.prides.append(new_pride)
        else:
            self.pride = pride
            pride.cell = self.cell
            if pride not in pride.cell.prides:
                pride.cell.prides.append(pride)

    def leave_pride(self):
        """Make sure to add the animal to another Pride after leaving the group. It could create varying issues to let
        the animals stay without a group."""
        if self.pride:
            self.pride.remove_member(self)
        self.pride = None
        

    def leave_group(self):
        self.leave_pride()

    def should_move(self):
        return True


class Erbast(Animal):
    id_counter = nCarviz + 1

    def __init__(self, energy, lifetime, social_attitude, cell):
        super().__init__(energy, lifetime, social_attitude, cell)
        self.herd = None
        self.id = Erbast.id_counter
        self.moved = False  # New attribute
        self.lastVisitedCell = None
        Erbast.id_counter += 1

    def join_group(self, group):
        self.leave_group()
        if isinstance(group, Herd):
            self.join_herd(group)

    def join_herd(self, herd):
        if self.herd is not None:
            self.herd.remove_member(self)
        herd.cell = self.cell
        if not herd.add_member(self):
            self.leave_herd()
            new_herd = Herd()
            new_herd.setThreshold(0)
            new_herd.add_member(self)
            self.herd = new_herd
            new_herd.cell = self.cell
            new_herd.cell.herds.append(new_herd)
        else:
            self.herd = herd
            herd.cell = self.cell
            if herd not in herd.cell.herds:
                herd.cell.herds.append(herd)


    def eat_vegetob(self, vegetob_available):
        # The Erbast eats the biggest amount of Vegetob to reach maximum energy (100)
        amount_needed = max(0, 100 - self.energy)

        # limit the consumption to the available vegetob
        amount_needed = min(amount_needed, vegetob_available)
        energy_gain = self.cell.vegetob.consume(amount_needed)
        self.energy += energy_gain

    def leave_herd(self):
        """Make sure to add the animal to another Pride after leaving the group. It could create varying issues to let
        the animals stay without a group."""
        if self.herd:
            self.herd.remove_member(self)
        self.herd = None

    def leave_group(self):
        self.leave_herd()

    def should_move(self):
        probability_of_moving = 0.2

        # 1st condition: Increase the probability a lot if a Carviz is in the cell
        carviz_present = any(isinstance(animal, Carviz) for animal in self.cell.inhabitants)

        if carviz_present:
            probability_of_moving += 0.5

        # 2nd condition: Decrease probability if energy is very low
        if self.energy < 15:
            probability_of_moving -= 0.4

        if self.cell.get_vegetob_amount() < 20:
            probability_of_moving += 0.3

        probability_of_moving = max(0, min(probability_of_moving, 1))

        return random.random() < probability_of_moving