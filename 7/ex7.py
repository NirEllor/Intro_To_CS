#################################################################
# FILE : ex7.py
# WRITER : Nir Ellor Waizner , ellorw.nir , 323816678
# EXERCISE : intro 2cs ex7 2022-2023
# DESCRIPTION: A program that contains recursive functions
#################################################################
##############################################################################
#                                   Imports                                  #
##############################################################################
from ex7_helper import *
##############################################################################
#                                 FUNCTIONS                                  #


def mult(x, y):
    """This function implements multiplication in O(n) run time complexity"""
    if y == 1:
        return x
    return add(x, mult(x, subtract_1(y)))


def is_even(n):
    """This nuber checks if a number is even or not"""
    if n == 0:
        return True
    if n < 0:
        return False
    return is_even(subtract_1(subtract_1(n)))


def log_mult(x, y):
    """This function implements multiplication in O(log(n)) run time complexity"""
    if y == 1:
        return x
    if not is_odd(y):
        t = log_mult(x, divide_by_2(y))
        return add(t, t)
    return add(x, log_mult(x, add(divide_by_2(y), divide_by_2(y))))


def is_power_helper(b, x):
    """ This function checks if there is a natural (or zero) number, called n, so that b ** n == x """
    if x == 1:
        return True
    if is_odd(x) != is_odd(b):
        return False
    if b == x:
        return True
    if b > x:
        return False
    if log_mult(b, log_mult(b, b)) == x:
        return True
    return is_power_helper(log_mult(b, b), x)


def is_power(b, x):
    return is_power_helper(b, x)

print(is_power(2, 3))

def reverse(s):
    """This function calls the recursive slicing function"""
    return recursive_slicing(s, 0)


def recursive_slicing(string, index):
    """This function implements the slicing method using recursion"""
    if index == len(string) - 1:
        return string[index]
    new_sliced_str = string[index]
    return append_to_end(recursive_slicing(string, index + 1), new_sliced_str)


def play_hanoi(hanoi, n, src, dest, temp):
    """This function implements the induction proof of the solution for n elements in Towers Of Hanoi game"""
    """ In case No discs were entered"""
    if n == 0:
        return
    """Induction step - move all n - 1 discs from tower 1 (src) to tower 3 (temp)"""
    play_hanoi(hanoi, n - 1, src, temp, dest)
    """Base case - Once we moved all of them, move the last remaining disc from tower 1 (src) to tower 2 (dest)"""
    hanoi.move(src, dest)
    """Move all n - 1 discs from tower 3 (temp) to tower 2 (dest), using tower 1 (src)"""
    play_hanoi(hanoi, n - 1, temp, dest, src)
    """Done!"""


lst = [0]  # A recursive technique in order to globally save the number of occurrences, so it won't be run over


def number_of_ones(n):
    """This function recursively checks occurrences of one in rach number from n down to 1, using a helper function"""
    if n == 0:
        return lst[0]
    ones_helper_n(n)
    return number_of_ones(n - 1)


def ones_helper_n(num):
    """This function checks occurrences of ones in a specific number recursively"""
    if num == 0:
        return 0
    ones_helper_n(num // 10)
    last_digit = num % 10
    if last_digit == 1:
        lst[0] += 1
        return lst[0]
    else:
        return lst[0]


def compare_2d_lists(l1, l2):
    """This function compares between two dimension lists, using recursive functions"""
    if len(l1) != len(l2):
        return False
    return compare_1d_lists(l1, l2, 0)


def compare_1d_lists(l1, l2, nested_list_index):
    """This function compares between one dimension lists, recursively"""
    if nested_list_index == len(l1):
        return True
    if len(l1[nested_list_index]) != len(l2[nested_list_index]):
        return False
    if not compare_elements(l1[nested_list_index], l2[nested_list_index], 0):
        return False
    return compare_1d_lists(l1, l2, nested_list_index + 1)


def compare_elements(lst1, lst2, index):
    """This function compares between elements of one dimension lists, recursively"""
    if index == len(lst1):
        return True
    if lst1[index] != lst2[index]:
        return False
    return compare_elements(lst1, lst2, index + 1)


def magic_list(n):
    """This function calls the magic_helper function, giving it an empty list, symbolizing zero"""
    lst1 = []
    return magic_helper(n, lst1)


def magic_helper(n, lst_magic):
    """This function recursively builds the natural numbers from zero to n, having each deep copied list
    representing a number"""
    if n == 0:
        return []
    """The recursion to the left creates internal lists, being deep copied since each list is wrapped up
    in a new list"""
    return magic_helper(n - 1, lst_magic) + [magic_helper(n - 1, lst_magic)]
