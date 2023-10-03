class Vegetob:
    def __init__(self, density):
        self.density = density
        self.poisonous = False

    def get_density(self):
        return self.density

    def growing(self):
        if self.density < 100:
            self.density = min(100, self.density + 2)

    def consume(self, amount_needed):
        # Amount needed is the amount of Vegetob the Erbast needs to reach maximum energy
        # min function necessary to ensure density does not become negative
        consumed_density = min(amount_needed, self.density) 
        self.density -= consumed_density
        return consumed_density
