#############################################################
# FILE : math_print.py
# WRITER : Nir Ellor Waizner , ellorw.nir , 323816678
# EXERCISE : intro2cs2 ex1 2023
# DESCRIPTION: A simple simple program which defines functions, assisted by functions from the math module
# the standard output (screen).
# WEB PAGES I USED:
# https://docs.python.org/3/library/math.html
#############################################################

import math

def golden_ratio():
    """This function prints the value of the golden ratio"""
    print(((1 + math.sqrt(5)) / 2))


def six_squared():
    """This function prints 6 to the power of 2"""
    print(6 ** 2)


def hypotenuse():
    """This function prints the length of the permit in a right triangle, having edges of 5 and 12"""
    print(math.sqrt((12 ** 2) + (5 ** 2)))


def pi():
    """This function prints the value of pi"""
    print(math.pi)


def e():
    """This function prints the value of e"""
    print(math.e)


def squares_area():
    """This function prints the area of squares with edges of 1 to 10"""
    print(1 ** 2, 2 ** 2, 3 ** 2, 4 ** 2, 5 ** 2, 6 ** 2, 7 ** 2, 8 ** 2, 9 ** 2, 10 ** 2)


if __name__ == '__main__':
    golden_ratio()
    six_squared()
    hypotenuse()
    pi()
    e()
    squares_area()
