from Constants import *


class AnimalGroup:
    def __init__(self, max_size):
        self.members = []
        self.max_size = MAX_SIZE

    def add_member(self, animal):
        if len(self.members) < self.max_size:
            self.members.append(animal)
            return True
        return False

    def remove_member(self, animal):
        if animal in self.members:
            self.members.remove(animal)

    @property
    def getSize(self):
        return len(self.members)

    def isFull(self):
        return len(self.members) >= self.max_size


class Herd(AnimalGroup):
    def __init__(self, max_size=MAX_SIZE):
        super().__init__(max_size)

    def graze(self):
        for erbast in self.members:
            vegetob_available = erbast.get_cell().vegetob.get_density()
            vegetob_per_erbast = vegetob_available/len(self.members)
            erbast.graze(vegetob_per_erbast)


class Pride(AnimalGroup):
    def __init__(self, max_size=MAX_SIZE):
        super().__init__(max_size)

