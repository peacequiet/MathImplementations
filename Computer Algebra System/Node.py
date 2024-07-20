class Node:
    def __init__(self, coefficient, power):
        self.coefficient = coefficient
        self.power = power
        self.left = None
        self.right = None

    def __str__(self):
        return f"Node: {self.value}"