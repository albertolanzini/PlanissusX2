from Constants import *
from Groups import *


class Animal:
    def __init__(self, energy, lifetime, social_attitude, cell):
        self.energy = energy
        self.lifetime = lifetime
        self.age = 0
        self.social_attitude = social_attitude
        self.cell = cell  # The cell where this animal currently is
        self.dead = False

    def ageing(self):
        print(f"Aging animal with id {self.id}")
        self.age += 1
        if self.age > self.lifetime:
            self.die()

    def get_energy(self):
        return self.energy

    def get_cell(self):
        return self.cell

    def die(self):
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
        if not pride.add_member(self):
            new_pride = Pride()
            new_pride.setThreshold(0)
            new_pride.add_member(self)
            self.pride = new_pride
            new_pride.cell = self.cell
            new_pride.cell.prides.append(pride)
        else:
            self.pride = pride


    def leave_pride(self):
        """Make sure to add the animal to another Pride after leaving the group. It could create varying issues to let
        the animals stay without a group."""
        if self.pride:
            self.pride.remove_member(self)
        self.pride = None
        

    def leave_group(self):
        self.leave_pride()


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


    def graze(self, vegetob_available):
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