#############################################################
# FILE : shapes.py
# WRITER : Nir Ellor Waizner , ellorw.nir , 323816678
# EXERCISE : intro2cs2 ex2 2023
# DESCRIPTION: This program contains functions dealing with shapes and their area.
# WEB PAGES I USED:
# https://docs.python.org/3/library/math.html
#############################################################

import math

CIRCLE = "1"
RECTANGLE = "2"
TRIANGLE = "3"


def circle(radius):
    """ This function calculates the area of a circle, given the radius as an argument"""
    return pow(radius, 2) * math.pi


def rectangle(length, width):
    """ This function calculates the area of a rectangle, given the length and width as an argument"""
    return length * width


def triangle(size):
    """ This function calculates the area of an equilateral triangle, given one of the edges as an argument"""
    return pow(size, 2) * math.sqrt(3) / 4


def shape_area():
    """ This function calculates the area of a shape chosen by the user, given relevant details about the shape
    from the user"""
    user_input = input("Choose shape (1=circle, 2=rectangle, 3=triangle): ")

    if user_input not in [CIRCLE, RECTANGLE, TRIANGLE]:
        return None

    elif user_input == CIRCLE:
        radius = float(input())
        return circle(radius)

    elif user_input == RECTANGLE:
        first_size = float(input())
        second_size = float(input())
        return rectangle(first_size, second_size)

    elif user_input == TRIANGLE:
        triangle_size = float(input())
        return triangle(triangle_size)

