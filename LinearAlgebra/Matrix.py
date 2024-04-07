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
    
    def __str__(self):
        return str(self.matrix)
    
    def copy(self):
        mtx_copy = Matrix(self.rows, self.columns)
        mtx_copy.matrix = [row[:] for row in self.matrix]                           # deep copy 
        return mtx_copy
    
    def randomize(self, min, max):
        for i, val in enumerate(self.matrix):
            for j, val in enumerate(self.matrix[i]):
                self.matrix[i][j] = random.randint(min, max)
        return

def matrix_add(mtx_1, mtx_2):                                                       # adds matrices of the same size 
    if mtx_1.size == mtx_2.size:                                                    # check to ensure the matrices are actually the same size
        mtx_3 = Matrix(3, 3)
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


matrix_1 = Matrix(3, 3)
matrix_1.randomize(-10, 10)
matrix_2 = Matrix(3, 3)
matrix_2.randomize(-10, 10)
matrix_3 = matrix_add(matrix_1, matrix_2)
matrix_4 = scalar_mul(3, matrix_3)


print(matrix_1.size == matrix_2.size)

print(matrix_3)

print(matrix_4)