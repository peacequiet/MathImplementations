from ExpressionParser import *
# for sorting commutative trees
def encoding_of_operands(token):
    if expr_encoding(token) == "func":
        return 2
    elif expr_encoding(token) == "var":
        return 1
    elif expr_encoding(token) == "num":
        return 0
    else:
        return 3

def merge_sort(array):
    if len(array) < 2:
        return array

    left = []
    right = []
    for i, x in enumerate(array):
        if i < len(array) / 2:
            left.append(x)
        else:
            right.append(x)
    
    left = merge_sort(left)
    right = merge_sort(right)

    return merge(left, right)

# merge sort logic
def merge(left, right):
    result = []

    while left and right:
        if (encoding_of_operands(left[0].token) 
            <= encoding_of_operands(right[0].token)):  # encoding check
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))

    while left:
        result.append(left.pop(0))
    while right:
        result.append(right.pop(0))
    
    return result

# TODO: merge sort for alphabetical and numeric ordering