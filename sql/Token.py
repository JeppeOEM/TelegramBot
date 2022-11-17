

class Token:

    def __init__(self, address, bhoughtAt, threshold, amount):
        self.address = address
        self.bhoughtAt = bhoughtAt
        self.threshold = threshold
        self.amount = amount

    #def __repr__(self):
    #    return "Token('{}', '{}', {})".format(self.address, self.bhoughtAt, self.threshold, self.amount)
