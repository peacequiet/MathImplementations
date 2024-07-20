# TODO: make tokenized expression agree with postfix expression
# TODO: implement Shunting Yard algo


# we should only accept trig expressions with parens
# tokenizer online
def expression_tokenizer(expression):
    expression_tokens = []
    i = 0
    while i < len(expression):
        if expression[i:i+3] == "sin":
            expression_tokens.append("sin")
            i += 3  # Skip next two characters
        elif expression[i:i+3] == "cos":
            expression_tokens.append("cos")
            i += 3  # Skip next two characters
        elif expression[i:i+3] == "tan":
            expression_tokens.append("tan")
            i += 3  # Skip next two characters
        elif expression[i:i+2] == "pi":
            expression_tokens.append("pi")
            i += 2  # Skip next character
        elif expression[i] == " ":
            i += 1
        else:
            expression_tokens.append(expression[i])
            i += 1
    return expression_tokens


tokens = expression_tokenizer("sin(x) + 1 + 2 * tan(pi * x)")
# translates our expression from infix to postfix notation 
# to prepare for tree construction.
# TODO: instead of returning a string, make it take and return a list of strings
def infix_to_postfix_expression(expression):   
    postfix_str = ""
    visited_str = ""
    op_stack = []
    for token in expression:
        if ord(token) == 32:
            expression.replace(" ", "")
    for token in expression:
        visited_str = visited_str + token
        if ord(token) >= 48 and ord(token) <= 57:       # numerical operands
            postfix_str = postfix_str + token
        elif ord(token) >= 65 and ord(token) <= 90:     # variable operands
            postfix_str = postfix_str + token
        elif ord(token) >= 97 and ord(token) <= 122:    # variable operands contd
            postfix_str = postfix_str + token
        elif ord(token) != 32 and ord(token) != 40 and ord(token) != 41:             
            postfix_str = operation_logic(postfix_str, op_stack, token)
        elif ord(token) == 40:
            op_stack.append(token)
        elif ord(token) == 41:
            postfix_str = right_parens_logic(postfix_str, op_stack)
    for operation in op_stack:
        postfix_str = postfix_str + operation 

    return postfix_str

# decides what to do with operations encountered during traversal
def operation_logic(postfix_str, op_stack, token): 
    left_parens_index, left_parens_count = get_left_parens_index(op_stack)                      
    if len(op_stack) > 0:
        for operation in op_stack:
            if op_stack.index(operation) > left_parens_index or left_parens_count == 0:
                if operator_encoding(token) > operator_encoding(operation):
                    postfix_str = postfix_str + op_stack.pop() 
        op_stack.append(token) 
    else:
        op_stack.append(token)
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


# experimental encoding
def expr_encoding(token):

    match token: 
        case token if (token == "sin" 
                       or token == "cos" 
                       or token == "tan"):
            return "func"
        case "pi":
            return "num"
        case token if (ord(token) >= 49 and ord(token) <= 57
                       or ord(token) >= 65 and ord(token) <= 90
                       or ord(token) >= 97 and ord(token) <= 122):
            return "num"
        case token if token == "(":
            return "lp"
        case token if token == ")":
            return "rp"
        case token if ord(token) == 45:      # subtraction 
            return "operator"       
        case token if ord(token) == 43:      # addition
            return "operator"       
        case token if ord(token) == 47:      # division
            return "operator"       
        case token if ord(token) == 42:      # multiplication
            return "operator"
        case token if ord(token) == 61:      # equals sign
            return "operator"
        case token if ord(token) == 94:      # exponentiation
            return "operator"
        case _:
            return None

# special encoding 
# TODO : make encoding compatible with tokens instead of single chars
def operator_encoding(token):
    match token: 
        case token if (token == "sin" 
                       or token == "cos" 
                       or token == "tan"):
            return 0
        case token if ord(token) == 45:      # subtraction 
            return 5       
        case token if ord(token) == 43:      # addition
            return 4
        case token if ord(token) == 47:      # division
            return 3
        case token if ord(token) == 42:      # multiplication
            return 2
        case token if ord(token) == 61:      # equals sign
            return 0
        case token if ord(token) == 94:      # exponentiation
            return -1
        case _:
            return None
    
for token in tokens:
    print(expr_encoding(token))

# print(infix_to_postfix_expression("( 1 + x ) ^ e * k - ( 3 - 2 * 4 )"))