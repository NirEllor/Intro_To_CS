#############################################################
# FILE : largest_and_smallest.py
# WRITER : Nir Ellor Waizner , ellorw.nir , 323816678
# EXERCISE : intro2cs2 ex2 2023
# DESCRIPTION: This program contains two functions dealing with finding maximum and minimum.
#############################################################

def largest_and_smallest(num1, num2, num3):
    """ This function calculates the maximum number and minimum number from 3 given numbers """
    if num1 >= num2:
        if num1 >= num3:
            max_num = num1
        else:
            max_num = num3
    else:
        if num2 >= num3:
            max_num = num2
        else:
            max_num = num3

    if num1 <= num2:
        if num1 <= num3:
            min_num = num1
        else:
            min_num = num3
    else:
        if num2 <= num3:
            min_num = num2
        else:
            min_num = num3
    return max_num, min_num



def check_largest_and_smallest():
    """ This function checks the behavior of largest_and_smallest function """
    is_working = True
    if largest_and_smallest(17, 1, 6) != (17, 1):
        is_working = False
    if largest_and_smallest(1, 17, 6) != (17, 1):
        is_working = False
    if largest_and_smallest(1, 1, 2) != (2, 1):
        is_working = False
    if largest_and_smallest(1, 1, 1) != (1, 1): # The largest and the smallest are equal
        is_working = False
    if largest_and_smallest(1.0, 1, 2) != (2, 1.0):
        # 1 and 1.0 have different types, suppose to take the first parameter entered
        is_working = False
    if is_working:
        return True
    else:
        return False

