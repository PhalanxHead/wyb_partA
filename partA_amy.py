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

def is_valid_pos(board, locations, piece, move):
	"""
	Returns True if move is valid.
	_____________________
	Input Vars:
		board: 			The board array
		locations: 	  The list of piece locations
		piece:			 The location of the current piece
		move:			The direction you want to move in (as a (0,1) tuple)
	"""
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
		return (move_i + piece_i, move_j + piece_j)

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
			return (move_i + piece_i, move_j + piece_j)

	return False

"""Determine the number of moves for each player """
def moves(board, locations):
	possible_moves = []
	buffers = [(1,0), (0,1), (-1,0), (0,-1)]

	for piece in locations:
		piece_moves = []

		for move in buffers:

			poss_move = is_valid_pos(board, locations, piece, move)

			if poss_move:
				piece_moves.append(poss_move)

		possible_moves.append(piece_moves)

	return possible_moves

"""Check if any black pieces are surrounded on the board by the white pieces
	that we moved and hence need to be removed from the board, this also updates
	the black pieces that are alive"""
def check_state(board, black):
	alive = black
	state = board

	for piece in alive:
		piece_i = piece[0]
		piece_j = piece[1]

		if piece_i = 0 or piece_i = 7:
			if (state[piece_i][piece_j + 1] == "O") and (state[piece_i][piece_j - 1] == "O") // 
			or (state[piece_i][piece_j + 1] == "O") and (state[piece_i][piece_j - 1] == "X") //
			or (state[piece_i][piece_j + 1] == "X") and (state[piece_i][piece_j - 1] == "O"):

				alive.remove(piece)
				state[piece_i][piece_j] = "-"

		elif piece_j = 0 or piece_j = 7:
			if (state[piece_i + 1][piece_j] == "O") and (state[piece_i - 1][piece_j] == "O") //
			or (state[piece_i + 1][piece_j] == "X") and (state[piece_i - 1][piece_j] == "O") //
			or (state[piece_i + 1][piece_j] == "O") and (state[piece_i - 1][piece_j] == "X"):
				
				alive.remove(piece)
				state[piece_i][piece_j] = "-"

		else:
			if (state[piece_i][piece_j + 1] == "O") and (state[piece_i][piece_j - 1] == "O") //
			or (state[piece_i + 1][piece_j] == "O") and (state[piece_i - 1][piece_j] == "O"):
				
				alive.remove(piece)
				state[piece_i][piece_j] = "-"

	return alive, state 

def massacre(board, black, white):
	sequence = []
	state = board
	alive_pieces = black
	white_location = white

	while alive_pieces:
		#generate a list of valid moves for white
		#choose move with minimum manhatten distance 
		#generate a list of position that white should reach in order to eliminate black pieces

		alive_pieces, state = check_state(board, black)



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
	#use massacre function
	print("massacre block")
