import random


class Clan:
    def __init__(self):
        self.color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        self.members = []
        self.strength = random.randint(1, 10)  # Random clan strength

    def size(self):
        return len(self.members)

    def total_strength(self):
        return self.size() * self.strength
