#################################################################
# FILE : boggle.py
# WRITERS : Nir Ellor Waizner, Amir Ben Avi
# EXERCISE : intro 2cs ex11 2022-2023
# DESCRIPTION: A program that operates the utils functions in the  Boggle game
#################################################################
##############################################################################

# GameController


import GameGui
import GameModel
import boggle_board_randomizer
import ex11_utils

PLAYING = True
NOT_PLAYING = False


class Boggle:
    def __init__(self, game_words):
        self.__logic = GameModel.GameModel([], game_words)
        self.__gui = GameGui.GameGui(self.__logic.get_board())

        # # setting the start game action command
        start_action_command = self.__create_start_game_action()
        self.__gui.set_start_game_command(start_action_command)

    def __create_start_game_action(self):
        """
        Create the action for the Start Game button.
        Returns:
        - function: The action function to be executed when the cube button is pressed.
        """
        def action(event):
            """
            Action function for the Start Game button.
            This function starts the game, initializes the game board, and sets up
            the cube and submit actions.
            Parameters:
            - event: The event triggered by the button press.
            """
            game_board = boggle_board_randomizer.randomize_board(boggle_board_randomizer.LETTERS)
            self.__logic.reset_game(game_board)
            self.__gui.reset_game(self.__logic.get_board())
            self.__logic.set_game_status(PLAYING)

            # setting the cube action command
            cube_action_command = self.__create_cube_action()
            self.__gui.set_cubes_command(cube_action_command)

            # setting the submit action command
            submit_action_command = self.__create_submit_action()
            self.__gui.set_submit_command(submit_action_command)

            # manage the game time
            self.__manage_game_time()

        return action

    def __create_cube_action(self):
        """
        Create the action for the cubes on the game board.
        Returns:
        - function: The action function to be executed when a cube is clicked.
        """
        def action(event):
            """
            Action function for the cubes on the game board.

            This function updates the current word and cube colors when a cube is clicked.

            Parameters:
            - event: The event triggered by the cube click.
            """
            if self.__logic.get_game_status():
                cube = event.widget
                cube_y = cube.grid_info()["row"]
                cube_x = cube.grid_info()["column"]
                self.__logic.pressed_on_cube(cube_y, cube_x)
                self.__gui.set_cur_word(self.__logic.get_cur_word())
                self.__gui.update_cube_color(cube)

        return action

    def __create_submit_action(self):
        """
        Create the action for the Submit button.
        Returns:
        - function: The action function to be executed when the button is pressed.
        """
        def action(event):
            """
            Action function for the Submit button.
            This function checks if the current word is valid, updates the score and
            the list of valid words, and resets the current word and cube colors.
            Parameters:
            - event: The event triggered by the button press.
            """
            if self.__logic.get_game_status():
                is_valid_word = self.__logic.add_word_if_path_is_valid()

                if is_valid_word:
                    self.__logic.add_score()

                    cur_score = self.__logic.get_accumulated_score()
                    self.__gui.set_score(cur_score)

                    valid_words = self.__logic.get_valid_words()
                    self.__gui.set_valid_words(valid_words)

                self.__logic.clear_cur_path()
                cur_word = self.__logic.get_cur_word()
                self.__gui.set_cur_word(cur_word)
                self.__gui.reset_cube_colors()

        return action

    def __manage_game_time(self):
        """This function manages the timer action: creates the timer, and when time ends the game will stop"""
        time_left_in_game = self.__logic.get_time_left_in_game()
        str_time_left_in_game = self.__logic.format_time_to_str(time_left_in_game)

        if time_left_in_game >= 0:
            self.__gui.set_timer(str_time_left_in_game)
            root = self.__gui.get_root()
            root.after(200, self.__manage_game_time)
        else:
            self.__logic.set_game_status(NOT_PLAYING)

    def run(self):
        """This function runs the game"""
        self.__gui.run()


if __name__ == '__main__':
    words = ex11_utils.get_words_from_file("boggle_dict.txt")
    boggle = Boggle(words)
    boggle.run()
