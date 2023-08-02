#################################################################
# FILE : GameModel.py
# WRITERS : Nir Ellor Waizner, Amir Ben Avi
# EXERCISE : intro 2cs ex11 2022-2023
# DESCRIPTION: A program that operates the utils functions in the  Boggle game
#################################################################
##############################################################################

import ex11_utils
import time

PLAYING_TIME_IN_SECONDS = 180  # 3 minutes
PLAYING = True
NOT_PLAYING = False


class GameModel:
    """
    This class represents the game logic for the Boggle game.
    Attributes:
        __cur_path (list): List of tuples representing the current path of selected cubes.
        __valid_words (list): List of valid words formed during the game.
        __board (list): List of lists representing the game board.
        __words (iterable): The dictionary's game .
        __start_time (float): Time at which the game started.
        __game_status (bool): Current game status (playing or not playing).
        __accumulated_score (int): Accumulated score during the game.
    """
    def __init__(self, board, words):
        self.__cur_path = []
        self.__valid_words = []
        self.__board = board
        self.__words = words
        self.__start_time = None
        self.__game_status = NOT_PLAYING
        self.__accumulated_score = 0

    def get_cur_word(self):
        """This function returns the current word that the user chosen"""
        return ex11_utils.get_word_from_path(self.__board, self.__cur_path)

    def get_board(self):
        """This function returns the current word that the user has chosen"""
        return self.__board

    def get_accumulated_score(self):
        """This function returns the accumulated score during the game"""
        return self.__accumulated_score

    def get_valid_words(self):
        """This function returns the list of valid words formed during the game"""
        return self.__valid_words

    def get_game_status(self):
        """This function returns the current game status."""
        return self.__game_status

    def set_game_status(self, status):
        """This function sets the game status (playing or not playing)"""
        self.__game_status = status

    def reset_game(self, board):
        """This function reset the logic elements of the game"""
        self.__board = board
        self.__cur_path = []
        self.__valid_words = []
        self.__start_time = self.get_cur_time()
        self.__game_status = NOT_PLAYING
        self.__accumulated_score = 0

    def pressed_on_cube(self, y, x):
        """"This function handles the user's selection of a cube on the game board"""
        if (y, x) not in self.__cur_path:
            self.__cur_path.append((y, x))
        else:
            self.__cur_path.remove((y, x))

    def add_word_if_path_is_valid(self):
        """
        this function checks if the current path is valid in the board by calling utils module
        valid word is a word that the path is valid, and not already in valid_words
        """
        word = ex11_utils.is_valid_path(self.__board, self.__cur_path, self.__words)
        if word and word not in self.__valid_words:
            self.__valid_words.append(word)
            return True
        return False

    def clear_cur_path(self):
        """This function clears the current selected path"""
        self.__cur_path = []

    def add_score(self):
        """This function adds the score based on the length of the current path"""
        self.__accumulated_score += len(self.__cur_path) ** 2

    def get_cur_time(self):
        """This function returns the current time"""
        current_time = time.time()
        return current_time

    def get_time_left_in_game(self):
        """This function calculates the remaining time left in the game."""
        current_time = time.time()
        remaining_time = PLAYING_TIME_IN_SECONDS - (current_time - self.__start_time)
        return remaining_time

    def format_time_to_str(self, time_obj):
        """This function Formats the given time object into a string representation of minutes and seconds"""
        minutes = int(time_obj // 60)
        seconds = int(time_obj % 60)
        return f"{minutes:02d}:{seconds:02d}"
