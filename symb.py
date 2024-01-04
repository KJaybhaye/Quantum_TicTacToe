import random

class Symb:
    def __init__(self, val=0, pos=None, empty=False):
    # self.place = place
        self.val = val
        self.entangled = None
        self.measured = False
        self.pos = pos
        self.empty = empty
        self.symbol = None

    def measure(self):
        if self.measured == True:
            return False
        val = random.randint(1,10)
        self.val = 1 if val <=5 else -1
        self.measured = True
        if self.entangled:
            self.entangled.val = -1 if val <=5 else 1
            self.entangled.measured = True

    def entangle(self, other, embsym=None):
        if self.entangled or other.entangled:
            return False
        self.entangled = other
        other.entangled = self
        if embsym:
            self.symbol = embsym
            other.symbol = embsym