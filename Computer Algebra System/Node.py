from ExpressionParser import *
# TODO: algorithm for simplifying expression trees

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
# going to move to new file
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

# def simp_neg(node):
#     if node == None:
#         return
#     if node.value == "-":

        

tokens = expression_tokenizer("-sin(x) + 1 - 2 * tan(pi * x)")
postfix_expression = infix_to_postfix_expression(tokens)
tree = expression_to_tree(postfix_expression)
tree.in_order()
print()
    

