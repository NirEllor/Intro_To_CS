#############################################################
# FILE : hello_turtle.py
# WRITER : Nir Ellor Waizner , ellorw.nir , 323816678
# EXERCISE : intro2cs2 ex1 2023
# DESCRIPTION: A simple program which defines functions in order to
# draw a fleet, using the turtule module
#############################################################

import turtle

def draw_triangle():
    """ This function will draw a triangle"""
    turtle.forward(45)
    turtle.right(120)
    turtle.forward(45)
    turtle.right(120)
    turtle.forward(45)
    turtle.right(120)


def draw_sail():
    """This function will draw a sail, assisted by draw_triangle function"""
    turtle.left(90)
    turtle.forward(50)
    turtle.right(150)
    draw_triangle()
    turtle.right(30)
    turtle.up()
    turtle.forward(50)
    turtle.down()
    turtle.left(90)


def draw_ship():
    """This function will draw a ship, assisted by draw_triangle and draw_sail functions"""
    turtle.forward(50)
    draw_sail()
    turtle.forward(50)
    draw_sail()
    turtle.forward(50)
    draw_sail()
    turtle.forward(50)
    turtle.right(120)
    turtle.forward(20)
    turtle.right(60)
    turtle.forward(180)
    turtle.right(60)
    turtle.forward(20)
    turtle.right(120)


def draw_fleet():
    """This function will draw a ship, assisted by all the functions above"""
    turtle.up()
    turtle.forward(120)
    turtle.down()
    draw_ship()
    turtle.up()
    turtle.left(180)
    turtle.forward(300)
    turtle.right(180)
    turtle.down()
    draw_ship()
    turtle.up()
    turtle.forward(300)


if __name__ == '__main__':
    draw_fleet()
    turtle.done()
