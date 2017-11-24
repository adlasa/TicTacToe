import copy

class Board:
	#Have to change so high schore matches computer
	X_WON = -1
	DRAW = 0
	O_WON = 1
	NOT_DONE = 2

	def __init__(self, playerPiece):
		self.board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
		self.playerPiece = playerPiece
		if self.playerPiece == 'x':
			self.computerPiece = 'o'
			Board.X_WON = -1
			Board.O_WON = 1
			self.computerTurn = True
		else:
			self.computerPiece = 'x'
			Board.X_WON = 1
			Board.O_WON = -1
			self.computerTurn = False

	def printBoard(self):
		#Print self.Board
		print('-------------')
		for i in range(3):
			for j in range(3):
				print(self.board[i][j], end='')
			print('')
		print('-------------')

	def checkPiece(self, piece, board):
		#Check row
		for i in range(3):
			row = True
			for j in range(3):
				if board[i][j] != piece:
					row = False
					break
			if row:
				return True
		#Check Column
		for j in range(3):
			column = True
			for i in range(3):
				if board[i][j] != piece:
					column = False
					break
			if column:
				return True
		#Check diagnols
		if board[0][0] == piece and board[1][1] == piece and board[2][2] == piece:
			return True
		if board[0][2] ==  piece and board[1][1] == piece and board[2][0] == piece:
			return True
		return False

	def isFull(self, board):
		full = True
		for i in range(3):
			for j in range(3):
				if board[i][j] == ' ':
					full = False
		return full

	def evaluate(self, board):
		#Return -1 X's, 0 Draw, 1 O's, 2 for not done
		if self.checkPiece('x', board):
			return Board.X_WON
		elif self.checkPiece('o', board):
			return Board.O_WON
		#Check if self.board full
		if self.isFull(board):
			return Board.DRAW
		return Board.NOT_DONE

	def makeMove(self, x, y):
		#Return true if allowed, false if not
		if x >= 0 and x < 3 and y >= 0 and y < 3 and self.board[x][y] == ' ':
			if self.computerTurn:
				self.board[x][y] = self.computerPiece
			else:
				self.board[x][y] = self.playerPiece
		else:
			return False
		self.computerTurn = not self.computerTurn
		return True

	def getAllMoves(self, board):
		moves = list()
		for i in range(3):
			for j in range(3):
				if board[i][j] == ' ':
					moves.append(tuple([i, j]))
		return moves

	def negamax(self, board, turn):
		evaluation = self.evaluate(board)
		#If board is complete return evaluation
		if evaluation != Board.NOT_DONE:
			if evaluation == Board.DRAW:
				return 0
			return evaluation * turn

		maxEval = -100 #inf
		moves = self.getAllMoves(board)
		for move in moves:
			if turn == 1:
				board[move[0]][move[1]] = self.computerPiece
			else:
				board[move[0]][move[1]] = self.playerPiece

			value = -self.negamax(copy.deepcopy(board), turn*-1)
			if value > maxEval:
				maxEval = value
			board[move[0]][move[1]] = ' '
		return maxEval

	def computerMove(self):
		moves = self.getAllMoves(self.board)
		maxEval = -100
		bestMove = tuple([0,0])
		for move in moves:
			self.board[move[0]][move[1]] = self.computerPiece
			value = -self.negamax(copy.deepcopy(self.board), -1)
			if value > maxEval:
				bestMove = move
				maxEval = value
			self.board[move[0]][move[1]] = ' '
		self.makeMove(bestMove[0], bestMove[1])

def game():
	playerPiece = input('Welcome to tick tack toe. Please enter your piece choice, either x or o: ')
	board = Board(playerPiece)
	while board.evaluate(board.board) == Board.NOT_DONE:
		board.printBoard()
		if not board.computerTurn:
			x = int(input('X coord: '))
			y = int(input('Y coord: '))
			while not board.makeMove(x, y):
				print('Invalid move')
				x = int(input('X coord: '))
				y = int(input('Y coord: '))
		else:
			board.computerMove()
	board.printBoard()
	evaluation = board.evaluate(board.board)
	playAgain = False
	if (playerPiece == 'x' and evaluation == Board.X_WON) or (playerPiece == 'o' and evaluation == Board.O_WON):
		playAgain = int(input('You won! Enter 1 to play again, 0 to quit: '))
	elif evaluation == Board.DRAW:
		playAgain = int(input('It\'s a draw! Enter 1 to play again, 0 to quit: '))
	else:
		playAgain = int(input('You lost! Enter 1 to play again, 0 to quit: '))
	if playAgain == 1:
		return True
	else:
		return False

if __name__ == '__main__':
	playAgain = True
	while playAgain:
		playAgain = game()