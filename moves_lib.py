"""
Library for partA.py
Alistair Moffat Appreciation Society
Amy Rieck and Luke Hedt
26/03/2018
"""

def command_moves(board, locations):
    """
    Determines the number of moves for a set of piece locations.
    Returns:        List(Tuple(A possible move)).
    ________________________
    Input Variables:
        board:           The board array as defined above.
        locations:       A list of all the locations to try moves for.
    """
    possible_moves = []
    buffers = [(1,0), (0,1), (-1,0), (0,-1)]

    for piece in locations:
        piece_moves = []

        for move in buffers:

            poss_move = return_valid_move(board, locations, piece, move)

            if poss_move:
                piece_moves.append(poss_move)

        possible_moves.append(piece_moves)

    return possible_moves

""" ************************************************************************* """

def return_valid_move(board, locations, piece, move):
    """
    Returns:             A tuple of the new location if move is valid.
    ________________________
    Input Variables:
        board:             The board array
        locations:           The list of piece locations
        piece:            The location of the current piece
        move:            The direction you want to move in (as a (0,1) tuple)
    """
    move_i = move[0]
    move_j = move[1]

    piece_i = piece[0]
    piece_j = piece[1]

    try:
        """ Try and move the piece, moves outside the board are invalid."""
        position = board[piece_i + move_i][piece_j + move_j]
    except IndexError:
        return False

    """ Outside the board again """
    if ((piece_i + move_i) < 0) or ((piece_j + move_j) < 0):
        return False

    """ One space moves are valid if there are no pieces in the way"""
    if position == "-":
        return (move_i + piece_i, move_j + piece_j)

        """ Can't move into a corner """
    elif position == "X":
        pass

        """ Try jumping """
    elif position == "O" or position == "@":

        try:
            move_i *=2
            move_j *=2
            jump = board[piece_i + move_i][piece_j + move_j]
        except IndexError:
            return False

        if ((piece_i + move_i) < 0) or ((piece_j + move_j) < 0):
            return False

        if jump == "-":
            return (move_i + piece_i, move_j + piece_j)

    return False
