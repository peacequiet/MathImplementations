from ExpressionParser import *
# TODO: algorithm for simplifying expression trees
#   Sub-TODO: refactor node to have a list of children

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

    def post_order(node):
        if node == None:
            return 
        Node.in_order(node.left)
        Node.in_order(node.right)
        print(str(node))

    def pre_order(node):
        if node == None:
            return 
        Node.in_order(node.left)
        Node.in_order(node.right)
        print(str(node))
    

# transforms expression into tree
# going to move to new file (?)
def expression_to_tree(expression):
    token_stack = []
    for token in expression:
        if expr_encoding(token) == "num":
            node = Node(token)
            token_stack.append(node)
        elif expr_encoding(token) == "func":
            node = Node(token)
            node.right = token_stack.pop()
            token_stack.append(node)
        elif token == "~":
            node = Node(token)
            node.right = token_stack.pop()
            token_stack.append(node)
        else:
            node = Node(token)
            node.right = token_stack.pop()
            node.left = token_stack.pop()
            token_stack.append(node)

    return token_stack[0]

# transforms neg and sub into mul by -1
def simp_neg(node):
    if node == None:
        return
    elif node.token == "~":
        node.left = Node("-1")
        node.token = "*"
    elif node.token == "-":
        node.token = "+"
        temp = node.right
        node.right = Node("*")
        node.right.left = Node("-1")
        node.right.right = temp

    simp_neg(node.left)
    simp_neg(node.right)
    return

        

tokens = expression_tokenizer("-sin(x) + 1 - 2 * tan(pi * x)")
print(tokens)
print()
postfix_expression = infix_to_postfix_expression(tokens)
print(postfix_expression)
print()
tree = expression_to_tree(postfix_expression)
simp_neg(tree)
tree.in_order()

    

