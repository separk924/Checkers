"""
This Checkers player uses the minimax algorithm to find the optimal disc
placement according to the number of plies designated by difficulty_level.
********************************************************************************
********    This Checkers player uses alpha-beta pruning, and can be    ********
********    can be turned on/off by changing the self.ab attribute to   ********
********                            to False.                           ******** 
********************************************************************************
"""
__author__ = "Seung Park"
__license__ = "University of Puget Sound"
__date__ = "May 10, 2023"

################################################################
######### IMPORTS
################################################################
import math, copy
from checkersPiece import Piece

class Player():

    '''
    Constructor, takes a player ID that's either 1 or 3 that tells whether the player
    is the computer or human player, a difficulty level (# of plies to look ahead),
    and the color of the player's pieces
    '''
    def __init__(self, id, difficulty_level):
        # id=1 for computer, id=2 for human
        self.id = id
        self.difficulty_level = difficulty_level
        self.num_discs = 0
        self.discs = []
        self.ab = True
    
    '''
    This function takes a board and the other player and returns the location of where
    to place the chosen piece, the chosen piece, the old location of the chosen piece, and
    the removed disc (if there is any)
    :param board: The board
    :param other_player: The other player
    :return: The location of where to place the chosen piece
    '''
    def pick_move(self, board, other_player):
        location, thePiece, value, oldLoc, removedDisc = self.minimax(board, self, other_player, self.difficulty_level, -math.inf, math.inf, self.ab)
        print("The computer chose to move this piece:",thePiece.id)
        print("To location:", location)
        print()
        if board.matrix[location[0]][location[1]] == '--':
            return location, thePiece, oldLoc, removedDisc
    
    '''
    This function takes a board, the player, the other player, the number of plies, the alpha
    number, the beta number, and whether alpha-beta pruning is enabled. This function performs
    the minimax algorithm and returns the best move to make according to the number of plies.
    :param board: the board
    :param player: the current player
    :param other_player: the other player
    :param difficulty: the number of plies to look ahead
    :param alpha: the alpha number
    :param beta: the beta number
    :param ab: is alpha-beta pruning enabled
    :return: the best move to make according to the number of plies
    '''
    def minimax(self, board, player, other_player, difficulty, alpha, beta, ab):
        
        if difficulty == 0:
            return None, None, self.heuristic(board), [0,0], None
        if self.gameDone(board, player):
            return None, None, self.heuristic(board), [0,0], None
        
        # AI
        if player.id == 1:
            value = -math.inf
            location = []
            for row in range(len(board.matrix)):
                for column in range(len(board.matrix[0])):
                    oldLoc = [row, column]
                    # Checks if the location has one of the computer's discs
                    if board.matrix[row][column]!= '--' and board.matrix[row][column].status >= 1:
                        locations = self.moveDiagonal(board, column, row, board.matrix[row][column])
                        locations += self.hop(board, column, row, board.matrix[row][column])
                        
                        # makes sure there are available locations
                        if len(locations) != 0:
                            thePiece = board.matrix[row][column]
                            
                            # Check all valid moves for the disc at board[row][column]
                            for loc in board.matrix[row][column].moves:
                                boardCopy = copy.deepcopy(board)
                                removedDisc = None
                                location = loc
                                
                                # moving the disc to potential location
                                tmp = copy.deepcopy(boardCopy.matrix[row][column])
                                boardCopy.matrix[loc[0]][loc[1]] = tmp
                                boardCopy.matrix[row][column] == '--'
                                
                                # If piece becomes "kinged"
                                kinged = False
                                if loc[0] == len(boardCopy.matrix)-1:
                                    if tmp.status == 1:
                                        self.make_king(tmp)
                                        kinged = True
                                
                                # if the player's disc hopped, remove the opponent's disc
                                if loc[0]-row <= -2 and loc[1]-column <= -2:
                                    removedDisc, removedRow, removedCol = self.removeOpponentDisc(boardCopy, row-1, column-1)
                                if loc[0]-row >= 2 and loc[1]-column >= 2:
                                    removedDisc, removedRow, removedCol = self.removeOpponentDisc(boardCopy, row+1, column+1)
                                if loc[0]-row <= -2 and loc[1]-column >= 2:
                                    removedDisc, removedRow, removedCol = self.removeOpponentDisc(boardCopy, row-1, column+1)
                                if loc[0]-row >= 2 and loc[1]-column <= -2:
                                    removedDisc, removedRow, removedCol = self.removeOpponentDisc(boardCopy, row+1, column-1)
                                
                                # calculate other scores for other states
                                newScore = self.minimax(boardCopy, other_player, player, difficulty-1, alpha, beta, ab)[2]
                                
                                # Put things back
                                temp = boardCopy.matrix[loc[0]][loc[1]]
                                boardCopy.matrix[loc[0]][loc[1]] = '--'
                                boardCopy.matrix[row][column] = temp
                                if removedDisc != None:
                                    boardCopy.matrix[removedRow][removedCol] = removedDisc
                                if kinged:
                                    temp.status = 1
                                
                                # update better score
                                if newScore > value:
                                    value = newScore
                                    location = loc
                                    thePiece = boardCopy.matrix[row][column]
                                    
                                if(ab):
                                    alpha = max(alpha, value)
                                    if alpha >= beta:
                                        break
                                    
                            return location, thePiece, value, oldLoc, removedDisc
        # HUMAN
        if player.id == 2:
            value = -math.inf
            location = []
            for row in range(len(board.matrix)):
                for column in range(len(board.matrix[0])):
                    oldLoc = [row, column]
                    # Checks if the location has one of the computer's discs
                    if board.matrix[row][column]!= '--' and board.matrix[row][column].status <= -1:
                        locations = self.moveDiagonal(board, column, row, board.matrix[row][column])
                        locations += self.hop(board, column, row, board.matrix[row][column])
                        
                        # makes sure there are available locations
                        if len(locations) != 0:
                            thePiece = board.matrix[row][column]
                            
                            # Check all valid moves for the disc at board[row][column]
                            for loc in board.matrix[row][column].moves:
                                boardCopy = copy.deepcopy(board)
                                removedDisc = None
                                
                                # moving the disc to potential location
                                tmp = copy.deepcopy(boardCopy.matrix[row][column])
                                boardCopy.matrix[row][column] = '--'
                                boardCopy.matrix[loc[0]][loc[1]] = tmp
                                
                                # If piece becomes "kinged"
                                kinged = False
                                if loc[0] == 0:
                                    if tmp.status == -1:
                                        self.make_king(tmp)
                                        kinged = True
                                
                                # if the player's disc hopped, remove the opponent's disc
                                if loc[0]-row <= -2 and loc[1]-column <= -2:
                                    removedDisc, removedRow, removedCol = self.removeOpponentDisc(boardCopy, row-1, column-1)
                                if loc[0]-row >= 2 and loc[1]-column >= 2:
                                    removedDisc, removedRow, removedCol = self.removeOpponentDisc(boardCopy, row+1, column+1)
                                if loc[0]-row <= -2 and loc[1]-column >= 2:
                                    removedDisc, removedRow, removedCol = self.removeOpponentDisc(boardCopy, row-1, column+1)
                                if loc[0]-row >= 2 and loc[1]-column <= -2:
                                    removedDisc, removedRow, removedCol = self.removeOpponentDisc(boardCopy, row+1, column-1)
                                    
                                
                                # calculate other scores for other states
                                newScore = self.minimax(boardCopy, other_player, player, difficulty-1, alpha, beta, ab)[2]
                                
                                # Put things back
                                temp = boardCopy.matrix[loc[0]][loc[1]]
                                boardCopy.matrix[row][column] = temp
                                boardCopy.matrix[loc[0]][loc[1]] = '--'
                                if removedDisc != None:
                                    boardCopy.matrix[removedRow][removedCol] = removedDisc
                                if kinged:
                                    tmp.status = 1
                                
                                if newScore < value:
                                    value = newScore
                                    location = loc
                                    thePiece = board.matrix[row][column]
                                    
                                if(ab):
                                    alpha = min(beta, value)
                                    if alpha >= beta:
                                        break
                                    
                            return location, thePiece, value, oldLoc, removedDisc
    
    '''
    This function  checks to see whether one color remains or if there are any more 
    legal moves you can make
    :param board: current game state
    :param player: the player id
    :return: True if the game is done, False if the player has no more discs or if they
             have no more valid moves
    '''
    def gameDone(self, board, player):
        
        # If the player has any pieces left on the board
        if player.num_discs == 0:
            return True
        
        # Check if player can move
        if self.isLegalMoveLeft(board, player):
            return False
        elif self.isTie(board):
            return True
        else: 
            return True
        
    '''
    This function checks to see whether a player can move or not
    :param board: current game state
    :param player: the player
    :return: True if the player can move
    '''
    def isLegalMoveLeft(self, board, player):
        for row in range(len(board.matrix)):
            for column in range(len(board.matrix[0])):
                if player.id == 1:
                    if board.matrix[row][column] != '--' and board.matrix[row][column].status >= 1:
                        if len(self.moveDiagonal(board, column, row, board.matrix[row][column])) > 0 or len(self.hop(board, column, row, board.matrix[row][column])) > 0:
                            return True
                if player.id == 2:
                    if board.matrix[row][column] != '--' and board.matrix[row][column].status <= -1:
                        if len(self.moveDiagonal(board, column, row, board.matrix[row][column])) > 0 or len(self.hop(board, column, row, board.matrix[row][column])) > 0:
                            return True
        return False
    
    '''
    This function checks to see whether a player can move or not
    :param board: current game state
    :param player: the player
    :return: True if the game is a tie
    '''
    def isTie(self, board):
        isTie = True
        for row in range(len(board.matrix)):
            for column in range(len(board.matrix[0])):
                if board.matrix[row][column] != '--' and board.matrix[row][column].status >= 1:
                    if len(self.moveDiagonal(board, column, row, board.matrix[row][column])) > 0 or len(self.hop(board, column, row, board.matrix[row][column])) > 0:
                        isTrue = False
                if board.matrix[row][column] != '--' and board.matrix[row][column].status <= -1:
                    if len(self.moveDiagonal(board, column, row, board.matrix[row][column])) > 0 or len(self.hop(board, column, row, board.matrix[row][column])) > 0:
                        isTrue = False
        return isTie
            
        
    '''
    This function takes a checkers baord, the column and row of a specific checkers
    piece. It then checks the piece's diagonal locations and checks if it's open. If it
    is, add it to the list of possible locations to move to.
    :param board: The board
    :param column: The column index
    :param row: The row index
    :param piece: The piece to move
    :return: A list of all possible locations to move to
    '''
    def moveDiagonal(self, board, column, row, piece):
        # if piece is kinged
        if piece.status > 1 or piece.status < -1:
            canMove = []
            if row-1 >= 0 and column-1 >= 0:
                if board.matrix[row-1][column-1] == '--':
                    loc = [row-1, column-1]
                    canMove.append(loc)
            if row-1 >= 0 and column+1 < len(board.matrix[0]):
                if board.matrix[row-1][column+1] == '--':
                    loc = [row-1, column+1]
                    canMove.append(loc)
            if row+1 < len(board.matrix) and column-1 >= 0:
                if board.matrix[row+1][column-1] == '--':
                    loc = [row+1, column-1]
                    canMove.append(loc)
            if row+1 < len(board.matrix) and column+1 < len(board.matrix[0]):
                if board.matrix[row+1][column+1] == '--':
                    loc = [row+1, column+1]
                    canMove.append(loc)
            piece.moves += canMove
            return canMove
        # if piece is not kinged yet
        else:
            if piece.status == 1:
                canMove = []
                if row+1 < len(board.matrix) and column+1 < len(board.matrix[0]):
                    if board.matrix[row+1][column+1] == '--':
                        loc = [row+1, column+1]
                        canMove.append(loc)
                if row+1 < len(board.matrix) and column-1 >= 0:
                    if board.matrix[row+1][column-1] == '--':
                        loc = [row+1, column-1]
                        canMove.append(loc)
                piece.moves += canMove
                return canMove
            if piece.status == -1:
                canMove = []
                if row-1 >= 0 and column-1 >= 0:
                    if board.matrix[row-1][column-1] == '--':
                        loc = [row-1, column-1]
                        canMove.append(loc)
                if row-1 >= 0 and column+1 < len(board.matrix[0]):
                    if board.matrix[row-1][column+1] == '--':
                        loc = [row-1, column+1]
                        canMove.append(loc)
                piece.moves += canMove
                return canMove
    
    '''
    This function takes a checkers baord, the column and row of a specific checkers
    piece. It then checks if the piece can hop over another piece. This function then
    returns a list of all possible hopping locations
    :param board: The board
    :param column: The column index
    :param row: The row index
    :param piece: The piece to move
    :return: A list of all possible hopping locations
    '''
    def hop(self, board, column, row, piece):
        
        canHop = []
        # if piece is kinged
        if piece.status > 1 or piece.status < -1:
            if piece.status > 1:
                if row-2 >= 0 and column-2 >= 0:
                    if board.matrix[row-1][column-1] != '--' and board.matrix[row-1][column-1].status <= -1 and board.matrix[row-2][column-2] == '--':
                        loc = [row-2, column-2]
                        canHop.append(loc)
                if row+2 < len(board.matrix)-1 and column-2 >= 0:
                    if board.matrix[row+1][column-1] != '--' and board.matrix[row+1][column-1].status <= -1 and board.matrix[row+2][column-2] == '--':
                        loc = [row+2, column-2]
                        canHop.append(loc)
                if row+2 < len(board.matrix)-1 and column+2 < len(board.matrix[0])-1:
                    if board.matrix[row+1][column+1] != '--' and board.matrix[row+1][column+1].status <= -1 and board.matrix[row+2][column+2] == '--':
                        loc = [row+2, column+2]
                        canHop.append(loc)
                if row-2 >= 0 and column+2 < len(board.matrix[0])-1:
                    if board.matrix[row-1][column+1] != '--' and board.matrix[row-1][column+1].status <= -1 and board.matrix[row-2][column+2] == '--':
                        loc = [row-2, column+2]
                        canHop.append(loc)
                piece.moves += canHop
                return canHop
            if piece.status < -1:
                if row-2 >= 0 and column-2 >= 0:
                    if board.matrix[row-1][column-1] != '--' and board.matrix[row-1][column-1].status >= 1 and board.matrix[row-2][column-2] == '--':
                        loc = [row-2, column-2]
                        canHop.append(loc)
                if row+2 < len(board.matrix)-1 and column-2 >= 0:
                    if board.matrix[row+1][column-1] != '--' and board.matrix[row+1][column-1].status >= 1 and board.matrix[row+2][column-2] == '--':
                        loc = [row+2, column-2]
                        canHop.append(loc)
                if row+2 < len(board.matrix)-1 and column+2 < len(board.matrix[0])-1:
                    if board.matrix[row+1][column+1] != '--' and board.matrix[row+1][column+1].status >= 1 and board.matrix[row+2][column+2] == '--':
                        loc = [row+2, column+2]
                        canHop.append(loc)
                if row-2 >= 0 and column+2 < len(board.matrix[0])-1:
                    if board.matrix[row-1][column+1] != '--' and board.matrix[row-1][column+1].status >= 1 and board.matrix[row-2][column+2] == '--':
                        loc = [row-2, column+2]
                        canHop.append(loc)
                piece.moves += canHop
                return canHop
            # if piece is not kinged yet
        else:
            if piece.status == 1:
                if row+2 < len(board.matrix)-1 and column+2 < len(board.matrix[0])-1:
                    if board.matrix[row+1][column+1] != '--' and board.matrix[row+1][column+1].status <= -1 and board.matrix[row+2][column+2] == '--':
                        loc = [row+2, column+2]
                        canHop.append(loc)
                if row+2 <= len(board.matrix)-1 and column-2 >= 0:
                    if board.matrix[row+1][column-1] != '--' and board.matrix[row+1][column-1].status <= -1 and board.matrix[row+2][column-2] == '--':
                        loc = [row+2, column-2]
                        canHop.append(loc)
                piece.moves += canHop
                return canHop
            if piece.status == -1:
                if row-2 >= 0 and column-2 >= 0:
                    if board.matrix[row-1][column-1] != '--' and board.matrix[row-1][column-1].status >= 1 and board.matrix[row-2][column-2] == '--':
                        loc = [row-2, column-2]
                        canHop.append(loc)
                if row-2 >= 0 and column+2 <= len(board.matrix)-1:
                    if board.matrix[row-1][column+1] != '--' and board.matrix[row-1][column+1].status >= 1 and board.matrix[row-2][column+2] == '--':
                        loc = [row-2, column+2]
                        canHop.append(loc)
                piece.moves += canHop
                return canHop
    
    '''
    This function takes a Checkers board, the index of the new piece location, the index
    of the old piece location, the piece to move, and whether the piece hopped or not.
    :param board: A Checkers board
    :param newRow: The new row
    :param newColumn: The new column
    :param oldRow: The old row
    :param oldColumn: The old column
    :param piece: The piece to move
    :param didHop: Whether the piece hopped or not
    '''
    def move(self, board, newRow, newColumn, oldRow, oldColumn, piece, didHop):
        if not didHop:
            board.matrix[newRow][newColumn] = piece
            board.matrix[oldRow][oldColumn] = '--'
            if piece.status == 1:
                if newRow == len(board.matrix)-1:
                    self.make_king(piece)
            if piece.status == -1:
                if newRow == 0:
                    self.make_king(piece)         
        else:
            board.matrix[newRow][newColumn] = piece
            board.matrix[oldRow][oldColumn] = '--'
            if newRow-oldRow <= -2 and newColumn-oldColumn <= -2:
                self.removeOpponentDisc(board, oldRow-1, oldColumn-1)
            if newRow-oldRow >= 2 and newColumn-oldColumn >= 2:
                self.removeOpponentDisc(board, oldRow+1, oldColumn+1)
            if newRow-oldRow <= -2 and newColumn-oldColumn >= 2:
                self.removeOpponentDisc(board, oldRow-1, oldColumn+1)
            if newRow-oldRow >= 2 and newColumn-oldColumn <= -2:
                self.removeOpponentDisc(board, oldRow+1, oldColumn-1)
            if piece.status == 1:
                if newRow == len(board.matrix)-1:
                    self.make_king(piece)
            if piece.status == -1:
                if newRow == 0:
                    self.make_king(piece)
    
    '''
    This function takes a Checkers board, and the index of the removed disc and returns
    the removed disc with its row and column
    :param board: A Checkers board
    :param row: the row index of the removed disc
    :param column: the column index of the removed disc
    :return: The removed disc
    :return: The row of the removed disc
    :return: The column of the removed disc
    '''
    def removeOpponentDisc(self, board, row, column):
        removedDisc = board.matrix[row][column]
        board.matrix[row][column] = '--'
        return removedDisc, row, column
    
    """
    Calculate the heuristic value for a given board state. Evaluation score is 
    calculated using these heuristics:
        - Count the number of pieces each player has on the board (addition for the AI
        and subtraction for the human player).
        - If any pieces are "kinged", add/subtract an additional weight to the piece
        - The closer a piece is to the opposing side, add/subtract additional weight to 
        include how close the piece is to becoming "kinged"
    :param board: current game state
    :return: the heuristic value for the given player's game state
    """
    def heuristic(self, board):
        
        # additional weight for pieces that are closer to being kinged
        computer_weight = 0
        for row in range(len(board.matrix)):
            for col in range(len(board.matrix[row])):
                if isinstance(board.matrix[row][col], Piece) and board.matrix[row][col].status == 1:
                    computer_weight += 5 + ((len(board.matrix)-1) - row)
                elif isinstance(board.matrix[row][col], Piece) and board.matrix[row][col].status > 1:
                    computer_weight += 20  
        
        human_weight = 0
        for row in range(len(board.matrix)):
            for col in range(len(board.matrix[row])):
                if isinstance(board.matrix[row][col], Piece) and board.matrix[row][col].status == -1:
                    human_weight += 5 + row
                elif isinstance(board.matrix[row][col], Piece) and board.matrix[row][col].status < -1:
                    human_weight += 20

        return computer_weight - human_weight
    
    '''
    This function takes a Checkers piece and makes it "kinged"
    :param piece: the piece to make "kinged"
    '''
    def make_king(self, piece):
        if piece.status == 1:
            piece.status = 2
            piece.id += 'K'
            self.discs.append(piece.id)
        if piece.status == -1:
            piece.status = -2
            piece.id += 'K'
            self.discs.append(piece.id)