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
        self.age += 1
        if self.age % 10 == 0 and self.age != 0:
            self.expend_energy(2)
        if self.age > self.lifetime:
            self.die()

    def get_energy(self):
        return self.energy

    def get_cell(self):
        return self.cell

    def die(self):
        if self.should_spawn_offspring():
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
            if self.herd.getSize < self.herd.max_size:
                offspring1.join_group(self.herd)
                self.cell.inhabitants.add(offspring1)
            if self.herd.getSize < self.herd.max_size:
                offspring2.join_group(self.herd)
                self.cell.inhabitants.add(offspring2)
            
        elif isinstance(self, Carviz):
            if self.pride.getSize < self.pride.max_size:
                offspring1.join_group(self.pride)
                self.cell.inhabitants.add(offspring1)
            if self.pride.getSize < self.pride.max_size:
                offspring2.join_group(self.pride)
                self.cell.inhabitants.add(offspring2)


    def should_spawn_offspring(self):
        """
        Determines whether the animal should spawn offspring.
        If the energy level is above 0 (otherwise the animal is too weak to spawn an offspring), 
        the method calculates a probability based on the energy level and the age of the animal. 
        """
        if self.energy <= 0:
            return False

        energy_threshold = 20
        age_lower_threshold = 20

        energy_factor = 1 / (1 + math.exp(-self.energy + energy_threshold))
        age_factor = 1 / (1 + math.exp(-self.age + age_lower_threshold))

        probability = energy_factor * age_factor

        # Increase the probability to ensure longevity of the simulation
        probability *= 1.5

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
        """
        If the animal is already part of a group, remove it from the group, then add it to a new group.
        Add it to the "target group" if the group.add_member(self) method returns a True value, otherwise
        create a new group such that the animal can join a different group.
        """
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
        if self.pride:
            self.pride.remove_member(self)
        self.pride = None
        

    def leave_group(self):
        self.leave_pride()

    def should_move(self):
        probability_of_moving = 0.2
        
        erbast_present = any(isinstance(animal, Erbast) and not animal.dead for animal in self.cell.inhabitants)

        # Do not move if an Erbast is present in the cell
        if erbast_present:
            return False  

        # Increase the probability if no Erbast is in the cell
        if not erbast_present:
            probability_of_moving += 0.4

        # Increase the probability if the vegetob density is very low (unlikely that an Erbast will come),
        # decrease it if the vegetob density is very high (likely that an Erbast will come in the cell).
        if self.cell.get_vegetob_amount() < 10:
            probability_of_moving += 0.2
        elif self.cell.get_vegetob_amount() > 75:
            probability_of_moving -= 0.2


        probability_of_moving = max(0, min(probability_of_moving, 1))

        return random.random() < probability_of_moving


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
        """
        If the animal is already part of a group, remove it from the group, then add it to a new group.
        Add it to the "target group" if the group.add_member(self) method returns a True value, otherwise
        create a new group such that the animal can join a different group.
        """
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
    
    def eat_poison(self, poison_density):
        # Decrease energy and lifetime based on the density of the poison
        energy_loss = poison_density * 0.2
        
        # In this simulation poisonous vegetob can cause long-term damage shortening the lifetime
        if poison_density > 7:
            lifetime_loss = 1
            if self.age > self.lifetime:
                self.die()

        self.expend_energy(self.cell.vegetob.consume(energy_loss))
        
        
    def leave_herd(self):
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

        # 3rd condition: Increase probability if vegetob amount is low
        if self.cell.get_vegetob_amount() < 20:
            probability_of_moving += 0.3

        probability_of_moving = max(0, min(probability_of_moving, 1))

        return random.random() < probability_of_moving