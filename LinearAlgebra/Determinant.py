from Matrix import *

class Determinant:
    def det_three(matrix):
        term_1 = matrix.matrix[0][0] * matrix.matrix[1][1] * matrix.matrix[2][2]
        term_2 = matrix.matrix[0][1] * matrix.matrix[1][2] * matrix.matrix[2][0]
        term_3 = matrix.matrix[0][2] * matrix.matrix[1][0] * matrix.matrix[2][1]
        term_4 = matrix.matrix[0][2] * matrix.matrix[1][1] * matrix.matrix[2][0]
        term_5 = matrix.matrix[0][0] * matrix.matrix[1][2] * matrix.matrix[2][1]
        term_6 = matrix.matrix[0][1] * matrix.matrix[1][0] * matrix.matrix[2][2]
        return term_1 + term_2 + term_3 - term_4 - term_5 - term_6
