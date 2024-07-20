
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
    visited_str = ""
    op_stack = []
    for entry in expression:
        visited_str = visited_str + entry
        if ord(entry) >= 48 and ord(entry) <= 57:       # numerical operands
            postfix_str = postfix_str + entry
        elif ord(entry) >= 65 and ord(entry) <= 90:     # variable operands
            postfix_str = postfix_str + entry
        elif ord(entry) >= 97 and ord(entry) <= 122:    # variable operands contd
            postfix_str = postfix_str + entry
        elif ord(entry) != 32 and ord(entry) != 40 and ord(entry) != 41:             
            postfix_str = operation_logic(postfix_str, op_stack, entry)
        elif ord(entry) == 40:
            op_stack.append(entry)
        elif ord(entry) == 41:
            postfix_str = right_parens_logic(postfix_str, op_stack, entry)
    for operation in op_stack:
        postfix_str = postfix_str + operation 

    return postfix_str

# decides what to do with operations encountered during traversal
def operation_logic(postfix_str, op_stack, entry): 
    left_parens_index, left_parens_count = get_left_parens_index(op_stack)                      
    if len(op_stack) > 0:
        for operation in op_stack:
            if op_stack.index(operation) > left_parens_index or left_parens_count == 0:
                if expr_encoding(entry) > expr_encoding(operation):
                    postfix_str = postfix_str + op_stack.pop() 
        op_stack.append(entry) 
    else:
        op_stack.append(entry)
    return postfix_str

# logic that handles right parentheses - empties stack from right to left
def right_parens_logic(postfix_str, op_stack):
    while op_stack and op_stack[-1] != '(':
        postfix_str += op_stack.pop()
    if op_stack and op_stack[-1] == '(':
        op_stack.pop()
    return postfix_str

def get_left_parens_index(op_stack):
    index = 0
    for operation in op_stack:
        if ord(operation) == 40:
            index = op_stack[::-1].index("(")
    return (len(op_stack) - index - 1, op_stack.count("("))

# special encoding 
def expr_encoding(entry):
    index = ord(entry)

    match ord(entry): 
        case 45:      # subtraction 
            return 5       
        case 43:      # addition
            return 4
        case 47:      # division
            return 3
        case 42:      # multiplication
            return 2
        case 61:      # equals sign
            return 0
        case 94:      # exponentiation
            return -1
        case _:
            return None
    
print(infix_to_postfix_expression("(1+x)^e*k-(3-2*4)"))