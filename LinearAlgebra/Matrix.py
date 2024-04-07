import random

# TODO: implement a way to turn a given list into a Matrix object
class Matrix:
    def __init__(self, rows, columns):
        self.matrix = [None] * rows
        for i, val in enumerate(self.matrix):
            self.matrix[i] = [0] * columns
        self.size = str(rows) + " * " + str(columns)                                # holds string representing size
        self.rows = rows
        self.columns = columns
    
    def copy(self):
        mtx_copy = Matrix(self.rows, self.columns)
        mtx_copy.matrix = [row[:] for row in self.matrix]                           # deep copy 
        return mtx_copy
    
    def randomize(self, min, max):
        for i, val in enumerate(self.matrix):
            for j, val in enumerate(self.matrix[i]):
                self.matrix[i][j] = random.randint(min, max)
        return
    
    def find_columns(array):
        columns = 0
        for row in array:
            if len(row) > columns:
                columns = len(row)
        return columns

    def array_to_matrix(array, is_jagged):                                          # turns input array to matrix
        if is_jagged:
            rows = len(array)
            columns = Matrix.find_columns(array)
        else:
            rows = len(array)
            columns = len(array[0])

        matrix = Matrix(rows, columns)
        for i, val in enumerate(array):
            for j, val in enumerate(array[i]):
                matrix.matrix[i][j] = array[i][j]

        return matrix

    def __str__(self):
        return str(self.matrix)

def matrix_add(mtx_1, mtx_2):                                                       # adds matrices of the same size 
    if mtx_1.size == mtx_2.size:                                                    # check to ensure the matrices are actually the same size
        mtx_3 = Matrix(mtx_1.rows, mtx_1.columns)
        for i, val in enumerate(mtx_1.matrix):
            for j, val in enumerate(mtx_1.matrix[i]):
                mtx_3.matrix[i][j] = mtx_1.matrix[i][j] + mtx_2.matrix[i][j]        # adds elements together iteratively
    return mtx_3                                                                    # return type = Matrix

def scalar_mul(s, mtx):
    mtx_return = mtx.copy()
    for i, val in enumerate(mtx_return.matrix):
        for j, val in enumerate(mtx_return.matrix[i]):
            mtx_return.matrix[i][j] = s * mtx_return.matrix[i][j]
    return mtx_return                                                   # return type = Matrix

def matrix_mul_sum(mtx_1, mtx_2, row, column, size):                        # returns integer total for entry in mtx_3_i_j
    row_mul = mtx_1.matrix[row]                                             # create two vectors, one representing row, one representing columns
    col_mul = [0] * size                                                    

    for i in range(size):
        col_mul[i] = mtx_2.matrix[i][column]

    total_mul = [row_mul[i] * col_mul[i] for i, val in enumerate(row_mul)]  # multiply vectors together
    total = sum(total_mul)                                                  # calculate their sum
    
    return total                                        

def matrix_mul(mtx_1, mtx_2):
    if mtx_1.columns == mtx_2.rows:
        mtx_3 = Matrix(mtx_1.rows, mtx_2.columns)
        for i, val in enumerate(mtx_3.matrix):
            for j, val in enumerate(mtx_3.matrix[i]):
                mtx_3.matrix[i][j] = matrix_mul_sum(mtx_1, mtx_2, i, j, mtx_1.columns)
    return mtx_3

matrix_1 = Matrix(3, 3)
matrix_1.randomize(-10, 10)
matrix_2 = Matrix(3, 3)
matrix_2.randomize(-10, 10)
matrix_3 = matrix_add(matrix_1, matrix_2)
matrix_4 = scalar_mul(3, matrix_3)

array   = [[3, 4, 5], 
           [3, 6, 9], 
           [3, 9, 27]]

array_2 = [[3, 4, 5], 
           [3, 6, 9], 
           [3, 9, 27]]

matrix_5 = Matrix.array_to_matrix(array, False)
matrix_6 = Matrix.array_to_matrix(array_2, False)


# print(matrix_1.size == matrix_2.size)

# print(matrix_5)
# print(matrix_6)

# print(matrix_mul_sum(matrix_5, matrix_6, 0, 0, 3))
print(matrix_mul(matrix_5, matrix_6))

