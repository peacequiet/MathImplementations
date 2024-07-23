from ExpressionParser import *
import math
from Helper import *
# TODO: algorithm(s) for simplifying expression trees   - 90% complete
# TODO: GUI                                             - 0% complete
# TODO: unit tests                                      - 10% complete
# TODO: cleanup, separation of concerns                 - 10% complete
# TODO: try-except                                      - 100% complete for the moment

class Node:
    def __init__(self, token):
        self.token = token 
        self.children = []

    def __str__(self):
        return f"Node: {self.token}"
    
    def post_order(node):
        for child in node.children:
            if child is not None:
                Node.post_order(child)
        print(str(node))

    def pre_order(node):
        print(str(node))
        for child in node.children:
            if child is not None:
                Node.pre_order(child)    

# transforms expression into tree
# going to move to new file (?)
def expression_to_tree(expression):
    token_stack = []
    for token in expression:
        if expr_encoding(token) == "num" or expr_encoding(token) == "var":
            node = Node(token)
            token_stack.append(node)
        elif expr_encoding(token) == "func":
            node = Node(token)
            node.children.append(token_stack.pop())
            token_stack.append(node)
        elif token == "~":
            node = Node(token)
            node.children.append(None)
            node.children.append(token_stack.pop())
            token_stack.append(node)
        elif token == "^":
            tree_helper(token, token_stack)
        else:
            tree_helper(token, token_stack)

    return token_stack[0]

def tree_helper(token, token_stack):
    node = Node(token)
    node.children.append(None)
    node.children.append(token_stack.pop())
    node.children[0] = token_stack.pop()
    token_stack.append(node)

# transforms neg and sub into mul by -1
def simp_neg(node):
    if node == None:
        return
    elif node.token == "~":
        node.children[0] = Node("-1")
        node.token = "*"
    elif node.token == "-":
        node.token = "+"
        temp = node.children[1]
        node.children[1] = Node("*")
        node.children[1].children.append(Node("-1"))
        node.children[1].children.append(temp)
    for child in node.children:
        if child is not None:
            simp_neg(child)

    return

# simplifies addition operators, merges them and sends their children to a single node
def simp_level_operators(node):
    if node.token == "+":
        level_operators_logic(node)
    if node.token == "*":
        level_operators_logic(node)
    for child in node.children:
        simp_level_operators(child)

    return

def level_operators_logic(node):
    i = 0
    while i < len(node.children):
        child = node.children[i]
        if child.token == node.token:
            node.children.pop(i)
            node.children += child.children
            child.children.clear()
        else:
            i += 1

# combine like terms
def simp_like_terms(node):
    if node.token == "*":
        for i, child1 in enumerate(node.children):
            if child1.token == "^":
                for j, child2 in enumerate(node.children):
                    if i != j and child2.token == "^" and child2.children[0].token == child1.children[0].token: 
                        simp_like_terms_logic(node, i, j, child2)

    return

def simp_like_terms_logic(node, i, j, child2):
    node.children.pop(j)        # pops child 2
    temp = node.children[i].children[1]
    node.children[i].children[1] = Node("+")
    node.children[i].children[1].children.append(temp)
    node.children[i].children[1].children.append(child2)
    return

# turns division into mul expressions
def simp_dvd(node):
    if node.token == "/":
        if node.children[0].token == "/":
            simp_dvd_logic(node, 0)
        if node.children[1].token == "/":
            simp_dvd_logic(node, 1)
    elif node.token == "*":
        if node.children[1].token == "/":
            simp_mul_dvd_logic(node)
    for child in node.children:
        if child is not None:
            simp_dvd(child)

    return

# special case of simp_dvd
def simp_mul_dvd_logic(node):
    node_a = node.children[0]
    node_b = node.children[1].children[0]
    node_c = node.children[1].children[1]
    new_mul = node.children[1]
    node.children[1].children.clear()
    node.children.clear()
    new_mul.append(node_a)
    new_mul.append(node_b)
    node.children.clear()
    node.append(new_mul)
    node.append(node_c)
    node.token = "/"

# main logic for simp_Dvd
def simp_dvd_logic(node, index):
    div_child_of_node = node.children[index]
    other_child_of_node = node.children[1-index]
    left_child_of_div = div_child_of_node.children[0]
    right_child_of_div = div_child_of_node.children[1]

    node.children = [left_child_of_div if index == 0 else div_child_of_node, 
                     div_child_of_node if index == 0 else right_child_of_div]
    div_child_of_node.children = [right_child_of_div if index == 0 else other_child_of_node,
                                  other_child_of_node if index == 0 else left_child_of_div]
    div_child_of_node.token = "*"

# simplifies addition nodes
def simp_fold_add(node):
    sum = 0
    for child in node.children:
        if child is not None:
            simp_fold_add(child)
    if node.token == "+":
        i = 0
        while i < len(node.children):
            child = node.children[i]
            if child.token == "pi":
                sum += math.pi
                node.children.pop(i)
            elif child.token == "e":
                sum += math.e
                node.children.pop(i)
            elif expr_encoding(child.token) == "num" :
                sum += float(child.token)
                node.children.pop(i)
            else:
                i += 1
        if not node.children:
            node.token = "" + str(sum)
        else:
            sum_node = Node("" + str(sum))
            node.children.append(sum_node)

# simplifies multiplication nodes
def simp_fold_mul(node):
    mul = 1
    for child in node.children:
        if child is not None:
            simp_fold_mul(child)
    if node.token == "*":
        i = 0
        while i < len(node.children):
            child = node.children[i]
            if child.token == "0":
                mul = 0
                node.children.clear()
            elif child.token == "pi":
                mul *= math.pi
                node.children.pop(i)
            elif child.token == "e":
                mul *= math.e
                node.children.pop(i)
            elif expr_encoding(child.token) == "num": 
                mul *= float(child.token)
                node.children.pop(i)
            else:
                i += 1
        if not node.children:
            node.token = "" + str(mul)
        elif mul != 1:
            mul_node = Node("" + str(mul))
            node.children.append(mul_node)

# simplifies power nodes
def simp_fold_pow(node):
    for child in node.children:
        if child is not None:
            simp_fold_pow(child)
    if node.token == "^" and expr_encoding(node.children[0].token) != "var":
        if (node.children[0].token == "0" and node.children[1].token == "0"):
            raise Exception("Sorry, the expression 0 ^ 0 is undefined.")
        else:
            node.token = "" + str(float(node.children[0].token) ** float(node.children[1].token))
            node.children.clear()

def simp_fold(node, changes):
    # record each change 
    # iterate until there are no changes
    return

def simp_canonical_order(node):
    node.children = sorted(node.children, key=lambda child: child.token[0])
    if node.token == "+" or node.token == "*":
        node.children = merge_sort(node.children)
    for child in node.children:
        if child is not None:
            simp_canonical_order(child)
    return

# TODO: simp_fold function that iterates
# TODO: Evaluate/full simp - built into simp_fold iterations
# TODO: Advanced operations

# tokens = expression_tokenizer("-sin(x) * 1 * 20 * tan(pi * x)")
# tokens = expression_tokenizer("(x * 4) * (2 ^ 2) = x")
tokens = expression_tokenizer("(x ^ 4) / (2 ^ 2) / 4 * 6")
print(tokens)
print()
postfix_expression = infix_to_postfix_expression(tokens)
print(postfix_expression)
print()
tree = expression_to_tree(postfix_expression)
simp_neg(tree)
simp_level_operators(tree)
simp_like_terms(tree)
simp_dvd(tree)
simp_fold_pow(tree)
simp_fold_mul(tree)
simp_fold_add(tree)
simp_canonical_order(tree)
tree.post_order()

    

