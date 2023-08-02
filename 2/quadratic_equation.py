#############################################################
# FILE : quadratic_equation.py
# WRITER : Nir Ellor Waizner , ellorw.nir , 323816678
# EXERCISE : intro2cs2 ex2 2023
# DESCRIPTION: This program contains functions dealing with quadratic equations.
# WEB PAGES I USED:
# https://docs.python.org/3/library/math.html
# https://docs.python.org/3.4/library/stdtypes.html#str.split
# https://he.wikipedia.org
#############################################################

import math


def quadratic_equation(a, b, c):
    """ This function calculates the solution, if exists, of a quadratic equation, given the 3 coefficients"""
    if pow(b, 2) - (4 * a * c) > 0:
        x1 = (-b + math.sqrt(pow(b, 2) - 4 * a * c)) / (2 * a)
        x2 = (-b - math.sqrt(pow(b, 2) - 4 * a * c)) / (2 * a)
        return x1, x2
    elif pow(b, 2) - (4 * a * c) == 0:
        x1 = -b / (2 * a)
        return x1, None
    else:
        return None, None


def quadratic_equation_user_input():
    """ This function uses the quadratic_equation function, by having the 3 coefficients of the quadratic equation as
     an input from the user"""
    user_input = input("Insert coefficients a, b, and c: ")
    parameters = user_input.split(" ")
    par_0 = float(parameters[0])
    par_1 = float(parameters[1])
    par_2 = float(parameters[2])
    if par_0 == 0:
        print("The parameter 'a' may not equal 0")
    else:
        solution = quadratic_equation(par_0, par_1, par_2)
        if len(solution) == 2 and None not in solution and par_0 != 0:
            x, y = quadratic_equation(par_0, par_1, par_2)
            print("The equation has 2 solutions: {} and {}".format(x, y))
        elif len(solution) == 2 and solution.count(None) == 1 and par_0 != 0:
            x, y = quadratic_equation(par_0, par_1, par_2)
            print("The equation has 1 solution: {}".format(x))
        elif len(solution) == 2 and solution.count(None) == 2 and par_0 != 0:
            print("The equation has no solutions")


