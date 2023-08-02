#############################################################
# FILE : ex3.py
# WRITER : Nir Ellor Waizner , ellorw.nir , 323816678
# EXERCISE : intro2cs2 ex3 2023
# DESCRIPTION: This program mostly contains advanced mathematics functions dealing with calculus and linear algebra.
#############################################################

ZERO = "0"
NOTHING = ""

def input_list():
    """ This function returns a list of all the numbers the user sent and their sum as a final element in the list"""
    lst = []
    user_input = input()
    if user_input == ZERO:
        lst.append(0)
    else:
        sum_num = 0
        while user_input != NOTHING:
            num_input = float(user_input)
            sum_num += num_input
            lst.append(num_input)
            user_input = input()
        lst.append(sum_num)
    return lst


def inner_product(vec_1, vec_2):
    """ This function calculating the inner product of two vectors """
    product_sum = 0
    length_v1 = len(vec_1)
    length_v2 = len(vec_2)
    if length_v1 == 0 and length_v2 == 0:
        return 0
    if length_v1 != length_v2:
        return None
    for i in range(length_v1):
            product = vec_1[i] * vec_2[i]
            product_sum += product
    return product_sum



def ascending_sequence(sequence):
    """ This functions determines whether a sequence is ascending"""
    is_ascending = True
    for i in range(1, len(sequence)):
        if sequence[i - 1] > sequence[i]:
            is_ascending = False
    if is_ascending:
        return True
    else:
        return False


def very_ascending_sequence(sequence):
    """ This functions determines whether a sequence is very ascending"""
    is_very_ascending = True
    for i in range(1, len(sequence)):
        if sequence[i - 1] >= sequence[i]:
            is_very_ascending = False
    if is_very_ascending:
        return True
    else:
        return False


def descending_sequence(sequence):
    """ This functions determines whether a sequence is descending"""
    is_descending = True
    for i in range(1, len(sequence)):
        if sequence[i - 1] < sequence[i]:
            is_descending = False
    if is_descending:
        return True
    else:
        return False


def very_descending_sequence(sequence):
    """ This functions determines whether a sequence is very descending"""
    is_very_ascending = True
    for i in range(1, len(sequence)):
        if sequence[i - 1] <= sequence[i]:
            is_very_ascending = False
    if is_very_ascending:
        return True
    else:
        return False



def sequence_monotonicity(sequence):
    """ This functions determines whether a sequence is has a certain type of monotonicity"""
    if len(sequence) <= 1:
        return [True, True, True, True]
    lst = []
    first_scenario = ascending_sequence(sequence)
    second_scenario = very_ascending_sequence(sequence)
    third_scenario = descending_sequence(sequence)
    fourth_scenario = very_descending_sequence(sequence)
    lst.append(first_scenario)
    lst.append(second_scenario)
    lst.append(third_scenario)
    lst.append(fourth_scenario)
    return lst


def monotonicity_inverse(def_bool):
    """ This functions returns an example of a sequence, based on certain type of monotonicity"""
    if def_bool == [True, True, False, False]:
        return [1, 2, 3, 4]
    elif def_bool == [False, False, True, True]:
        return [4, 3, 2, 1]
    elif def_bool == [True, False, False, False]:
        return [1, 1, 2, 3]
    elif def_bool == [False, False, True, False]:
        return [3, 3, 2, 1]
    elif def_bool == [True, False, True, False]:
        return [1, 1, 1, 1]
    elif def_bool == [False, False, False, False]:
        return [1, 7, -2, 1]
    else:
        return None



def convolve(mat):
    """ This functions returns a matrix after the convolution operation being done on it"""
    if len(mat) == 0:
        return None
    else:
        start_row = 0
        end_row = 2
        start_column = 0
        end_column = 2

        matrix_table = []
        matrix_row = []

        while end_row < len(mat):
            sum_matrix_row = 0
            for i in range(start_row, end_row + 1):
                for j in range(start_column, end_column + 1):
                        sum_matrix_row += mat[i][j]

            start_column += 1
            end_column += 1
            matrix_row.append(sum_matrix_row)

            if end_column == len(mat[0]):
                start_row += 1
                end_row += 1
                start_column = 0
                end_column = 2

                matrix_table.append(matrix_row)
                matrix_row = []

        return matrix_table


def sum_of_vectors(vec_lst):
    """ This functions calculates the sum of vectors"""
    if len(vec_lst) == 0:
        return None
    vector_solution = []
    index = 0
    sum_num = 0
    while index < len(vec_lst[0]):
        for lst in vec_lst:
            if len(lst) == 0:
                return None
            sum_num += lst[index]
        vector_solution.append(sum_num)
        index += 1
        sum_num = 0
    return vector_solution


def num_of_orthogonal(vectors):
    """ This functions determines the number of orthogonal pairs, without repeats"""
    cnt_perpendicular = 0
    used_pairs = []
    for j in range(len(vectors)):
        for i in range(len(vectors)):
            pair = [i, j]
            pair_oppose = pair[::-1]
            if inner_product(vectors[i], vectors[j]) == 0 and pair not in used_pairs and pair_oppose not in used_pairs:
                if i != j:
                    used_pairs.append(pair)
                    cnt_perpendicular += 1
    return cnt_perpendicular
