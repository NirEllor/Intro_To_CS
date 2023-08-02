#################################################################
# FILE : puzzle_solver.py
# WRITER : Nir Ellor Waizner , ellorw.nir , 323816678
# EXERCISE : intro 2cs ex8 2022-2023
# DESCRIPTION: A program that operates a puzzle game using backtracking
#################################################################
##############################################################################
#                                   Imports                                  #
##############################################################################
from typing import List, Tuple, Set, Optional
##############################################################################
#                                 FUNCTIONS                                  #


# We define the types of a partial picture and a constraint (for type checking).
Picture = List[List[int]]
Constraint = Tuple[int, int, int]


def max_rows_seen_cells(picture, row, col):
    """This function counts the max num of seen cells in the row of a given cell"""
    cnt = 1
    locked_row = 0
    for i in range(len(picture[row])):
        if i != col:
            if picture[row][i] == 0 and abs(col - i) < 2:
                cnt = 1
                locked_row += 1
                if locked_row == 2 or row == 0 or row == len(picture) - 1:
                    break
            if abs(picture[row][i]) == 1:
                cnt += 1
    return cnt


def max_columns_seen_cells(picture, row, col):
    """This function counts the max num of seen cells in the column of a given cell"""
    cnt = max_rows_seen_cells(picture, row, col)
    locked_column = 0
    for j in range(len(picture)):
        for k in range(len(picture[0])):
            if j != row and k == col:
                if picture[j][k] == 0 and abs(j - row) < 2:
                    locked_column += 1
                    if locked_column == 2 or col == 0 or col == len(picture[0]) - 1:
                        return cnt
                if abs(picture[j][k]) == 1:
                    cnt += 1
    return cnt


def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    """This function counts the max seen cells, assisted by the aforementioned functions"""
    if picture[row][col] == 0:
        return 0
    return max_columns_seen_cells(picture, row, col)


def min_rows_seen_cells(picture, row, col):
    """This function counts the min num of seen cells in the row of a given cell"""
    cnt = 1
    locked_row = 0
    for i in range(len(picture[row])):
        if i != col:
            if (picture[row][i] == 0 or picture[row][i] == -1) and abs(col - i) < 2:
                cnt = 1
                locked_row += 1
                if locked_row == 2 or row == 0 or row == len(picture) - 1:
                    break
            if picture[row][i] == 1:
                cnt += 1
    return cnt


def min_columns_seen_cells(picture, row, col):
    """This function counts the min num of seen cells in the column of a given cell"""
    cnt = min_rows_seen_cells(picture, row, col)
    locked_column = 0
    for j in range(len(picture)):
        for k in range(len(picture[0])):
            if j != row and k == col:
                if (picture[j][k] == 0 or picture[j][k] == -1) and abs(j - row) < 2:
                    cnt = 1
                    locked_column += 1
                    if locked_column == 2 or col == 0 or col == len(picture[0]) - 1:
                        return cnt
                if picture[j][k] == 1:
                    # print(j, k)
                    cnt += 1
    return cnt


def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    """This function counts the min seen cells, assisted by the aforementioned functions"""
    if picture[row][col] == 0 or picture[row][col] == -1:
        return 0
    return min_columns_seen_cells(picture, row, col)


def check_constraints(picture: Picture, constraints_set: Set[Constraint]) -> int:
    """This function determines the possibility for a solution in the puzzle game, given a picture and
    a constraint set"""
    second_scenario = False
    for constraint in constraints_set:
        a = constraint[0]
        b = constraint[1]
        c = constraint[2]
        maximum = max_seen_cells(picture, a, b)
        minimum = min_seen_cells(picture, a, b)
        if c > maximum:
            return 0
        if c < minimum:
            return 0
        if maximum >= c > minimum or minimum <= c < maximum:
            second_scenario = True
    if second_scenario:
        return 2
    return 1


def deep_copy_list(lst):
    """This function manually creates a deep copy, will be used when we'll fund a solution to the puzzle game"""
    # Base case: If lst is not a list, return the element itself
    if not isinstance(lst, list):
        return lst

    # Create a new list to store the copied elements
    copied_list = []

    # Iterate over the elements in the original list
    for item in lst:
        # Recursively deep copy each element and append it to the new list
        copied_item = deep_copy_list(item)
        copied_list.append(copied_item)

    return copied_list


def move_forward(row, column, picture):
    """This function moves us to the next point to the left in the same row, or to the starting point of a new row if
    necessary """
    if column < len(picture[0]) - 1:
        return row, column + 1
    else:  # We reached the end of the row
        return row + 1, 0


def is_over(picture, num):
    """Determining if there is still an element in the lists that wasn't changed """
    for i in range(len(picture)):
        for j in range(len(picture[0])):
            if picture[i][j] == num:
                return False
    return True


def _solve_puzzle_helper(picture, start_row, start_column, constraints, num_of_solutions, solutions, maybe_sol):
    """This is the engine to the solve_puzzle function, using recursion"""
    if check_constraints(picture, constraints) == 0:
        # Base case - The constraint set conditions were violated
        return False
    else:
        if is_over(picture, -1):
            # Checking if all the lists were filled with zeros and ones
            if check_constraints(picture, constraints) == 1:
                # Checking if the current fully filled picture is a sure solution
                the_solution = deep_copy_list(picture)
                solutions.append(the_solution)
                # The solution won't be run over
                num_of_solutions[0] += 1
            elif check_constraints(picture, constraints) == 2:
                # Checking if the current fully filled picture is only a possible solution
                maybe_solution = deep_copy_list(picture)
                maybe_sol.append(maybe_solution)
                # The solution won't be run over
            return False
        picture[start_row][start_column] = 1
        # Try filling the point with 1
        next_step = move_forward(start_row, start_column, picture)
        # Move to the next point
        _solve_puzzle_helper(picture, next_step[0], next_step[1], constraints, num_of_solutions, solutions, maybe_sol)
        # Recursion - Try moving until the base case or the solution
        picture[start_row][start_column] = 0
        # Try filling the point with 0
        _solve_puzzle_helper(picture, next_step[0], next_step[1], constraints, num_of_solutions, solutions, maybe_sol)
        # Recursion - Try moving until the base case or the solution
        picture[start_row][start_column] = -1
        # Backtracking - Fill back to -1
    if num_of_solutions[0] < 1 and len(maybe_sol) < 1:
        # Check if there aren't any type of solutions at all
        return None
    elif len(solutions) == 0:
        # If there is no sure solution at all
        return maybe_sol[0]
    return solutions[0]
    # There is a sure solution


def solve_puzzle(constraints_set: Set[Constraint], n: int, m: int) -> Optional[Picture]:
    """This function solves the puzzle game using the aforementioned helper function"""
    puzzle = []
    for i in range(n):
        columns = []
        for j in range(m):
            columns.append(-1)
        puzzle.append(columns)
    listed_constraints = list(constraints_set)
    # A deep copy list was created
    row = 0
    column = 0
    cnt_solutions = [0]  # The number of sure solutions
    solutions = []  # The sure solutions
    maybe_solutions = []   # The possible solutions
    return _solve_puzzle_helper(puzzle, row, column, listed_constraints, cnt_solutions, solutions, maybe_solutions)


# print(solve_puzzle({(0, 3, 3), (1, 2, 5), (2, 0, 1), (0, 0, 0)}, 3, 4))
# print(solve_puzzle({(0, 3, 3), (1, 2, 5), (2, 0, 1), (2, 3, 5)}, 3, 4))
# print(solve_puzzle({(0, 2, 3), (1, 1, 4), (2, 2, 5)}, 3, 3))
# print(solve_puzzle({(0, 3, 3), (1, 2, 5), (2, 0, 1), (0, 0, 1)}, 3, 4))
# print(solve_puzzle({(0, 3, 3), (2, 0, 1)}, 3, 4))
# print(solve_puzzle(set(), 2, 2))


def _num_solutions_helper(picture, start_row, start_column, constraints, num_of_solutions, num_of_maybe_solutions):
    """This is the engine to the how_many_solutions function, using recursion"""
    if check_constraints(picture, constraints) == 0:
        # Base case - The constraint set conditions were violated
        return False
    else:
        if is_over(picture, -1):
            # Checking if all the lists were filled with zeros and ones
            if check_constraints(picture, constraints) == 1:
                # Checking if the current fully filled picture is a sure solution
                num_of_solutions[0] += 1
            print("sure solutions", num_of_solutions)
            if check_constraints(picture, constraints) == 2:
                # Checking if the current fully filled picture is a possible solution
                num_of_maybe_solutions[0] += 1
            print("possible solutions", num_of_maybe_solutions)
            return False
        picture[start_row][start_column] = 1
        # Try filling the point with 1
        next_step = move_forward(start_row, start_column, picture)
        # Move to the next point
        _num_solutions_helper(picture, next_step[0], next_step[1], constraints, num_of_solutions,
                              num_of_maybe_solutions)
        # Recursion - Try moving until the base case or the solution
        picture[start_row][start_column] = 0
        # Try filling the point with 0
        _num_solutions_helper(picture, next_step[0], next_step[1], constraints, num_of_solutions,
                              num_of_maybe_solutions)
        # Recursion - Try moving until the base case or the solution
        picture[start_row][start_column] = -1
        # Backtracking - Fill back to -1
    if num_of_solutions[0] < 1 and num_of_maybe_solutions[0] < 1:
        # Check if there aren't any type of solutions at all
        return 0
    if num_of_solutions[0] < 1:
        # If there is no sure solution at all
        return num_of_maybe_solutions[0]
    return num_of_solutions[0]
    # There is a sure solution


def how_many_solutions(constraints_set: Set[Constraint], n: int, m: int) -> int:
    """This function counts the number of solutions in the puzzle game using the aforementioned helper function"""
    puzzle = []
    for i in range(n):
        columns = []
        for j in range(m):
            columns.append(-1)
        puzzle.append(columns)
    listed_constraints = list(constraints_set)
    # A deep copy list was created
    row = 0
    column = 0
    cnt_solutions = [0]  # The number of sure solutions
    cnt_maybe_solutions = [0]  # The number of possible solutions
    return _num_solutions_helper(puzzle, row, column, listed_constraints, cnt_solutions, cnt_maybe_solutions)


# print(how_many_solutions({(0, 3, 3), (1, 2, 5), (2, 0, 1), (2, 3, 5)}, 3, 4))
# print(how_many_solutions({(0, 3, 3), (1, 2, 5), (2, 0, 1), (0, 0, 1)}, 3, 4))
# print(how_many_solutions({(0, 2, 3), (1, 1, 4), (2, 2, 5)}, 3, 3))
# print(how_many_solutions({(i, j, 0) for i in range(3) for j in range(3)}, 3, 3))
# print(how_many_solutions(set(), 2, 2))
# print(how_many_solutions({(0, 3, 3), (2, 0, 1)}, 3, 4))


def generate_puzzle(picture: Picture) -> Set[Constraint]:
    ...
