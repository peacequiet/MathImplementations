# Tokenizes the expression into numbers, operators, functions, and parentheses

# TODO: negative terms
# we can do this by creating another if statement enclosing the current one
# and adjusting string ranges
def expression_tokenizer(expression):
    expression_tokens = []
    i = 0
    expression.replace(" ", "")
    while i < len(expression):
        if expression[i:i+3] in ("sin", "cos", "tan"):
            expression_tokens.append(expression[i:i+3])
            i += 3
        elif (expression[i] == "-" 
              and (expression[i-1] in "+-*/^(" or i == 0)):
            expression_tokens.append("~")               # replace unary subtraction with squiggly operator
            i += 1 
        elif expression[i:i+2] == "pi":
            expression_tokens.append("pi")
            i += 2
        elif expression[i] == " ":
            i += 1
        else:
            expression_tokens.append(expression[i])
            i += 1
    return expression_tokens

# Encodes the expression tokens into categories
def expr_encoding(token):
    if token in ("sin", "cos", "tan"):
        return "func"
    elif token == "pi":
        return "num"
    elif token.isalnum():
        return "num"
    elif token == "(":
        return "lp"
    elif token == ")":
        return "rp"
    elif token in "+-*/^~":
        return "op"
    else:
        return None

# Encodes the operators into precedence levels
def operator_encoding(token):
    if token in ("sin", "cos", "tan"):
        return 4
    elif token == "^":
        return 3
    elif token in "*/":
        return 2
    elif token in "+-~":
        return 1
    else:
        return 0

# Converts an infix expression to a postfix expression using Shunting Yard
def infix_to_postfix_expression(expression):
    postfix_list = []
    op_stack = []
    for token in expression:
        token_type = expr_encoding(token)
        if token_type == "num":
            postfix_list.append(token)
        elif token_type == "func":
            op_stack.append(token)
        elif token_type == "op":
            while op_stack and operator_encoding(op_stack[-1]) >= operator_encoding(token): 
                postfix_list.append(op_stack.pop())
            op_stack.append(token)
        elif token_type == "lp":
            op_stack.append(token)
        elif token_type == "rp":
            while op_stack and op_stack[-1] != "(":
                postfix_list.append(op_stack.pop())
            op_stack.pop()  
            if op_stack and expr_encoding(op_stack[-1]) == "func":
                postfix_list.append(op_stack.pop())
    while op_stack:
        postfix_list.append(op_stack.pop())
    return postfix_list

# Examples
tokens = expression_tokenizer("-sin(x) + 1 + 2 * tan(pi * x)")
postfix_expression = infix_to_postfix_expression(tokens)
print(tokens)
print(postfix_expression)
