# TODO: algorithm to turn postfix expression into expression tree 
# the rough schematic will involve popping each pair of terms
# into left and right trees and combining them as we come across
# operations.

class Node:
    def __init__(self, coefficient, power):
        self.coefficient = coefficient
        self.power = power
        self.left = None
        self.right = None

    def __str__(self):
        return f"Node: {self.value}"