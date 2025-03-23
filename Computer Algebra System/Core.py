from ExpressionParser import *
from Helper import *
from Node import *
import math
# TODO: algorithm(s) for simplifying expression trees   - 100% complete
# TODO: GUI                                             - 0% complete
# TODO: unit tests                                      - 10% complete
# TODO: cleanup, separation of concerns                 - 10% complete
# TODO: try-except                                      - 80% complete 
# TODO: IO
# TODO: Autodiff

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
# node is the input node, changes is number of modifications
def simp_neg(node, changes):
    if node == None:
        return
    elif node.token == "~":
        node.children[0] = Node("-1")
        node.token = "*"
        changes += 1
    elif node.token == "-":
        node.token = "+"
        temp = node.children[1]
        node.children[1] = Node("*")
        node.children[1].children.append(Node("-1"))
        node.children[1].children.append(temp)
        changes += 1
    for child in node.children:
        if child is not None:
            changes += simp_neg(child, 0)
    
    return changes

# simplifies addition operators, merges them and sends their children to a single node
def simp_level_operators(node, changes):
    if node.token == "+*":           # combine these lines?
        changes += level_operators_logic(node, 0)
    for child in node.children:
        changes += simp_level_operators(child, 0)
    
    if node.token in "+*" and len(node.children) == 1:
        node.token = node.children[0].token
        node.children.clear()
    return changes

def level_operators_logic(node, changes):
    i = 0
    while i < len(node.children):
        child = node.children[i]
        if child.token == node.token:
            node.children.pop(i)
            node.children += child.children
            child.children.clear()
            changes += 1
        else:
            i += 1
    return changes

# combine like terms
def simp_like_terms(node, changes):
    if node.token == "*":
        for i, child1 in enumerate(node.children):
            if child1.token == "^":
                for j, child2 in enumerate(node.children):
                    if (i != j and child2.token == "^" 
                        and child2.children[0].token == child1.children[0].token): 
                        simp_like_terms_logic(node, i, j, child2)
                        changes += 1
    for child in node.children:
        if child is not None:
            changes += simp_like_terms(child, 0)

    return changes

def simp_like_terms_logic(node, i, j, child2):
    node.children.pop(j)        # pops child 2
    temp = node.children[i].children[1]
    node.children[i].children[1] = Node("+")
    node.children[i].children[1].children.append(temp)
    node.children[i].children[1].children.append(child2)
    return

# turns division into mul expressions
def simp_dvd(node, changes):
    if node.token == "/":
        if node.children[0].token == "/":
            simp_dvd_logic(node, 0)
            changes += 1
        if node.children[1].token == "/":
            simp_dvd_logic(node, 1)
            changes += 1
    elif node.token == "*":
        if node.children[1].token == "/":
            simp_mul_dvd_logic(node)
            changes += 1
    for child in node.children:
        if child is not None:
            changes += simp_dvd(child, 0)

    return changes

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

    node.children = [left_child_of_div if index == 0 
                     else div_child_of_node, 
                     div_child_of_node if index == 0 
                     else right_child_of_div]
    div_child_of_node.children = [right_child_of_div if index == 0 
                                  else other_child_of_node,
                                  other_child_of_node if index == 0 
                                  else left_child_of_div]
    div_child_of_node.token = "*"

# folds additions into single constant when possible
def simp_fold_add(node, changes):
    sum = 0
    for child in node.children:
        if child is not None:
            changes += simp_fold_add(child, 0)
    if node.token == "+":
        sum, changes = fold_add_logic(node, changes)
        if not node.children:
            node.token = "" + str(sum)
        elif changes > 0 and sum != 0:
            sum_node = Node("" + str(sum))
            node.children.append(sum_node)

    return changes

def fold_add_logic(node, changes):
    sum = 0
    i = 0
    while i < len(node.children):
        child = node.children[i]
        if child.token == "pi":
            sum += math.pi
            node.children.pop(i)
            changes += 1
        elif child.token == "e":
            sum += math.e
            node.children.pop(i)
            changes += 1
        elif (expr_encoding(child.token) == "num" 
                and ((len(node.children) > 1 
                and expr_encoding(node.children[1].token) != "var" 
                and expr_encoding(node.children[0].token) == "num")
                or sum != 0)):
            sum += float(child.token)
            node.children.pop(i)
            changes += 1
        else:
            i += 1
    return sum, changes

# fold muls logic
def simp_fold_mul(node, changes):
    mul = 1
    for child in node.children:
        if child is not None:
            changes += simp_fold_mul(child, 0)
    if node.token == "*":
        changes, mul = fold_mul_logic(node, changes, mul)
        if not node.children:                       
            node.token = "" + str(mul)
        elif mul != 1:
            mul_node = Node("" + str(mul))
            node.children.append(mul_node)

    return changes

def fold_mul_logic(node, changes, mul):
    i = 0
    while i < len(node.children):
        child = node.children[i]
        if child.token == "0" or child.token == "0.0":
            mul = 0
            node.children.clear()
            changes += 1
        elif child.token == "pi":
            mul *= math.pi
            node.children.pop(i)
            changes += 1
        elif child.token == "e":
            mul *= math.e
            node.children.pop(i)
            changes += 1
        elif (expr_encoding(child.token) == "num" 
                and ((len(node.children) > 1 
                and expr_encoding(node.children[1].token) != "var" 
                and expr_encoding(node.children[0].token) == "num") 
                or mul != 1)): 
            mul *= float(child.token)
            node.children.pop(i)
            changes += 1
        else:
            i += 1
    return changes, mul

# simplifies power nodes
def simp_fold_pow(node, changes):
    for child in node.children:
        if child is not None:
            changes += simp_fold_pow(child, 0)
    if node.token == "^" and expr_encoding(node.children[0].token) != "var":
        if (node.children[0].token == "0" and node.children[1].token == "0"):
            raise Exception("Sorry, the expression 0 ^ 0 is undefined.")
        else:
            node.token = "" + str(float(node.children[0].token) ** float(node.children[1].token))
            node.children.clear()
            changes += 1

    return changes

# gives expressions a regular order
def simp_canonical_order(node):
    node.children = sorted(node.children, key=lambda child: child.token[0])
    if node.token == "+" or node.token == "*":
        node.children = merge_sort(node.children)
    for child in node.children:
        if child is not None:
            simp_canonical_order(child)

    return

# simplifies and folds trigs
def simp_fold_trig(node, changes):
    for child in node.children:
        if child is not None:
            changes += simp_fold_trig(child, 0)
    if node.token in ("sin", "cos", "tan"):
        if expr_encoding(node.children[0].token) == "num":
            node.token = str(trig_funcs(node.token, float(node.children[0].token)))
            node.children.clear()
            changes += 1
    return changes

def trig_funcs(token, value):
    if token == "sin":
        return math.sin(value)
    elif token == "cos":
        return math.cos(value)
    elif token == "tan":
        return math.tan(value)

# fold divisions 
def simp_fold_dvd(node, changes):
    div = 1
    for child in node.children:
        if child is not None:
            changes += simp_fold_dvd(child, 0)
    if node.token == "/":
        changes, div = fold_dvd(node, changes, div)
        if not node.children:
            node.token = "" + str(div)
        else:
            div_node = Node("" + str(div))
            node.children.append(div_node)
    return changes

def fold_dvd(node, changes, div):
    i = 0
    while i < len(node.children):
        child = node.children[i]
        if child.token == "0" or child.token == "0.0":
            raise Exception("Division by zero error.")
        elif child.token in ["pi", "e"]:
            div = div_helper(div, child.token)
            node.children.pop(i)
            changes += 1
        elif (expr_encoding(child.token) == "num" 
                and ((len(node.children) > 1 
                and expr_encoding(node.children[1].token) != "var" 
                and expr_encoding(node.children[0].token) == "num") 
                or div != 1)):
            div = div_helper(div, child.token)
            node.children.pop(i)
            changes += 1
        else:
            i += 1
    return changes, div

def div_helper(div, token):
    if div == 1:
        if token == "pi":
            div = math.pi
        elif token == "e":
            div = math.e
        else:
            div = float(token)
    else:
        if token == "pi":
            div /= math.pi
        elif token == "e":
            div /= math.e
        else:
            div /= float(token)
    return div

# performs all simp operations
def simp_fold(node):
    start = True
    while start:
        changes = 0
        changes += simp_neg(node, 0)
        changes += simp_level_operators(node, 0)
        changes += simp_like_terms(node, 0)
        changes += simp_dvd(node, 0)
        changes += simp_fold_pow(node, 0)
        changes += simp_fold_mul(node, 0)
        changes += simp_fold_add(node, 0)
        changes += simp_fold_trig(node, 0)
        changes += simp_fold_dvd(node, 0)
        simp_canonical_order(node)
        if changes == 0:
            start = False
    simp_canonical_order(node)
    return

# TODO: User input
def user_input():
    expression = input("Please enter an expression: ")
    tree = expression_to_tree(expression_parser(expression))
    simp_fold(tree)
    tree.post_order()
    return

# TODO: simp_fold function that iterates - 90% complete (needs testing)
# TODO: Advanced operations (autodiff)

# LAUNCH
# user_input()

# tree = expression_to_tree(expression_parser("+ 3 + "))
# simp_fold(tree)
# tree.post_order()

    

