""" Transform the text board into an array  """
def prepare_board(board):
	board_array = []
	row = []

	for char in board:

		if char == "\n":
			board_array.append(row)
			row = []

		elif char != " ":
			row.append(char)

	return board_array

"""Determine locations of all the pieces of the board depending on the colour"""
def locations(board, player):
	location_array = []

	if player == "white":
		symbol = "O"
	else:
		symbol = "@"

	for i in range(len(board)):
		for j in range(len(board)):

			if board[i][j] == symbol:
				location_array.append((i,j))

	return location_array

def is_valid_move(board, locations, piece, move):

	move_i = move[0]
	move_j = move[1]

	piece_i = piece[0]
	piece_j = piece[1]

	try:
	# try and move the piece, moves outside the board are invalid.
		position = board[piece_i + move_i][piece_j + move_j]
	except IndexError:
		return False

	# Outside the board again,
	if ((piece_i + move_i) < 0) or ((piece_j + move_j) < 0):
		return False

	# One space moves are valid
	if position == "-":
		return True

	#Try jumping
	elif position == "X":
		pass

	elif position == "O" or position == "@":

		try:
			jump = board[piece_i + move_i*2][piece_j + move_j*2]
		except IndexError:
			return False

		if ((piece_i + move_i*2) < 0) or ((piece_j + move_j*2) < 0):
			return False

		if jump == "-":
			return True

	return False

"""Determine the number of moves for each player """
def moves(board, locations):
	num_moves = 0
	buffers = [(1,0), (0,1), (-1,0), (0,-1)]

	for piece in locations:
		piece_moves = 0

		for move in buffers:

			piece_moves += is_valid_move(board, locations, piece, move)

		num_moves += piece_moves

	return num_moves

def massacre(board, black, white):
	sequence = []




	return sequence

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
	white_moves = moves(board_as_array, white_locations)
	black_moves = moves(board_as_array, black_locations)
	print(str(white_moves) + "\n" + str(black_moves))

elif command.lower() == "massacre":
	#use massacre function
	print("massacre block")
