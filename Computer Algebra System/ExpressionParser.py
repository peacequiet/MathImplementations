# Tokenizes the expression into numbers, operators, functions, and parentheses
def expression_tokenizer(expression):
    expression_tokens = []
    i = 0
    expression = expression.replace(" ", "")
    length = len(expression)
    while i < length:
        if expression[i:i+3] in ("sin", "cos", "tan"):
            expression_tokens.append(expression[i:i+3])
            i += 3
        elif (expression[i] == "-" 
              and expression[i+1].isnumeric()
              and not expression[i-1].isalnum()):
            i = scan_for_digits(i, 1, length, expression, expression_tokens)
        elif (expression[i] == "-" 
              and (expression[i-1] in "+-*/^(" or i == 0)):
            expression_tokens.append("~")                               # replace unary negation with squiggly operator
            i += 1 
        elif expression[i:i+2] == "pi":
            expression_tokens.append("pi")
            i += 2
        elif expression[i].isnumeric():
            i = scan_for_digits(i, 0, length, expression, expression_tokens)
        elif expression[i] == " ":
            i += 1
        else:
            expression_tokens.append(expression[i])
            i += 1
    return expression_tokens

# gets digits of a multidigit number
def scan_for_digits(i, j, length, expression, expression_tokens):
    while i + j < length and expression[i+j].isnumeric():
        j +=1
    expression_tokens.append(expression[i:i+j])
    return (i + j)

# Encodes the expression tokens into categories
# TODO: special encoding for variables
def expr_encoding(token):
    if token in ("sin", "cos", "tan"):
        return "func"
    elif token == "pi":
        return "num"
    elif token == "e":
        return "num"
    elif token[0].isnumeric():
        return "num"
    elif len(token) >= 2 and token[0] == "-":
        if token[1].isnumeric():
            return "num"
    elif token.isalpha():
        return "var"
    elif token == "(":
        return "lp"
    elif token == ")":
        return "rp"
    elif token in "+-*/^~=":
        return "op"
    else:
        raise Exception("Unknown symbol: " + token)

# Encodes the operators into precedence levels
def operator_encoding(token):
    if token in ("sin", "cos", "tan"):
        return 4
    elif token == "^":
        return 3
    elif token in "*/~":
        return 2
    elif token in "+-":
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
        if token_type == "var":
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

# takes infix string expression, converts to postfix
def expression_parser(expression):
    tokens = expression_tokenizer(expression)
    parse_exceptions(tokens)
    postfix_expression = infix_to_postfix_expression(tokens)
    return postfix_expression

# PARSE ERRORS
#catches too many parentheses
def parens_error_catcher(tokens):
    lp_num = tokens.count("(")
    rp_num = tokens.count(")")
    if (lp_num + rp_num) % 2 != 0:
        raise Exception("PARSE ERROR: Expression has mismatched parentheses")

def op_error_catcher(tokens, length):
    if expr_encoding(tokens[0]) == "op" and tokens[0] != "~":
         raise Exception("PARSE ERROR: Cannot start expression with binary operator")
    for i, token in enumerate(tokens):
        if (i < length - 1
            and expr_encoding(token) == "op" 
            and expr_encoding(tokens[i + 1]) == "op"):
            raise Exception("PARSE ERROR: Neighboring operators at " + str(i) + ", " + str(i + 1))
        
def term_error_catcher(tokens, length):
    for i, token in enumerate(tokens):
        if (i < length - 1
            and expr_encoding(token) in ["num", "var", "func"]
            and expr_encoding(tokens[i + 1]) not in ["lp", "rp", "op"]):
            raise Exception("PARSE ERROR: Neighboring terms at " + str(i) + ", " + str(i + 1))

def parse_exceptions(tokens):
    length = len(tokens)
    parens_error_catcher(tokens)
    op_error_catcher(tokens, length)
    term_error_catcher(tokens, length)


# examples
#print(expression_parser("2 + 6 ^ 70"))
# tokens = expression_tokenizer("-sin(x) + 1 - 20 * tan(pi * x)")
# postfix_expression = infix_to_postfix_expression(tokens)
# # parens_error_catcher(tokens)
# print(tokens)
# print(postfix_expression)