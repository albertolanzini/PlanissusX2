from Constants import *
import numpy as np


def generate_threshold(mean=0.275, std_dev=0.1, min_val=0, max_val=0.4):
    threshold = np.random.normal(loc=mean, scale=std_dev)
    threshold = np.clip(threshold, min_val, max_val)  # Clip the values to be within the desired range
    return threshold


class AnimalGroup:
    def __init__(self, max_size, threshold=0.0):
        self.members = []
        self.max_size = MAX_SIZE
        self.threshold = threshold

    def add_member(self, animal):
        if len(self.members) < self.max_size:
            if self.threshold < animal.social_attitude:
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

    def setThreshold(self, value):
        self.threshold = value


class Herd(AnimalGroup):
    def __init__(self, max_size=MAX_SIZE, threshold=generate_threshold()):
        super().__init__(max_size, threshold)

    def graze(self):
        for erbast in self.members:
            vegetob_available = erbast.get_cell().vegetob.get_density()
            vegetob_per_erbast = vegetob_available/len(self.members)
            erbast.graze(vegetob_per_erbast)


class Pride(AnimalGroup):
    def __init__(self, max_size=MAX_SIZE):
        super().__init__(max_size)

