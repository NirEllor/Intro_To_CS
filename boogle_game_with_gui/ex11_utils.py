#################################################################
# FILE : ex11_utils.py
# WRITERS : Nir Ellor Waizner, Amir Ben Avi
# EXERCISE : intro 2cs ex11 2022-2023
# DESCRIPTION: A program that operates the utils functions in the  Boggle game
#################################################################
##############################################################################

from typing import List, Tuple, Iterable, Optional

Board = List[List[str]]
Path = List[Tuple[int, int]]

Y, X = 0, 1
PATH, WORD = 0, 1


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """
    Checks if a given path on the board is a valid word.
    Args:
        board (Board): The game board containing cube positions.
        path (Path): The path on the board to check.
        words (Iterable[str]): The list of valid words.
    Returns:
        Optional[str]: The word if the path is valid, otherwise None.
    """
    # created the set to check for duplicates
    used_cubes = set()

    if not len(path):
        return None

    prev_cube = path[0]
    used_cubes.add(prev_cube)

    for i in range(1, len(path)):
        cur_cube = path[i]
        # checks if the distance between cubes is valid
        if not abs(prev_cube[Y] - cur_cube[Y]) and not abs(prev_cube[X] - cur_cube[X]):
            return None

        if abs(prev_cube[Y] - cur_cube[Y]) > 1 or abs(prev_cube[X] - cur_cube[X]) > 1:
            return None
        # checks if there are no duplicates
        if cur_cube in used_cubes:
            return None

        used_cubes.add(cur_cube)

        prev_cube = cur_cube

    # after we passed all the conditions, the path is legal, and we need to check if the path is in the dict.
    word_from_path = get_word_from_path(board, path)
    if word_from_path not in words:
        return None

    return word_from_path


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
    Finds all paths on the board of length n that correspond to valid words.
    Args:
        n (int): The length of the paths to find.
        board (Board): The game board containing cube positions.
        words (Iterable[str]): The list of valid words.

    Returns:
        List[Path]: A list of paths of length n that correspond to valid words.
    """
    return find_length_n(n, board, words, PATH)


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
    Finds all words on the board of length n that correspond to valid words.
    Args:
        n (int): The length of the words to find.
        board (Board): The game board containing cube positions.
        words (Iterable[str]): The list of valid words.
    Returns:
        List[Path]: A list of paths with words of length n that correspond to valid words.
    """
    return find_length_n(n, board, words, WORD)


def find_length_n(n: int, board: Board, words, path_or_word) -> List[Path]:
    valid_paths = []
    # for every y, x in the board we call the helper to recursively create all the correct paths of size n
    for y in range(len(board)):
        for x in range(len(board[y])):
            current_path = []
            find_length_n_helper(n, board, words, valid_paths, current_path, path_or_word, y, x)
    return valid_paths


def find_length_n_helper(n, board, words, valid_paths, current_path, path_or_word, y, x):
    """
    Finds all paths or words on the board of length n that correspond to valid words or sub-words.
    Args:
        n (int): The length to find.
        board (Board): The game board containing cube positions.
        words (Iterable[str]): The list of valid words.
        path_or_word: Indicates whether to find paths of length n or words of length n.
    Returns:
        List[Path]: A list of paths of paths of length n or words of length n that correspond to valid words or
         sub-words.
    """
    current_path.append((y, x))

    if n == 1:
        if is_valid_path(board, current_path, words):
            valid_paths.append(current_path[:])
        current_path.pop()
        return

    if n < 1:
        current_path.pop()
        return

    cur_word = get_word_from_path(board, current_path)
    words = [word for word in words if word.startswith(cur_word)]

    if not words:
        current_path.pop()
        return

    for y_inc in range(-1, 2):
        for x_inc in range(-1, 2):
            if 0 <= y + y_inc <= len(board) - 1 and 0 <= x + x_inc <= len(board[y]) - 1:
                if not x_inc and not y_inc:
                    continue
                # check if the current path(sub_word) is in the word list, if so, continue to add, if not pop and return
                decrement = len(board[y][x]) if path_or_word == WORD else 1
                find_length_n_helper(n - decrement, board, words, valid_paths,
                                     current_path, path_or_word,
                                     y + y_inc, x + x_inc)

    current_path.pop()


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """
    Finds the maximum score paths on the board that correspond to valid words.
    Args:
        board (Board): The game board containing cube positions.
        words (Iterable[str]): The list of valid words.
    Returns:
        List[Path]: A list of paths on the board that correspond to valid words, with the maximum scores.
    """
    words_in_board = {}
    max_len_word = get_max_len_word(words)
    for n in range(1, max_len_word + 1):
        valid_paths_size_n = find_length_n_paths(n, board, words)
        for valid_path in valid_paths_size_n:
            word = get_word_from_path(board, valid_path)
            words_in_board[word] = valid_path

    return list(words_in_board.values())


def get_word_from_path(board, path):
    """
    Constructs the word from a given path on the board.
    Args:
        board (Board): The game board containing cube positions.
        path (Path): The path on the board.
    Returns:
        str: The word constructed from the path.
    """
    word = ""
    for cube in path:
        word += board[cube[Y]][cube[X]]
    return word


def get_words_from_file(file_path: str) -> List[str]:
    """
    Reads words from a file and returns them as a list.
    Args:
        file_path (str): The path to the file containing the words
    """
    with open(file_path, "r") as file:
        words_str = file.read()

    return words_str.splitlines()


def get_max_len_word(words: Iterable[str]):
    """
    Finds the length of the longest word in the given list of words.
    Args:
        words (Iterable[str]): The list of words.
    Returns:
        int: The length of the longest word.
    """
    max_len = len(words[0])

    for cur_word in words:
        cur_word_len = len(cur_word)
        if cur_word_len > max_len:
            max_len = cur_word_len

    return max_len
