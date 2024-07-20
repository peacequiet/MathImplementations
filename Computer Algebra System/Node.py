from ExpressionParser import *
# TODO: algorithm to turn postfix expression into expression tree 
# the rough schematic will involve popping each pair of terms
# into left and right trees and combining them as we come across
# operations.

class Node:
    def __init__(self, token):
        self.token = token 
        self.left = None
        self.right = None

    def __str__(self):
        return f"Node: {self.token}"
    
    def in_order(node):
        if node == None:
            return 
        Node.in_order(node.left)
        print(str(node))
        Node.in_order(node.right)

class Tree:
    def __init__(self, root):
        self.root = root
    
    def __str__(self):
        return f"Root: {self.root.token}"
    
node1 = Node("3")
node2 = Node("2")
node3 = Node("3")
node2.left = node1
node2.right = node3

# node2.in_order()

# transforms expression into tree
def expression_to_tree(expression):
    token_stack = []
    for token in expression:
        if expr_encoding(token) == None:
            node = Node(token)
            token_stack.append(node)
        else:
            node = Node(token)
            node.right = token_stack.pop()
            node.left = token_stack.pop()
            token_stack.append(node)

    return token_stack[0]

expression_to_tree(infix_to_postfix_expression("( 1 + 2 ) ^ 3 * 7 - ( 3 - 2 * 4 )")).in_order()
    

