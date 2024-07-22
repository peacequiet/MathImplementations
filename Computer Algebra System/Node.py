from ExpressionParser import *
# TODO: algorithm(s) for simplifying expression trees - 40% complete
# TODO: GUI - 0% complete
# TODO: unit tests - 0% complete
# TODO: cleanup, separation of concerns - 10% complete
# TODO: try-except - partially complete

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
        if expr_encoding(token) == "num":
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
        simp_dvd(child)

    return

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

def simp_fold_constants(node):
    sum = 0
    if node.token == "+":
        i = 0
        while i < len(node.children):
            child = node.children[i]
            if expr_encoding(child.token) == "num":
                sum += int(child.token)
                node.children.pop(i)
            else:
                i += 1
    if not node.children:
        node.token = "" + str(sum)
    else:
        sum_node = Node("" + str(sum))
        node.children.append(sum_node)
    
# TODO: Canonical order simp
# TODO: Evaluate/full simp
# TODO: Advanced operations

# tokens = expression_tokenizer("-sin(x) * 1 * 20 * tan(pi * x)")
tokens = expression_tokenizer("2 + 2 + 2 + 2 * 3")
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
simp_fold_constants(tree)
tree.post_order()

    

