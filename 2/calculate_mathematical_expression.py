#############################################################
# FILE : calculate_mathematical_expression.py
# WRITER : Nir Ellor Waizner , ellorw.nir , 323816678
# EXERCISE : intro2cs2 ex2 2023
# DESCRIPTION: This program contains two functions dealing with calculation of mathematical expressions.
# WEB PAGES I USED:
# https://docs.python.org/3.4/library/stdtypes.html#str.split
#############################################################

def calculate_mathematical_expression(num1, num2, operation):
    """ This function calculates an operation on two numbers """
    if operation in "+-*:":
        if operation == "+":
            return num1 + num2
        elif operation == "-":
            return num1 - num2
        elif operation == "*":
            return num1 * num2
        elif operation == ":":
            return num1 / num2
    elif num2 == 0 or operation not in "+-*:":
        return None


def calculate_from_string(string):
    """ This function calculates an operation on two numbers, having the whole expression inside of a string """
    splitted = string.split(" ")
    if splitted[1] not in "+-*:" or splitted[2] == "0":
        return None
    splitted_1 = float(splitted[0])
    splitted_2 = float(splitted[2])
    return calculate_mathematical_expression(splitted_1, splitted_2, splitted[1])
