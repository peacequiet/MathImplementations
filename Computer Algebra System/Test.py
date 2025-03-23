from Core import *
from Node import *

# TODO: complete autodiff https://en.wikipedia.org/wiki/Automatic_differentiation

tree = expression_to_tree(expression_parser("x + 2"))

# autodiff
def differentiate(node, var):
    # for child in node.children:
    #     if child is not None:
    #         differentiate(child)
    if expr_encoding(node.token) == "var":
        if node.token == var:
            node.token = "1"
        else:
            node.token = "0"
    elif expr_encoding(node.token) == "+":
        for child in node.children:
            differentiate(child, var)
    return

differentiate(tree)

Node.post_order(tree)