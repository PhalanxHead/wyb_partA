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

def return_valid_move(board, locations, piece, move):
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

def gen_winning_positions(board, black_locations):
	"""
	Generates a list of the winning positions in the game
	[[Position Pair], (Single Pos)]
	________________________
	Input Variables:
		board: The board array
		black_locations: The list of the locations of black pieces
	"""
	winning_pos = []
	winning_pair = []
	winning_buffer = []
	buffers = [(1,0), (-1,0), (0,1), (0,-1)]

	""" Loop through the black pieces positions and determine how to kill them"""
	for piece in black_locations:

		piece_i = piece[0]
		piece_j = piece[1]

		""" Check all of the available killing places"""
		for killpos in buffers:

			buffer_i = killpos[0]
			buffer_j = killpos[1]

			""" Check for corners"""
			try:
				if board[piece_i + buffer_i][piece_j + buffer_j] == "X":
					winning_pair = []
					winning_buffer = []
					winning_pos.append((piece_i - buffer_i, piece_j - buffer_j))

				""" Check for other black pieces"""
				elif board[piece_i + buffer_i][piece_j + buffer_j] == "@":
					winning_pair = []
					winning_buffer = []

				""" Ignore White pieces in building these sets"""
				elif board[piece_i + buffer_i][piece_j + buffer_j] in "-O":
					winning_pair.append((piece_i + buffer_i, piece_j + buffer_j))

				else:
					pass

				""" Add each tuple pair to a list"""
				if len(winning_pair) == 2:
					winning_buffer.append(winning_pair)
					winning_pair = []

				""" Add each list pair to a list"""
				if len(winning_buffer) == 2:
					winning_pos.append(winning_buffer)
					winning_pair = []
					winning_buffer = []

			except IndexError:
				winning_pair = []
				winning_buffer = []

	return winning_pos


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


""" Check if a potential white move will kill the white piece, we also need to check
	though if there are white pieces on opposite sides of the black, as this will
	result in killing the black pieces instead due to white having precedence"""
def white_killed(state, new_pos):
	piece_i = new_pos[0]
	piece_j = new_pos[1]

	if piece_i == 0 or piece_i == 7:
		if ((state[piece_i][piece_j + 1] == "@") and (state[piece_i][piece_j - 1] == "@")) //
		or (state[piece_i][piece_j + 1] == "@") and (state[piece_i][piece_j - 1] == "X") //
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

	elif piece_j == 0 or piece_j == 7:
		if (state[piece_i + 1][piece_j] == "@") and (state[piece_i - 1][piece_j] == "@") //
		or (state[piece_i + 1][piece_j] == "X") and (state[piece_i - 1][piece_j] == "@") //
		or (state[piece_i + 1][piece_j] == "@") and (state[piece_i - 1][piece_j] == "X"):

			""" Only need to check above and below of the piece"""

			if (piece_i - 2 < 0):
				pass
			else:
				piece_check = state[piece_i - 2][piece_j]

				if piece_check == "O":
					return False

			try:
				piece_check = state[piece_i + 2][piece_j]:

			except IndexError:
				piece_check = False

			if (piece_check == "O"):
				return False

	else:
		if (state[piece_i][piece_j + 1] == "@") and (state[piece_i][piece_j - 1] == "@") //
		or (state[piece_i + 1][piece_j] == "@") and (state[piece_i - 1][piece_j] == "@"):\

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


""" Update the board with the new position of the white piece and remove the piece
	from its old position on the board. Also update the white locations list """
def white_move(board, white, original_pos, new_pos):
	white_pieces = white
	state = board

	state[original_pos[0]][original_pos[1]] = "-"
	state[new_pos[0]][new_pos[1]] = "O"

	for i in range(len(white_pieces)):
		if white_pieces[i] == original_pos:
			white_pieces[i] = new_pos

	return white_pieces, state


def calc_man_dist(piece, pos):
	"""
	Calcuates the manhattan distance between 2 positions
	Returns: Manhattan Distance (int)
	__________________________
	Input Variabes:
		pos1: First (col, row) tuple
		pos2: Second (col, row) tuple
	"""
	piece_i = piece[0]
	piece_j = piece[1]
	pos_i = pos[0]
	pos_j = pos[1]

	man_dist = (abs(piece_i - pos_i) + abs(piece_j - pos_j))

	return man_dist


def get_min_manhattan_dist(board, white_locations, winning_pos):
	"""
	Calculates the manhattan distance between white pieces and current  winning positions.
	Returns: List(Optimal Piece 1 Location, Optimal Piece 2 Location, Sum of their Manhattan Distances)
	______________________
	Input Variables:
		board: 							The board array
		white_locations:		The location list of all  the white pieces
		winning_pos: 			The list of all the winning pairs.
	"""

	""" Just for the sake of initial values"""
	min_dist1 = [(9,9),(9,9),100]
	min_dist2 = [(9,9),(9,9),100]

	for piece in white_locations:
		piece_i = piece[0]
		piece_j = piece[1]

		""" The winning positions are formatted kind of annoyingly for this purpose"""
		for pos_quad in winning_pos:

			if isinstance(pos_quad, list):
				for pos_pair in pos_quad:

					if isinstance(pos_pair, list):
						for pos in pos_pair:

							man_dist = calc_man_dist(piece, pos)

							if man_dist < min_dist1[2]:
								min_dist1 = [piece, pos, man_dist]
							elif man_dist < min_dist2[2]:
								min_dist2 = [piece, pos, man_dist]

					""" Must otherwise be a tuple"""
					else:
						man_dist = calc_man_dist(piece, pos)

						if man_dist < min_dist1[2]:
							min_dist1 = [piece, pos, man_dist]
						elif man_dist < min_dist2[2]:
							min_dist2 = [piece, pos, man_dist]

			""" Also Must otherwise be a tuple """
			else:
				man_dist = calc_man_dist(piece, pos)

				if man_dist < min_dist1[2]:
					min_dist1 = [piece, pos, man_dist]
				elif man_dist < min_dist2[2]:
					min_dist2 = [piece, pos, man_dist]

	return [min_dist_1[0], min_dist2[0], min_dist_1[2] + min_dist2[2]]

""" Generates a list of which black pieces on the board can be killed during
	the current game state """
def black_to_kill(board, black_locations):
	can_kill = []

	for piece in black_locations:
		piece_i = black_locations[i][0]
		piece_j = black_locations[i][1]

		kill = False

		if (piece_i == 0) or (piece_i == 7):
			if (board[piece_i + 1][piece_j] != "@" and board[piece_i - 1][piece_j] != "@"):
				kill = [(piece_i + 1, piece_j), (piece_i - 1, piece_j)]

		elif (piece_j == 0) or (piece_j == 7):
			if (board[piece_i[piece_j + 1]] != "@" and board[piece_i][piece_j - 1] != "@"):
				kill = [(piece_i, piece_j + 1, (piece_i, piece_j - 1))]
		else:
			if (board[piece_i[piece_j + 1]] != "@" and board[piece_i][piece_j - 1] != "@"):
				kill = [(piece_i, piece_j + 1, (piece_i, piece_j - 1))]

			elif (board[piece_i + 1][piece_j] != "@" and board[piece_i - 1][piece_j] != "@")
				kill = [(piece_i + 1, piece_j), (piece_i - 1, piece_j)]

		can_kill.append(kill)

	return can_kill
	
""" Need to pick which black piece to kill based off which black pieces are
	killable in the current game state and the minimum distance between
	white pieces and the said black piece. Black piece with the closest white
	pieces is selected."""
def white_pieces(board, black_kill, white_locations, black_locations):
	black_to_kill = None
	white_1_orig = None
	white_2_orig = None

	min_distance = None

	for i in range(len(black_kill)):
		if black_kill[i]:
			white_1_goal = black_kill[i][0]
			white_2_goal = black_kill[i][1]

			optimal1, optimal2, dist = get_min_manhattan_dist()

			if dist < min_distance:

				min_distance = dist
				black_to_kill = black_locations[i]
				white_1_orig = optimal1
				white_2_orig = optimal2

	return white1_orig, white1_new, white2_orig, white2_new
	
""" Massacre function """
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
	print(gen_winning_positions(board_as_array, black_locations))
