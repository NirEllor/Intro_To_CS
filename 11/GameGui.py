#################################################################
# FILE : GameGui.py
# WRITERS : Nir Ellor Waizner, Amir Ben Avi
# EXERCISE : intro 2cs ex11 2022-2023
# DESCRIPTION: A program that operates the utils functions in the  Boggle game
#################################################################
##############################################################################
import tkinter as tki
import pygame

CLICKED = True
NOT_CLICKED = False

BG_GAME_SOUND_PATH = "game_music.mp3"
CORRECT_ANSWER_SOUND = "correct_answer_sound.mp3"
SCORE_DISPLAY_TEXT = "SCORE:\n0"
START_CLOCK_DISPLAY = "00:00"

BUTTON_CLICK_COLOR = 'gray'
REGULAR_COLOR = '#ffffff'

BUTTON_STYLE = {"font": ("Courier", 20),
                "borderwidth": 1,
                "relief": tki.RAISED,
                "bg": REGULAR_COLOR
                }


class GameGui:
    """
    The GUI class for the Boggle game.
    """
    def __init__(self, board):
        """
        Initialize the GameGui object.

        Args:
            board (list[list[str]]): The initial game board.
        """
        # creating the root
        self.__root = tki.Tk()
        self.__root.title("Boggle Game")
        self.__root.resizable(False, False)

        # creating main frames
        self.__main_left_frame = tki.Frame(self.__root)
        self.__main_right_frame = tki.Frame(self.__root, background="#e5e5e5")
        self.__main_left_frame.pack(side=tki.LEFT, fill=tki.BOTH, expand=True)
        self.__main_right_frame.pack(side=tki.RIGHT, fill=tki.BOTH)

        # building the left main frame
        # creating the information frame
        self.__information_frame = tki.Frame(self.__main_left_frame, background="#14213d",
                                             height=100)
        self.__information_frame.pack(side=tki.TOP, fill=tki.BOTH)

        self.__start_game_button = self.__make_button("START GAME", self.__information_frame, BUTTON_STYLE)
        self.__start_game_button.pack(side=tki.RIGHT)

        self.__timer_label = tki.Label(self.__information_frame, text=START_CLOCK_DISPLAY, bg="#14213d", fg="white",
                                       font=("Courier", 40))
        self.__timer_label.pack(side=tki.LEFT)

        # creating the cur word frame
        self.__cur_word_frame = tki.Frame(self.__main_left_frame, background="#14213d",
                                          height=100)
        self.__cur_word_frame.pack(side=tki.TOP, fill=tki.BOTH)
        self.__cur_word_label = tki.Label(self.__cur_word_frame, bg="#14213d", fg="white", font=("Courier", 40))
        self.__cur_word_label.grid(row=0, column=0)

        # creating the cube frame
        self.__cubes_frame = tki.Frame(self.__main_left_frame, background="#14213d")
        self.__cubes_frame.pack(side=tki.BOTTOM, fill=tki.BOTH, expand=True)

        # building the right frame
        self.__score_label = tki.Label(self.__main_right_frame, text=SCORE_DISPLAY_TEXT,
                                       font=("Courier", 20), bg="#e5e5e5")
        self.__score_label.pack(side=tki.TOP)

        self.__valid_words_label = tki.Label(self.__main_right_frame, font=("Courier", 15), bg="#e5e5e5")
        self.__valid_words_label.pack(side=tki.TOP)

        self.__submit_button = self.__make_button("SUBMIT", self.__main_right_frame, BUTTON_STYLE)
        self.__submit_button.configure(pady=20)
        self.__submit_button.pack(side=tki.BOTTOM)

        # Sounds
        pygame.mixer.init()
        self.__bg_sound = pygame.mixer.Sound(BG_GAME_SOUND_PATH)
        self.__correct_answer_sound = pygame.mixer.Sound(CORRECT_ANSWER_SOUND)

    def run(self):
        """This function runs the GUI application"""
        self.__root.mainloop()

    def set_cubes_command(self, func):
        """This function sets the command of the cube button"""
        for cube in self.__cubes.keys():
            cube.bind("<Button-1>", func)

    def update_cube_color(self, cube):
        """This functin updates the color of the specified cube button."""
        self.__cubes[cube] = not self.__cubes[cube]

        if self.__cubes[cube] == CLICKED:
            cube['bg'] = BUTTON_CLICK_COLOR
        else:
            cube['bg'] = REGULAR_COLOR

    def reset_cube_colors(self):
        """This function reset the colors of all cube buttons."""
        for cube in self.__cubes.keys():
            self.__cubes[cube] = NOT_CLICKED
            cube['bg'] = REGULAR_COLOR

    def set_submit_command(self, func):
        """This function sets the command of the submit button"""
        self.__submit_button.bind("<Button-1>", func)

    def set_start_game_command(self, func):
        """This function sets the command of the start game button"""
        self.__start_game_button.bind("<Button-1>", func)

    def set_cur_word(self, cur_word):
        """This functon dislays the current word being collected"""
        self.__cur_word_label['text'] = cur_word

    def set_score(self, score):
        """This function sets the current accumulated score"""
        self.__score_label['text'] = f"SCORE:\n{score}"
        self.__correct_answer_sound.play()

    def set_valid_words(self, valid_words):
        """This function updates the valid words label"""
        valid_words_str = ""
        for valid_word in valid_words:
            valid_words_str += f"{valid_word}\n"
        self.__valid_words_label['text'] = valid_words_str

    def set_timer(self, time):
        """This function updates the timer in the information frame"""
        self.__timer_label['text'] = time

    def get_root(self):
        """This function gets the root of the widgets"""
        return self.__root

    def reset_game(self, board):
        """This function reset the GUI elements of the game"""
        self.__bg_sound.stop()
        self.__bg_sound.play()
        self.__create_cubes(board)
        self.__cur_word_label['text'] = ""
        self.__score_label['text'] = SCORE_DISPLAY_TEXT
        self.__timer_label['text'] = START_CLOCK_DISPLAY
        self.__valid_words_label['text'] = ""

    # ----- PRIVATE METHODS -----

    def __create_cubes(self, board):
        """THis function creates the cube buttons based on the game board."""

        self.__cubes = {}
        for i in range(len(board)):
            self.__cubes_frame.columnconfigure(i, weight=1)

        for i in range(len(board[0])):
            self.__cubes_frame.rowconfigure(i, weight=1)

        for row in range(len(board)):
            for col in range(len(board[row])):
                cube = self.__make_button(board[row][col], self.__cubes_frame, BUTTON_STYLE)
                cube.grid(row=row, column=col, rowspan=1, columnspan=1, sticky=tki.NSEW)
                self.__cubes[cube] = NOT_CLICKED

    def __make_button(self, button_char, parent_widget, style):
        """This function creates a cube widget"""
        button = tki.Button(parent_widget, text=button_char, **style)
        return button
