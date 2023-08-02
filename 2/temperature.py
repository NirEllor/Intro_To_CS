#############################################################
# FILE : temperature.py
# WRITER : Nir Ellor Waizner , ellorw.nir , 323816678
# EXERCISE :intro2cs2 ex2 2023
# DESCRIPTION: This program contains a function dealing with temperatures.
# WEB PAGES I USED:
# https://docs.python.org/3/library/math.html
#############################################################

def is_vormir_safe(max_tem, day1, day2, day3):
    """ This function determines whether if at least 2 days from 3 had higher temprature than a given max temprature
     as an argument"""
    cnt = 0
    if day1 > max_tem:
        cnt += 1
    if day2 > max_tem:
        cnt += 1
    if day3 > max_tem:
        cnt += 1
    if cnt >= 2:
        return True
    else:
        return False


