#################################################################
# FILE : car.py
# WRITER : Nir Ellor Waizner , ellorw.nir , 323816678
# EXERCISE : intro 2cs ex9 2022-2023
# DESCRIPTION: A program that operates the Car class in the rush hour's game
#################################################################
##############################################################################

class Car:
    """
    This class contains the methods and attributes each car in the rush hour game should have
    """
    UP = "u"
    DOWN = "d"
    LEFT = "l"
    RIGHT = "r"
    INVALID = "Invalid move"
    VERTICAL = 0
    HORIZONTAL = 1

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # Note that this function is required in your Car implementation.
        # implement your code and erase the "pass"
        self.name = name
        self.length = length
        self.location = location
        self.orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        lst = [self.location]
        if self.orientation == Car.VERTICAL:  # Vertical
            for i in range(1, self.length - 1 + 1):
                lst.append((self.location[0] + i, self.location[1]))
        elif self.orientation == Car.HORIZONTAL:  # horizontal
            for i in range(1, self.length - 1 + 1):
                lst.append((self.location[0], self.location[1] + i))
        return lst

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        # For this car type, keys are from 'udrl'
        # The keys for vertical cars are 'u' and 'd'.
        # The keys for horizontal cars are 'l' and 'r'.
        # You may choose appropriate strings.
        # implement your code and erase the "pass"
        # The dictionary returned should look something like this:
        # result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        # A car returning this dictionary supports the commands 'f','d','a'.
        # implement your code and erase the "pass"
        if self.orientation == Car.VERTICAL:
            result_vertical = {Car.UP: "Moving the car one step up", Car.DOWN: "Moving the car one step down"}
            return result_vertical
        if self.orientation == Car.HORIZONTAL:
            result_horizontal = {Car.RIGHT: "Moving the car one step right", Car.LEFT: "Moving the car one step left"}
            return result_horizontal

    def movement_requirements(self, move_key):
        """ 
        :param move_key: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        if move_key == Car.UP:
            x = self.car_coordinates()[0][0] - 1
            y = self.car_coordinates()[0][1]
            return [(x, y)]
        if move_key == Car.DOWN:
            x = self.car_coordinates()[-1][0] + 1
            y = self.car_coordinates()[-1][1]
            return [(x, y)]
        if move_key == Car.LEFT:
            x = self.car_coordinates()[0][0]
            y = self.car_coordinates()[0][1] - 1
            return [(x, y)]
        if move_key == Car.RIGHT:
            x = self.car_coordinates()[-1][0]
            y = self.car_coordinates()[-1][1] + 1
            return [(x, y)]
        return Car.INVALID

    def move(self, move_key):
        """ 
        :param move_key: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if move_key == Car.UP or move_key == Car.DOWN:
            if self.orientation != Car.VERTICAL:
                return False

            if move_key == Car.UP:
                self.location = (self.location[0] - 1, self.location[1])
                return True
            if move_key == Car.DOWN:
                self.location = (self.location[0] + 1, self.location[1])
                return True

        if move_key == Car.RIGHT or move_key == Car.LEFT:
            if self.orientation != Car.HORIZONTAL:
                return False
            if move_key == Car.RIGHT:
                self.location = (self.location[0], self.location[1] + 1)
                return True
            if move_key == Car.LEFT:
                self.location = (self.location[0], self.location[1] - 1)
                return True
        return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.name
