
class Node:
    def __init__(self, coefficient, power):
        self.coefficient = coefficient
        self.power = power
        self.left = None
        self.right = None

    def __str__(self):
        return f"Node: {self.value}"

# translates our expression from infix to postfix notation 
# to prepare for tree construction.
def infix_to_postfix_expression(expression):   
    postfix_str = ""
    op_stack = []
    for entry in expression:
        if expr_encoding(entry) == -1:
            postfix_str = postfix_str + entry
        elif expr_encoding(entry) > -1:             #TODO: split into separate method
            if op_stack.peek() is not None:

    return postfix_str

# special encoding 
def expr_encoding(entry):
    if ord(entry) == 45:        # subtraction 
        return 5        
    elif ord(entry) == 43:      # addition
        return 4
    elif ord(entry) == 47:      # division
        return 3
    elif ord(entry) == 42:      # multiplication
        return 2
    elif ord(entry) == 94:      # exponentiation
        return 1
    elif ord(entry) == 40:      # open parens
        return 0
    elif ord(entry) == 41:      # close parens
        return 0
    elif ord(entry) == 61:      # equals sign
        return 0
    elif (ord(entry) >= 48 and ord(entry) <= 57): # numerical operands
        return -1
    elif (ord(entry) >= 65 and ord(entry) <= 90): # variable operands
        return -1
    elif (ord(entry) >= 97 and ord(entry) <= 122):
        return -1
    else:
        return None
    
print(infix_to_postfix_expression("1 + x + E"))