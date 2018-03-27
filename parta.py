"""
Part A of the 2018 AI Assignment
Alistair Moffat Appreciation Society
Amy Rieck and Luke Hedt
16/03/2018 - 30/03/2018
"""
from moves_lib import *
from massacre_lib import *

def prepare_board(board):
    """
    Transforms the text board into an array.
    Returns:         board_array - A 2D array of the characters in the board.
    ________________________
    Input Variables:
        board:         A String representing the board as defined in the spec.
    """
    board_array = []
    row = []

    for char in board:

        if char == "\n":
            board_array.append(row)
            row = []

            """ Ignore Spaces """
        elif char != " ":
            row.append(char)

    return board_array

def locations(board, player):
    """
    Determines locations of all the pieces on the board depending on the colour.
    Returns:         List(Tuple(Piece Location))
    ________________________
    Input Variables:
        board:         The board array as above.
        player:         "white" or "black", allowing piece selection.
    """
    location_array = []

    if player == "white":
        symbol = "O"
    else:
        symbol = "@"

    """ Visit Every Space on the board """
    for i in range(len(board)):
        for j in range(len(board)):

            if board[i][j] == symbol:
                location_array.append((i,j))

    return location_array

"""
******************** MAIN **************************
"""

"""Preprocessing the board """
board = ""
rowcount = 0

while (rowcount < 9):
    row = input()

    if rowcount != 8:
        board += (row + "\n")
    else:
        command = row

    rowcount += 1


"""Represent the board as a matrix """
board_as_array = prepare_board(board)

"""Determine the locations of each piece on the board """
white_locations = locations(board_as_array, "white")
black_locations = locations(board_as_array, "black")

"""Based on what is given to us in stdin we either calculate the number of legal
    moves for each of the players, or we perform MASSACRE!, finding sequence of
    moves for white that will cleaar the board"""
if command.lower() == "moves":
    white_moves = command_moves(board_as_array, white_locations)
    black_moves = command_moves(board_as_array, black_locations)

    total_white = 0
    total_black = 0

    for i in range(len(white_moves)):
        total_white += len(white_moves[i])

    for i in range(len(black_moves)):
        total_black += len(black_moves[i])

    print(str(total_white) + "\n" + str(total_black))

    #print(white_moves)
    #print(black_moves)

elif command.lower() == "massacre":
    final_sequence = massacre(board_as_array, black_locations, white_locations)

    print(final_sequence)

    #for move in final_sequence:
    #    print(str(move[0]) + " -> " + str(move[1]))
