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

"""Determine the number of moves for each player """
def moves(board, locations):
	num_moves = 0
	buffers = [(1,0), (0,1), (-1,0), (0,-1)]
	
	for piece in locations:
		piece_moves = 0

		init_i = piece[0]
		init_j = piece[1]

		for moveset in buffers:

			buffer_i = moveset[0]
			buffer_j = moveset[1]

			try:
				position = board[init_i + buffer_i][init_j + buffer_j]
			except IndexError:
				position = None

			if ((init_i + buffer_i) < 0) or ((init_j + buffer_j) < 0):
				position = None

			if position == "-":
				piece_moves += 1

			elif position == "X":
				pass

			elif position == "O" or position == "@": 
				
				try:
					jump = board[init_i + buffer_i*2][init_j + buffer_j*2]
				except IndexError:
					jump = None

				if ((init_i + buffer_i*2) < 0) or ((init_j + buffer_j*2) < 0):
					jump = None

				if jump == "-":
					piece_moves += 1

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

