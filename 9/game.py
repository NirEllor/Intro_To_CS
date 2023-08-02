#################################################################
# FILE : game.py
# WRITER : Nir Ellor Waizner , ellorw.nir , 323816678
# EXERCISE : intro 2cs ex9 2022-2023
# DESCRIPTION: A program that operates the Game class in the rush hour's game and the gameplay itself
#################################################################
##############################################################################
import sys

from car import Car
import board as b
from helper import load_json
from sys import argv


class Game:
    """
    This class creates instances of the rush hour gme, given cars and parking lot in imported modules
    """
    COLORS = "YBOGWR"
    DIRECTIONS = "udrl"
    COMMA = ","
    END_GAME = "!"

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        # You may assume board follows the API
        # implement your code and erase the "pass"
        self.board = board

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        print(self.board)
        user_input = input("What color car to move, and what direction to move it? ")
        if user_input == Game.END_GAME:
            return False
        while len(user_input) != 3 or user_input[1] != Game.COMMA or user_input[0] not in Game.COLORS \
                or user_input[2] not in Game.DIRECTIONS:
            user_input = input("Invalid input, try again as instructed above: ")
            if user_input == Game.END_GAME:
                return False

        car_name = user_input[0]
        direction = user_input[2]
        self.board.move_car(car_name, direction)
        victory_coordinate = self.board.target_location()

        victory_cell = self.board.graphic_board[victory_coordinate[0]][victory_coordinate[1]]
        if victory_cell != self.board.EXIT:
            return victory_cell
        return True

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        playing = self.__single_turn()
        while playing is True:
            playing = self.__single_turn()

        if not playing:  # Pressed "!"
            print("Game stopped, goodbye!")
            return True
        else:  # Some car reached the exit and won
            print(f"{playing} reached the exit and won, game over!")
            return True


if __name__ == "__main__":
    # Your code here
    # All access to files, non API constructors, and such must be in this
    # section, or in functions called from this section.
    my_argv = argv
    j_file = load_json(my_argv[1])
    valid_cars = True
    for item in j_file.items():
        if len(item) != 2 or len(item[1]) != 3 or len(item[1][1]) != 2:
            print("Invalid car object")
            valid_cars = False
        if len(item[0]) != 1 and item[0] not in Game.COLORS:
            print("Invalid car's color")
            valid_cars = False
        item_length = item[1][0]
        if item_length != 2 and item_length != 3 and item_length != 4:
            print("Invalid car's length")
            valid_cars = False
        if item[1][2] != Car.HORIZONTAL and item[1][2] != Car.VERTICAL:
            print("Invalid car's orientation")
            valid_cars = False
    if valid_cars:
        my_cars_collection = []
        for car in j_file.items():
            my_car = Car(car[0], car[1][0], tuple(car[1][1]), car[1][2])
            my_cars_collection.append(my_car)
        my_board = b.Board()
        for car_game in my_cars_collection:
            my_board.add_car(car_game)
        my_game = Game(my_board)
        gaming = my_game.play()
        if gaming:
            sys.exit()
