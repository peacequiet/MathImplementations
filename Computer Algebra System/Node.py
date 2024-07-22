from ExpressionParser import *
# TODO: algorithm(s) for simplifying expression trees
# TODO: cleanup, separation of concerns

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
            node = Node(token)
            node.children.append(None)
            node.children.append(token_stack.pop())
            node.children[0] = token_stack.pop()
            token_stack.append(node)
        else:
            node = Node(token)
            node.children.append(None)
            node.children.append(token_stack.pop())
            node.children[0] = token_stack.pop()
            token_stack.append(node)

    return token_stack[0]

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
        for i, child in enumerate(node.children):
            if child.token == "+":
                node.children.pop(i)
                node.children += child.children
                child.children.clear()
    if node.token == "*":
        for i, child in enumerate(node.children):
            if child.token == "*":
                node.children.pop(i)
                node.children += child.children
                child.children.clear()
    for child in node.children:
        simp_level_operators(child)

    return 

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

# TODO: Division simplification
# def simp_division(node):

# tokens = expression_tokenizer("-sin(x) + 1 - 2 * tan(pi * x)")
tokens = expression_tokenizer("2 ^ 7 * 2 ^ 3")
print(tokens)
print()
postfix_expression = infix_to_postfix_expression(tokens)
print(postfix_expression)
print()
tree = expression_to_tree(postfix_expression)
# tree.post_order()
simp_neg(tree)
simp_level_operators(tree)
simp_like_terms(tree)
tree.post_order()

    

