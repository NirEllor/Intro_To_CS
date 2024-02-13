#################################################################
# FILE : board.py
# WRITER : Nir Ellor Waizner , ellorw.nir , 323816678
# EXERCISE : intro 2cs ex9 2022-2023
# DESCRIPTION: A program that operates the Board class in the rush hour's game
#################################################################
##############################################################################
from car import Car


class Board:
    """
    This class manages the board of the rush hour's game, its methods and attributes.
    """
    BOARD_ROWS = 7
    BOARD_COLUMNS = 8
    SPECIAL_ROW = 3
    SPECIAL_COLUMN = 7
    EMPTY = "_"
    NOTHING = "*"
    EXIT = "E"

    def __init__(self):
        # implement your code and erase the "pass"
        # Note that this function is required in your Board implementation.
        def __create_board():
            """This function creates the general board for each game, which is 7 x 7 square with 1special column to
            the right"""
            lst_external = []
            for i in range(Board.BOARD_ROWS):
                lst_internal = []
                for j in range(Board.BOARD_COLUMNS):
                    if j != Board.BOARD_ROWS:
                        lst_internal.append(Board.EMPTY)
                    elif i != Board.SPECIAL_ROW:
                        lst_internal.append(Board.NOTHING)
                    else:
                        lst_internal.append(Board.EXIT)
                lst_external.append(lst_internal)
            return lst_external
        self.graphic_board = __create_board()
        self.cars = {}

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        # The game may assume this function returns a reasonable representation
        # of the board for printing, but may not assume details about it.
        # implement your code and erase the "pass"
        lst = []
        for i in range(Board.BOARD_ROWS):
            row = " ".join(self.graphic_board[i])
            lst.append(row)
        return "\n".join(lst)

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        # In this board, returns a list containing the cells in the square
        # from (0,0) to (6,6) and the target cell (3,7)
        lst = []
        for i in range(Board.BOARD_ROWS):
            for j in range(Board.BOARD_COLUMNS):
                if i == Board.SPECIAL_ROW or j != Board.BOARD_COLUMNS - 1:
                    tpl = (i, j)
                    lst.append(tpl)
        return lst

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,move_key,description)
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]
        lst_car_moves = []
        lst_coordinates_with_cars_placed = set()

        for car in self.cars:

            for move in car.possible_moves():
                car.move(move)
                invalid_coordinate = False

                for coordinate in car.car_coordinates():
                    if coordinate not in self.cell_list() or self.graphic_board[coordinate[0]][coordinate[1]]\
                            != Board.EMPTY:
                        invalid_coordinate = True

                if not invalid_coordinate:
                    tpl = (car.name, move, f"{car.get_name()} car can move {move}")
                    lst_car_moves.append(tpl)

                for coordinate in car.car_coordinates():
                    lst_coordinates_with_cars_placed.add(coordinate)

                for m in car.possible_moves():
                    if m != move:
                        car.move(m)

        return lst_car_moves

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        # In this board, returns (3,7)
        return self.SPECIAL_ROW, self.SPECIAL_COLUMN

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        board_object = self.graphic_board[coordinate[0]][coordinate[1]]
        if board_object != Board.EMPTY:
            if board_object != Board.EXIT:
                return board_object
            return None
        return None

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.
        if car.get_name() in self.cars.keys():
            return False
        for coordinate in car.car_coordinates():
            if coordinate not in self.cell_list():
                return False
            board_object = self.graphic_board[coordinate[0]][coordinate[1]]
            if board_object != Board.EMPTY and board_object != Board.EXIT:
                return False

        for coordinate in car.car_coordinates():
            self.graphic_board[coordinate[0]][coordinate[1]] = car.get_name()
        self.cars[car.name] = car.length, car.location, car.orientation, car.car_coordinates(), car

        return True

    def move_car(self, name, move_key):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param move_key: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        if name not in self.cars.keys():
            print("Invalid, No such car in the parking lot")
            return False

        car_orientation = self.cars[name][2]
        car_coordinates = self.cars[name][3]
        car_object = self.cars[name][4]

        if car_orientation == Car.VERTICAL and (move_key == Car.RIGHT or move_key == Car.LEFT):
            print("Invalid, The car can't move in the specified direction")
            return False
        if car_orientation == Car.HORIZONTAL and (move_key == Car.UP or move_key == Car.DOWN):
            print("Invalid, The car can't move in the specified direction")
            return False
        coordinate_a = (car_object.movement_requirements(move_key))
        coordinate = coordinate_a[0]

        if coordinate not in self.cell_list():
            print("Invalid location, out of the parking lot square")
            return False
        board_position = self.graphic_board[coordinate[0]][coordinate[1]]
        if board_position != Board.EMPTY and board_position != Board.EXIT:
            print("Invalid location, No available place there")
            return False

        if move_key == Car.RIGHT or move_key == Car.DOWN:
            coordinate_to_empty = car_coordinates[0]  # Start of car
            self.graphic_board[coordinate_to_empty[0]][coordinate_to_empty[1]] = Board.EMPTY  # Abandon car's territory
            car_coordinates.pop(0)  # Enough with the start of the car in the list
            self.graphic_board[coordinate[0]][coordinate[1]] = name  # Marking car's territory
            car_coordinates.append(coordinate)  # Welcome the new end!
            car_object.location = car_coordinates[0]

        elif move_key == Car.LEFT or move_key == Car.UP:
            coordinate_to_empty = car_coordinates[-1]  # End of car
            self.graphic_board[coordinate_to_empty[0]][coordinate_to_empty[1]] = Board.EMPTY  # Abandon car's territory
            car_coordinates.pop(-1)  # Enough with the end of the car in the list
            self.graphic_board[coordinate[0]][coordinate[1]] = name  # Marking car's territory
            car_coordinates.insert(0, coordinate)  # Welcome the new start!
            car_object.location = coordinate

        return True
