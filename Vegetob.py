class Vegetob:
    def __init__(self, density):
        self.density = density

    def get_density(self):
        return self.density

    def growing(self):
        if self.density < 100:
            self.density += 1

    def consume(self, amount_needed):
        # Amount needed is the amount of Vegetob the Erbast needs to reach maximum energy
        consumed_density = min(amount_needed, self.density)
        self.density -= consumed_density
        return consumed_density
