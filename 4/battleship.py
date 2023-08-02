#############################################################
# FILE : battleship.py
# WRITER : Nir Ellor Waizner , ellorw.nir , 323816678
# EXERCISE : intro2cs2 ex4 2023
# DESCRIPTION: This program operates the submarines game, having 2 players - user (player) and computer (rival)
#############################################################

import helper


# These constants are relevant once the game is over, and it should be decided whether to continue playing
YES = "Y"
NO = "N"
NOT_OVER = "not over"


def init_board(rows, columns):
    """This function initiates a generic board, filled with water solely"""
    lst_external = []
    for i in range(rows):
        lst_internal = []
        for j in range(columns):
            lst_internal.append(helper.WATER)
        lst_external.append(lst_internal)
    return lst_external


def cell_loc(name):
    """This functions converts textual location to a numeric location, and deals with scenarios of special arguments"""
    if isinstance(name, list):  # Illegal arguments
        return None
    if len(name) > 3 or len(name) < 1:  # Illegal locations
        return None
    if not name[0].isdigit() and len(name) == 1:
        return None
    x = name[0].capitalize()  # locations' column, can be a character from A to Z
    n = name[1:3]  # locations' row, can be an int from 1 to 99
    if len(name) >= 3 and not name[2].isdigit() or len(name) == 2 and not name[1].isdigit():  # Illegal arguments
        return None
    # Matching the string to its ordered pair
    numeric_x = ord(x) - 65
    numeric_n = int(n) - 1
    return numeric_n, numeric_x


def valid_ship(board, size, loc):
    """This function determines whether a location to set a ship is valid"""
    if loc is None:
        return False
    board_length = len(board)
    row = loc[0]
    column = loc[1]
    if row >= board_length or column >= len(board[0]):  # Prevents from the top point of the ship to exceed from the
        # board's boundaries
        return False

    for i in range(row, row + size):
        if i >= board_length:  # Prevents from all the ship's points to exceed from the board's boundaries
            return False
        elif board[i][column] == helper.SHIP:  # Prevents from all the ship's points to clash with other ships
            return False
    return True


def create_player_board(rows, columns, ship_sizes):
    """This function creates the initial board of the user, having the ships in place"""
    initialize = init_board(rows, columns)

    for num in ship_sizes:  # Entering all the ships' top point in the user's desired location, each ship with its
        # own size
        helper.print_board(initialize)
        location = helper.get_input("Enter top coordinate for ship of size {0}: ".format(num))
        fixed_location = cell_loc(location)  # Converting to numeric location

        while valid_ship(initialize, num, fixed_location) is False:  # In case of illegal inputs, ask for location
            # until a valid one is given
            helper.print_board(initialize)
            location = helper.get_input("Not a valid location, enter top coordinate for ship of size {0}: ".format(num))
            fixed_location = cell_loc(location)

        for i in range(fixed_location[0], fixed_location[0] + num):  # entering all points of the current ship
            initialize[i][fixed_location[1]] = helper.SHIP
    return initialize


def fire_torpedo(board, loc):
    """This function is used by both user and rival to attack with torpedo, changing the board of the attacked side"""
    row = loc[0]
    column = loc[1]
    if board[row][column] == helper.WATER:
        board[row][column] = helper.HIT_WATER  # A miss
    elif board[row][column] == helper.SHIP:
        board[row][column] = helper.HIT_SHIP  # A hit
    return board


def locations_board(rows, columns, board, ship_size_num):
    """This function creates all the possible locations for the rival to randomly chose"""
    location_iteration = [(x, y) for x in range(rows) for y in range(columns) if valid_ship(board, ship_size_num,
                                                                                            (x, y))]
    return location_iteration


def rival_ship_placement(board, ship_size_num):
    # ship_size_num - size of a single ship from a tuple of ships sizes
    """This function places one ship of the rival in its place"""
    locations_list = locations_board(len(board), len(board[0]), board, ship_size_num)  # Locations for placing
    # the top point of the ship
    ships_used_locations = []  # In order to prevent clashes between ships
    location_select = helper.choose_ship_location(board, ship_size_num, locations_list)
    locations_list.pop(0)

    while not valid_ship(board, ship_size_num, location_select):  # Prevent an invalid location, randomly chose
        # a location until a valid location is chosen
        locations_list = locations_board(len(board), len(board[0]), board,
                                         ship_size_num)  # Locations for placing the top point of
        location_select = helper.choose_ship_location(board, ship_size_num, locations_list)

    location_row = location_select[0]
    location_column = location_select[1]

    for i in range(location_row, location_row + ship_size_num):  # Placing the ship from its valid top point
        if board[i][location_column] in ships_used_locations:  # Prevent an already used location for other ships
            break
        else:
            board[i][location_column] = helper.SHIP


def rival_fleet_placement(board, fleet_size_tuple):
    """This function places all rival's ships, using aforementioned function to each ship"""
    for num in fleet_size_tuple:
        rival_ship_placement(board, num)
    return board


def hidden_rival_fleet(board):
    """This function creates a hidden board of a board given as an argument"""
    board_rows = len(board)
    board_columns = len(board[0])
    hidden_board = init_board(board_rows, board_columns)
    ships_locations = []  # Locations where ships were replaced with water

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == helper.SHIP:
                hidden_board[i][j] = helper.WATER  # Hiding ships with water
                ships_locations.append((i, j))  # Saving the location in order to distinguish between original water
                # locations and converted water locations
            else:
                hidden_board[i][j] = board[i][j]  # Original water locations stay as they were
    return ships_locations, hidden_board  # returning ships locations for following functions


def valid_torpedo_user(board, row, column):
    """This function ensures valid torpedo location for the user, allowing location to be chosen twice or more"""
    board_length = len(board)
    board_width = len(board[0])
    if row >= board_length or column >= board_width:  # Exceeding from the rival board's boundaries
        return False
    else:
        return True


def valid_torpedo_rival(board, row, column):
    """This function ensures valid torpedo location for the rival, preventing location to be chosen twice or more"""
    board_length = len(board)
    board_width = len(board[0])
    if row >= board_length or column >= board_width:  # Exceeding from the user board's boundaries
        return False
    if board[row][column] == helper.HIT_SHIP or board[row][column] == helper.HIT_WATER:  # preventing location to be
        # chosen twice or more
        return False
    else:
        return True


def locations_board_torpedo(rows, columns, board):
    """This function creates all the possible locations for the rival to randomly chose"""
    location_iteration = [(x, y) for x in range(rows) for y in range(columns) if valid_torpedo_rival(board, x,
                                                                                                     y)]
    return location_iteration


def is_fleet_destroyed(board):
    """This function determines if there are any ships left in a board, hence whether the fleet was destroyed or not"""
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == helper.SHIP:  # Checks for ship in each location of the board
                return False
    return True


def valid_input_end_game(string):
    """This function repeatedly asking the user to decide whether to start a new game or not, until a valid answer is
    received """
    while string != YES and string != NO:  # User typing "Y" means yes, "N" means No
        string = helper.get_input("Invalid input, do you want to play again? ")

    else:
        return string


def game_step_one(board_rows, board_columns, ships_sizes, rival_board):
    """Step 1: Each side places its ships, then the two boards are printed"""
    user_fleet = create_player_board(board_rows, board_columns, ships_sizes)

    rival_fleet = rival_fleet_placement(rival_board, ships_sizes)

    used_locations = hidden_rival_fleet(rival_fleet)[0]  # The original ship locations of the hidden rival board
    hidden_fleet = hidden_rival_fleet(rival_fleet)[1]  # The hidden rival board itself

    helper.print_board(user_fleet, hidden_fleet)

    return user_fleet, hidden_fleet, rival_fleet, used_locations


def game_step_two(user_fleet, hidden_fleet):
    """Step 2: Each side chooses locations to shoot his torpedo"""
    board_rows = len(hidden_fleet)
    board_columns = len(hidden_fleet[0])
    target_select_rival = helper.choose_torpedo_target(user_fleet,
                                                       locations_board_torpedo(board_rows, board_columns, user_fleet))

    target_select_user = helper.get_input("Choose Target: ")  # Asking the user for location
    fixed_target_select_user = cell_loc(target_select_user)  # Converting to numeric location, unless an invalid
    # location is received, thus the expression is None

    while fixed_target_select_user is None:  # Dealing with the aforementioned None expression
        fixed_target_select_user = cell_loc(helper.get_input("Invalid target, choose Target: "))  # asking for location
        # and checking
        # until the location is valid

    valid_user = valid_torpedo_user(hidden_fleet, fixed_target_select_user[0], fixed_target_select_user[1])
    valid_rival = valid_torpedo_rival(user_fleet, target_select_rival[0], target_select_rival[1])

    while not valid_rival or not valid_user:  # Dealing with invalid locations in terms of exceeding board's boundaries
        # or rival chooses an already selected location
        if not valid_rival:  # Rival scenarios
            target_select_rival = helper.choose_torpedo_target(user_fleet, locations_board_torpedo(board_rows,
                                                                                                   board_columns,
                                                                                                   user_fleet))
            valid_rival = valid_torpedo_rival(user_fleet, target_select_rival[0], target_select_rival[1])
        else:  # User scenarios
            fixed_target_select_user = cell_loc(helper.get_input("Invalid target, choose Target: "))
            valid_user = valid_torpedo_user(hidden_fleet, fixed_target_select_user[0], fixed_target_select_user[1])

    return fixed_target_select_user, target_select_rival


def game_step_three(user_fleet, hidden_fleet, rival_fleet, target_select_user, target_select_rival, used_locations):
    """Step 3 - launching the torpedoes by the two sides"""
    fire_torpedo(user_fleet, target_select_rival)  # Rival fires the torpedo
    if target_select_user in used_locations:  # Checking if the user selected a location of a hidden ship
        ship_row = target_select_user[0]
        ship_column = target_select_user[1]
        hidden_fleet[ship_row][ship_column] = helper.SHIP  # Replace the water back to the ship, as it was

    fire_torpedo(hidden_fleet, target_select_user)  # User fires the torpedo towards rival board
    fire_torpedo(rival_fleet, target_select_user)  # User fires the torpedo towards hidden board
    if not is_fleet_destroyed(rival_fleet) and not is_fleet_destroyed(user_fleet):  # If no fleet was destroyed
        helper.print_board(user_fleet, hidden_fleet)


def game_step_four(user_fleet, hidden_fleet, rival_fleet, used_locations):
    """Step 4 - Continue shooting  until at least one fleet is destroyed"""
    if is_fleet_destroyed(user_fleet):
        helper.print_board(user_fleet, rival_fleet)
        answer = helper.get_input("Rival won! Do you want to play again? ")
        return answer

    elif is_fleet_destroyed(rival_fleet):
        helper.print_board(user_fleet, rival_fleet)
        answer = helper.get_input("User won! Do you want to play again? ")
        return answer

    elif is_fleet_destroyed(user_fleet) and is_fleet_destroyed(rival_fleet):  # In case both fleets were destroyed at
        # the same time
        helper.print_board(user_fleet, rival_fleet)
        answer = helper.get_input("It's a tie! Do you want to play again? ")
        return answer

    else:  # No fleet was destroyed
        second_step = game_step_two(user_fleet, hidden_fleet)  # Choosing locations for torpedoes once again
        game_step_three(user_fleet, hidden_fleet, rival_fleet, second_step[0], second_step[1], used_locations)
        # Launching the torpedoes once again
        return NOT_OVER


def main():
    """The function gathers the specific details for user and rival and operating the game until user don't want to"""
    game_on = YES

    while game_on == YES:  # The game is carried out inside the loop
        game_rows = helper.NUM_ROWS
        game_columns = helper.NUM_COLUMNS
        ships = helper.SHIP_SIZES
        rival_board = init_board(game_rows, game_columns)

        first_step = game_step_one(game_rows, game_columns, ships, rival_board)
        # Choosing locations for the ships
        user_fleet_main = first_step[0]
        hidden_fleet_main = first_step[1]
        rival_fleet_main = first_step[2]
        used_locations = first_step[3]

        continue_gaming = game_step_four(user_fleet_main, hidden_fleet_main, rival_fleet_main, used_locations)
        while continue_gaming == NOT_OVER:  # While no fleet was destroyed
            continue_gaming = game_step_four(user_fleet_main, hidden_fleet_main, rival_fleet_main, used_locations)

        if continue_gaming == NO:
            game_on = NO  # Breaking from the loop and quitting the game
        else:
            game_on = valid_input_end_game(continue_gaming)  # Repeatedly asking for a valid answer


if __name__ == "__main__":
    main()
