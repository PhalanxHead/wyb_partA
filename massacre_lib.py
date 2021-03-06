"""
Library for partA.py
Alistair Moffat Appreciation Society
Amy Rieck and Luke Hedt
26/03/2018
"""

from moves_lib import *

""" Make infinity a really large number """
INFINITY = 9999999

""" Defining our node that will be used within our A* search algorithm"""
class Node():
    def _init_(self):
        self.children = None
        self.state = None
        self.f_value = 0
        self.g_value = 0
        self.best_neighbour = None

""" ************************************************************************* """

def massacre(board, black, white):
    """
    Sets off the Massacre AI
    Returns:        The Sequence of moves
    ________________________
    Input Variables:
        board:         The board array as defined above
        black:        The list of black position tuples
        white:        The list of white position tuples
    """
    sequence = []
    state = board
    alive_pieces = black
    white_locations = white
    black_location = black

    """ Try to kill black pieces while they're still on the board """
    while alive_pieces:
        pieces_to_kill = gen_winning_positions(state, alive_pieces)
        white1_orig, white1_goal, white2_orig, white2_goal = white_pieces(state, pieces_to_kill, white_locations, black_location)

        white_1_sequence, state = A_star_search(white1_orig, white1_goal, white_locations, state)
        sequence.append(white_1_sequence)

        """ White 2 doesn't need to move if the black piece is next to an X """
        if white2_goal:
            white_2_sequence, state = A_star_search(white2_orig, white2_goal, white_locations, state)
            sequence.append(white_2_sequence)

        white_locations, state = white_move(state, white_locations, white1_orig, white1_goal)

        if white2_goal:
            white_locations, state = white_move(state, white_locations, white2_orig, white2_goal)

        alive_pieces, state = check_state(state, alive_pieces)

    return sequence

""" ************************************************************************* """

def white_pieces(board, winning_pos, white_locations, black_locations):
    """
    Need to pick which black piece to kill based off which black pieces are
    killable in the current game state and the minimum distance between
    white pieces and the said black piece. Black piece with the closest white
    pieces is selected.
    Returns:                Tuple(White1_Loc, White1_Goal, White2_Loc, White2_Goal)
    ________________________
    Input Variables:
        board:              The board array as defined above
        winning_pos:        The list of pairs of positions where a black
                            piece can be killed.
        white_locations:    The list of white piece location tuples.
        black_locations:    The list of black piece location tuples.
    """

    white1_orig = None
    white2_orig = None
    white1_goal = None
    white2_goal = None

    min_distance = INFINITY
    """ Flag for initialising values """
    min_dist_set = False

    """ Search through all of the pairs for the minimum distance between a
        White and Black pair. """
    for pair in winning_pos:

        winP1, P1Goal, winP2, P2Goal, dist = return_min_MD_pair(board, white_locations, winning_pos)

        """ Check the flag to see if values have been set. """
        if not min_dist_set:
              min_distance = dist
              white1_orig = winP1
              white1_goal = P1Goal
              min_dist_set = True
              if winP2 != (9,9):
                  white2_goal = P2Goal
                  white2_orig = winP2
              else:
                  white2_goal = None
                  white2_orig = None

        if dist < min_distance:
            min_distance = dist
            white1_orig = winP1
            white1_goal = P1Goal
            min_dist_set = True
            if winP2 != (9,9):
                white2_goal = P2Goal
                white2_orig = winP2
            else:
                white2_goal = None
                white2_orig = None

    return white1_orig, white1_goal, white2_orig, white2_goal

""" ************************************************************************* """

def return_min_MD_pair(board, white_locations, winning_pos):
    """
    Calculates the manhattan distance between The closest white pieces and the
    black piece they're klling.
    Returns:                 List(Current White1 Location, White 1 Goal, Current White 2 Location,
                                    White 2 Goal, Their Combined Manhattan Distance)
    ______________________
    Input Variables:
        board:               The board array
        white_locations:     The location list of all  the white pieces
        winning_pos:         The list of all the winning pairs.
    """

    """ Just for the sake of initial values.
        Note min_pair = [piece1, piece2], where
             piece = [Source, Dest, Manhattan Dist]"""
    current_min = [[(9,9), (9,9), INFINITY],[(9,9), (9,9), INFINITY]]

    """ Trial all of the pairs """
    for win_pair in winning_pos:
        trialPos = [[(9,9), win_pair[0], INFINITY], [(9,9), win_pair[1], INFINITY]]
        white_locations_temp = white_locations.copy()

        """ Check for the singular tuple (For a black piece next to an X) """
        if type(win_pair) is list:

            """ Search through each position in the pair """
            for i, wPiece in enumerate(win_pair):
                """ Find the lowest distance between the winning pos and a white piece """
                man_piece, man_dist = get_min_manhat_dist(wPiece, white_locations_temp)
                trialPos[i] = [man_piece, wPiece, man_dist]
                """ Remove the white piece from the list se we don't choose it again """
                white_locations_temp.remove(man_piece)

        else:
            man_piece, man_dist = get_min_manhat_dist(win_pair, white_locations_temp)
            trialPos[0] = [man_piece, win_pair, man_dist]
            """ Make sure if only one piece needs to be moved, the distance has no
                effect on which pair is chosen and that the position is out of range """
            trialPos[1] = [(9,9), (9,9), 0]

        """ Reset lowest distance pair if it has a lower combined distance """
        if trialPos[0][2] + trialPos[1][2] <  current_min[0][2] + current_min[1][2]:
            current_min = trialPos

    return [current_min[0][0], current_min[0][1], current_min[1][0], current_min[1][1], current_min[0][2] + current_min[1][2]]

""" ************************************************************************* """

def get_min_manhat_dist(win_pos, white_locations):
    """
    Calculates the minimum manhattan distance between a winning position and the list of white pieces
    Returns:
       min_piece:           The closest white piece
       min_dist:            The distance from the winning pos
    ______________________
    Input Variables:
        win_pos:            The winning position as (row, col)
        white_locations:    The list of white piece postions
    """

    """ Just for the sake of initial values"""
    min_piece = (9,9)
    min_dist = INFINITY

    """ Search through all the white pieces, work out how far away it is.
        If it's closer than the current min, reset the minimum values"""
    for white_loc in white_locations:
        local_min_dist = calc_man_dist(win_pos, white_loc)
        if local_min_dist < min_dist:
            min_piece = white_loc
            min_dist = local_min_dist

    return min_piece, min_dist

""" ************************************************************************* """

def calc_man_dist(piece, pos):
    """
    Calcuates the manhattan distance between 2 positions
    Returns:        int(Manhattan Distance, (|x1 - x2| + |y1 - y2|))
    __________________________
    Input Variabes:
        pos1:         First (row, col) tuple
        pos2:         Second (row, col) tuple
    """
    piece_i = piece[0]
    piece_j = piece[1]
    pos_i = pos[0]
    pos_j = pos[1]

    man_dist = (abs(piece_i - pos_i) + abs(piece_j - pos_j))

    return man_dist

""" ************************************************************************* """

def gen_winning_positions(board, black_locations):
    """
    Generates a list of the winning positions in the game
    Returns:                [[Position Pair], <(Single Pos)>]
    ________________________
    Input Variables:
        board:               The board array
        black_locations:     The list of the locations of black pieces
    """
    winning_pos = []
    winning_pair = []
    buffers = [(1,0), (-1,0), (0,1), (0,-1)]

    """ Loop through the black pieces positions and determine how to kill them"""
    for piece in black_locations:
        winning_pair = []
        piece_i = piece[0]
        piece_j = piece[1]

        """ Check all of the available killing places"""
        for i, killpos in enumerate(buffers):

            buffer_i = killpos[0]
            buffer_j = killpos[1]

            """ Clear the pair buffer if one of the positions in the first pair was invalid """
            if i == 2:
                winning_pair = []

            try:
                """ Check for corner pieces """
                if board[piece_i + buffer_i][piece_j + buffer_j] == "X":
                    winning_pair = []
                    winning_pos.append((piece_i - buffer_i, piece_j - buffer_j))

                    """ Check for other black pieces """
                elif board[piece_i + buffer_i][piece_j + buffer_j] == "@":
                    winning_pair = []

                    """ Ignore the presence of white pieces when building these sets """
                elif board[piece_i + buffer_i][piece_j + buffer_j] in "-O":
                    winning_pair.append((piece_i + buffer_i, piece_j + buffer_j))

                else:
                    pass

                """ Add each tuple pair to a list"""
                if len(winning_pair) == 2:
                    winning_pos.append(winning_pair)
                    winning_pair = []

                """ Reset if something goes wrong """
            except IndexError:
                winning_pair = []

    return winning_pos

""" ************************************************************************* """

def A_star_search(start, goal, white_locations, state):
    """ Implementation of the A* algorithm, based off the pseudocode from
        https://en.wikipedia.org/wiki/A*_search_algorithm.

        Remembering that:
            g(n) is defined as the total cost so far from the starting state
            h(n) is the estimated cost from the current state to the goal state (Manhattan Distance Heuristic)
            f(n) = h(n) + g(n)

    In this implementation we are using A* to find the best path for a piece to
    reach the goal position where it would be able to capture a black piece

    Returns:
        sequence:           The sequence of moves that A* took
        goal_state:         The board after A* finishes moving
    ________________________
    Input Variables:
        start:              The startng position of the white piece
        goal:               The goal position of the white piece
        white_locations:    The list of White Locations
        state:              The board array
    """

    goal_state = state
    """ List of available moves to a piece """
    buffers = [(1,0),(-1,0),(0,1),(0,-1)]

    nodes_to_explore = []
    nodes_searched = []

    g_n_scores = []

    """ Our first node is the initial state"""
    root_node = Node()

    root_node.state = start
    root_node.g_value = 0
    root_node.f_value = calc_man_dist(goal, start)
    root_node.children = []

    nodes_to_explore.append(root_node)

    """ Don't end until the goal has been found """
    while nodes_to_explore:
        for i, node in enumerate(nodes_to_explore, 0):

            """ Initialising the minimum values """
            if i == 0:
                curr_node = node
                min_f_value = node.f_value

            elif node.f_value <= min_f_value:
                curr_node = node
                min_f_value = node.f_value

            elif curr_node.state == goal:
                break

        """ Stop when the goal is reached """
        if curr_node.state == goal:
            break

        """ Mark node as searched """
        nodes_searched.append(curr_node.state)
        nodes_to_explore.remove(curr_node)

        """ Create the children nodes, if the nodes are valid """
        next_moves = []

        for move in buffers:
            valid = return_valid_move(state, white_locations, curr_node.state, move)

            if valid:
                next_moves.append(valid)

        """ Cycle through the next moves and determine the best move based on manhattan dist """
        for move in next_moves:
            new_child = Node()
            new_child.state = move

            if (curr_node.state[0] > goal[0]) or (curr_node.state[1] > goal[1]):

                new_child.g_value = ((new_child.state[0] - curr_node.state[0]) + (new_child.state[1] - curr_node.state[1]))

            elif (curr_node.state[0] < goal[0]) or (curr_node.state[1]  < goal[1]):
                new_child.g_value = ((curr_node.state[0] - new_child.state[0]) + (curr_node.state[1] - new_child.state[1]))


            new_child.f_value = calc_man_dist(move, goal) + new_child.g_value
            new_child.children = []

            curr_node.children.append(new_child)

        """ Loop through the child nodes and add them to the 'to be explored' list """
        for child in curr_node.children:

            if child.state in nodes_searched:
                pass

            elif child.state not in nodes_to_explore:
                nodes_to_explore.append(child)

            """ Set best neighbour for retracing the sequence """
            value_to_check = curr_node.f_value
            child.best_neighbour = curr_node

    node = curr_node
    sequence = [curr_node.state]

    """ Trace the sequence back from the goal state through the best neighbours """
    while node.state != start:

        node = node.best_neighbour
        sequence.append(node.state)

    """ Reverse the sequence """
    sequence = sequence[::-1]

    """ Mutate the board """
    goal_state[goal[0]][goal[1]] = "O"
    goal_state[start[0]][start[1]] = "-"

    return sequence, goal_state

""" ************************************************************************* """

def white_killed(state, new_pos):
    """
    Check if a potential white move will kill the white piece (to stop the move occurring)
    Returns:        True if white could be killed.
    ________________________
    Input Variables:
        state:      The Board Array as defined above
        new_pos:    The position white is trying to move to.
    """
    piece_i = new_pos[0]
    piece_j = new_pos[1]

    if piece_i == 0 or piece_i == 7:
        if ((state[piece_i][piece_j + 1] == "@") and (state[piece_i][piece_j - 1] == "@")) \
        or (state[piece_i][piece_j + 1] == "@") and (state[piece_i][piece_j - 1] == "X") \
        or (state[piece_i][piece_j + 1] == "X") and (state[piece_i][piece_j - 1] == "@"):

            """ Only need to check left and right of the piece"""

            if (piece_j - 2 < 0):
                pass
            else:
                piece_check = state[piece_i][piece_j - 2]

                if piece_check == "O":
                    return False

            try:
                piece_check = state[piece_i][piece_j + 2]

            except IndexError:
                piece_check = False

            if (piece_check == "O"):
                return False

            return True

    elif piece_j == 0 or piece_j == 7:
        if (state[piece_i + 1][piece_j] == "@") and (state[piece_i - 1][piece_j] == "@") \
        or (state[piece_i + 1][piece_j] == "X") and (state[piece_i - 1][piece_j] == "@") \
        or (state[piece_i + 1][piece_j] == "@") and (state[piece_i - 1][piece_j] == "X"):

            """ Only need to check above and below of the piece"""

            if (piece_i - 2 < 0):
                pass
            else:
                piece_check = state[piece_i - 2][piece_j]

                if piece_check == "O":
                    return False

            try:
                piece_check = state[piece_i + 2][piece_j]

            except IndexError:
                piece_check = False

            if (piece_check == "O"):
                return False

            return True

    else:


        if (state[piece_i][piece_j + 1] == "@") and (state[piece_i][piece_j - 1] == "@") \
        or (state[piece_i + 1][piece_j] == "@") and (state[piece_i - 1][piece_j] == "@"):

            """ Check left and right """

            if (piece_i - 2 < 0):
                pass
            else:
                piece_check = state[piece_i - 2][piece_j]

                if piece_check == "O":
                    return False

            try:
                piece_check = state[piece_i + 2][piece_j]
            except IndexError:
                piece_check = False

            if (piece_check == "O"):
                return False

            """ Check above and below"""

            if (piece_j - 2 < 0):
                pass
            else:
                piece_check = state[piece_i][piece_j - 2]

                if piece_check == "O":
                    return False

            try:
                piece_check = state[piece_i][piece_j + 2]
            except IndexError:
                piece_check = False

            if (piece_check == "O"):
                return False

            return True

    return False

""" ************************************************************************* """

def white_move(board, white, original_pos, new_pos):
    """
    Updated the board with the new position of the white piece, and remove it from it's old
    board position. Also update the white locations list.
    Returns:            Tuple(List(White Locations), New Board)
    ________________________
    Input Variables:
        board:          The board array as defined above
        white:          The list of white locations
        original_pos:   The original position of the white piece
        new_pos:        The position to move the piece to
    """
    white_pieces = white
    state = board

    state[original_pos[0]][original_pos[1]] = "-"
    state[new_pos[0]][new_pos[1]] = "O"

    for i in range(len(white_pieces)):
        if white_pieces[i] == original_pos:
            white_pieces[i] = new_pos

    return white_pieces, state

""" ************************************************************************* """

def check_state(board, black):
    """
    Checks if black pieces need to be removed (if they've been killed in the last move). Also updates the board.
    Returns:        Tuple(Alive Black Locations, The Board Array)
    ________________________
    Input Variables:
        board:       The Board Array as defined above.
        black:       The list of black locations.
    """
    alive = black
    state = board

    for piece in alive:
        piece_i = piece[0]
        piece_j = piece[1]

        """ Checking if a piece has been killed vertically"""
        if piece_i == 0 or piece_i == 7:
            if (state[piece_i][piece_j + 1] == "O") and (state[piece_i][piece_j - 1] == "O") \
            or (state[piece_i][piece_j + 1] == "O") and (state[piece_i][piece_j - 1] == "X") \
            or (state[piece_i][piece_j + 1] == "X") and (state[piece_i][piece_j - 1] == "O"):

                alive.remove(piece)
                state[piece_i][piece_j] = "-"

                """ Checking if a piece has been killed horizontally """
        elif piece_j == 0 or piece_j == 7:
            if (state[piece_i + 1][piece_j] == "O") and (state[piece_i - 1][piece_j] == "O") \
            or (state[piece_i + 1][piece_j] == "X") and (state[piece_i - 1][piece_j] == "O") \
            or (state[piece_i + 1][piece_j] == "O") and (state[piece_i - 1][piece_j] == "X"):

                alive.remove(piece)
                state[piece_i][piece_j] = "-"

                """ Last Check in case something funny has happened. """
        else:
            if (state[piece_i][piece_j + 1] == "O") and (state[piece_i][piece_j - 1] == "O") \
            or (state[piece_i + 1][piece_j] == "O") and (state[piece_i - 1][piece_j] == "O"):

                alive.remove(piece)
                state[piece_i][piece_j] = "-"

    return alive, state

""" ************************************************************************* """
