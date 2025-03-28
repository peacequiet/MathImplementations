def forward_elim(matrix):                                       # full forward elim algorithm
    length = len(matrix)
    for i, val in enumerate(matrix):                            # convert entries to float for division to work right
        for j, val in enumerate(matrix[i]):
            matrix[i][j] = float(matrix[i][j])
    for i, val in enumerate(matrix):
        if i < length:
            swap(matrix, i, i)
            const_cancel(matrix, i, i)

def swap(matrix, row, column):                                  # searches for leading row in matrix and swaps it with first row
    row_1_swap = None
    row_2_swap = None

    for i, val in enumerate(matrix):
        if i >= row:
            if val[column] == 0 and row_1_swap is None:
                row_1_swap = i
            elif val[column] != 0 and row_2_swap is None and row_1_swap is not None:
                row_2_swap = i

    if row_1_swap is not None and row_2_swap is not None:
        matrix[row_1_swap], matrix[row_2_swap] = matrix[row_2_swap], matrix[row_1_swap]
        
def mul_const(row_1, row_2, column):                            # determines proportion between rows 
    multiple = row_2[column] / row_1[column]
    return multiple

def const_cancel(matrix, row, column):                          # cancels entries in all rows below a given column
    dummy_row = None
    for i, val in enumerate(matrix):                            # iterate through rows (val)
        if i > (row) and val[column] != 0:                      # skip leading row to find row with a nonzero value at index = column
            mul = mul_const(matrix[row], matrix[i], column)     # find the proportion to multiply leading row by        
            dummy_row = [j * mul for j in matrix[row]]          # new row made to subtract from nonzero row    
            for j, value in enumerate(matrix[i]):               # iterate through values
                matrix[i][j] = matrix[i][j] - dummy_row[j]      # subtracts dummy row (mul * R_1) from target row (R_i) and replace target row (R_i) 
    return

array = [[1, 1, -3], 
         [-2, 0, 4], 
         [6, 2, -16]]

forward_elim(array)
print(array)
# matrix = [[1, -2, 1, 4], 
#           [0, 1, 2, -5],
#           [1, 1, 3, -7]]

# matrix_2 = [[0, 1, 2, 7 , 9], 
#           [4, -1, 6, 9, 11], 
#           [8, 2, 3, -5, -30],
#           [2, 0, 5, 4, 9],
#           [8, 6, 2, 2, 5]]

# swap(matrix, 0, 0)
# const_cancel(matrix, 0, 0)
# swap(matrix, 1, 1)
# const_cancel(matrix, 1, 1)
# forward_elim(matrix)
# print(matrix)