"""
This program creates a "Checkers" game. By default, one player will be human 
and the other player will be a computer player, whose AI is contained in the 
file "checkersPlayer.py". This will have a class called Player that contains
all of the functions required to play the game.
"""
__author__ = "Seung Park"
__license__ = "University of Puget Sound"
__date__ = "February 20, 2023"

################################################################
######### IMPORTS
################################################################
from checkersPiece import Piece
from checkersPlayer import Player

DEFAULT_AI_FILE = "checkersPlayer"
DEFAULT_COLUMNS = 8
DEFAULT_ROWS = 8
PLIES = 5
COMPUTER_PLAYER = 1
HUMAN_PLAYER = 2

class CheckerBoard():
    '''
    CONSTRUCTOR: This constructor takes in an the number of columns and number of
    rows. Has a matrix attribute
    :param columns: The number of columns
    :param rows: The number of rows
    '''
    def __init__(self, num_columns, num_rows):
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.matrix = []
    
    '''
    This function  checks to see whether one color remains or if there are any more 
    legal moves you can make
    :param board: current game state
    :param player: the player id
    :return: True if the game is done, False if the player has no more discs or if they
             have no more valid moves
    '''
    def gameDone(self, player):
        
        # If the player has any pieces left on the board
        if player.num_discs == 0:
            if player.id == 1:
                print("Congratulations! You won!")
            else:
                print("You Lost! Better luck playing a different game...")
            return True
        
        # Check if player can move
        if self.isLegalMoveLeft(player):
            return False
        elif self.isTie():
            print("It was a tie!")
            return True
        else: 
            if player.id == 1:
                print("Congratulations! You won!")
            else:
                print("You Lost! Better luck playing a different game...")
            return True
        
    '''
    This function checks to see whether a player can move or not
    :param player: the player id
    :return: True if the player can move, False otherwise
    '''
    def isLegalMoveLeft(self, player):
        for row in range(len(self.matrix)):
            for column in range(len(self.matrix[0])):
                if player.id == 1:
                    if self.matrix[row][column] != '--' and self.matrix[row][column].status >= 1:
                        if len(player.moveDiagonal(self, column, row, self.matrix[row][column])) > 0 or len(player.hop(self, column, row, self.matrix[row][column])) > 0:
                            return True
                if player.id == 2:
                    if self.matrix[row][column] != '--' and self.matrix[row][column].status <= -1:
                        if len(player.moveDiagonal(self, column, row, self.matrix[row][column])) > 0 or len(player.hop(self, column, row, self.matrix[row][column])) > 0:
                            return True
        return False
    
    '''
    This function checks to see whether a player can move or not
    :param board: current game state
    :param player: the player
    :return: True if the game is a tie
    '''
    def isTie(self):
        isTie = True
        for row in range(len(self.matrix)):
            for column in range(len(self.matrix[0])):
                if self.matrix[row][column] != '--' and self.matrix[row][column].status >= 1:
                    if len(self.moveDiagonal(self, column, row, self.matrix[row][column])) > 0 or len(self.hop(self, column, row, self.matrix[row][column])) > 0:
                        isTrue = False
                if self.matrix[row][column] != '--' and self.matrix[row][column].status <= -1:
                    if len(self.moveDiagonal(self, column, row, self.matrix[row][column])) > 0 or len(self.hop(self, column, row, self.matrix[row][column])) > 0:
                        isTrue = False
        return isTie
    
    '''
    This function takes the a row index, a column index, and the piece to place
    :param row: the row index
    :param column: the column index
    :param piece: the piece to place
    '''
    def placeDisc(self, row, column, piece):
        self.matrix[row][column] = piece
    
    '''
    This function takes the number of columns, and the number of rows. It then initializes 
    the board with '--' to represent an empty checkers board
    :param columns: The number of columns
    :param rows: The number of rows
    :return: The initial matrix of the Board
    '''
    def initializeBoard(self, columns, rows):
        matrix = [['--' for _ in range(columns)] for _ in range(rows)]
        return matrix
    
    '''
    This function takes the number of columns, the number of rows and the player
    id. It then iterates through the board and places the red and white pieces in the 
    correct initial place.
    :param columns: The number of columns
    :param rows: The number of rows
    :param player: The player
    :return: The created matrix
    '''
    def initDiscs(self, columns, rows, player):
        
        if player.id == 1:
            id = 1
            # iterate through the board and place the red pieces
            for i in range(rows):
                for j in range(columns):
                    if i % 2 != 0:
                        if j % 2 == 0:
                            newPiece = Piece('R', id, 1)
                            self.placeDisc(i, j, newPiece)
                            player.discs.append(newPiece.id)
                            player.num_discs += 1
                            id += 1
                    else:
                        if j % 2 != 0:
                            newPiece = Piece('R', id, 1)
                            self.placeDisc(i, j, newPiece)
                            player.discs.append(id)
                            player.num_discs += 1
                            id += 1
                
                if id >= 12: break
        else:
            id = 1
            # iterate through the board and place the white pieces
            for i in range(rows-1, 0, -1):
                for j in range(columns):
                    if i % 2 != 0:
                        if j % 2 == 0:
                            newPiece = Piece('B', id, -1)
                            self.placeDisc(i, j, newPiece)
                            player.discs.append(newPiece.id)
                            player.num_discs += 1
                            id += 1
                    else:
                        if j % 2 != 0:
                            newPiece = Piece('B', id, -1)
                            self.placeDisc(i, j, newPiece)
                            player.discs.append(newPiece.id)
                            player.num_discs += 1
                            id += 1
                
                if id >= 12: break
            
        return self.matrix
    
    '''
    This function builds the intial state of the board
    :param player1: The first player
    :param player2: The second player
    :return: The initial Board state
    '''
    def buildBoard(player1, player2):
        theBoard = CheckerBoard(DEFAULT_COLUMNS,DEFAULT_ROWS)
        theBoard.matrix = theBoard.initializeBoard(DEFAULT_COLUMNS,DEFAULT_ROWS)
        theBoard.matrix = theBoard.initDiscs(DEFAULT_COLUMNS,DEFAULT_ROWS, player1)
        theBoard.matrix = theBoard.initDiscs(DEFAULT_COLUMNS,DEFAULT_ROWS, player2)
        
        return theBoard
    
    '''
    This function takes itself and the board. It then prints the current state of the board
    '''
    def printBoard(self):
        print('   ', end='')
        for i, item in enumerate(self.matrix[0]):
            if i == len(self.matrix[0])-1:
                print(' ',i)
            else:
                print(' ',i, end='  ')
        print('   ', end='')
        for i, item in enumerate(self.matrix[0]):
            print('-----', end='')
        print('-')
        for i, elem in enumerate(self.matrix):
            print(i, end=' ')
            print("|", end=' ')
            for j, item in enumerate(elem):
                if item != '--' and len(item.id) == 2:
                    print(item.id, end='   ')
                elif item != '--' and len(item.id) == 3:
                    print(item.id, end='  ')
                elif item != '--' and len(item.id) == 4:
                    print(item.id, end=' ')
                else:
                    print(item, end='   ')
            print("|")
        print('   ', end='')
        for i, item in enumerate(self.matrix[0]):
            print('-----', end='')
        print('-')

################################################################################
# MAIN(): PARSE COMMAND LINE & START PLAYING
################################################################################
def main():
    computer_player = Player(COMPUTER_PLAYER, PLIES)
    human_player = Player(HUMAN_PLAYER, PLIES)
    theBoard = CheckerBoard.buildBoard(computer_player, human_player)
    # Intro to Game
    print("====================================================================================\n========================  WELCOME TO THE GAME OF CHECKERS!  ========================\n=============    If you need a refresher on how to play the game of    =============\n============  Checkers, make sure to check out this Wiki How article:   ============\n===================    https://www.wikihow.com/Play-Checkers      ==================\n====================================================================================\n==============    'R' stands for red discs and 'B' stands for black   ==============\n==============     discs. You will be playing with the black discs.     ============\n=====   To choose a disc, type the COLOR and NUMBER associated with the disc.  =====\n====================================================================================\n")
    theBoard.printBoard()
    player = 1
    # Keep the game going as long as the game has not ended
    current_player = computer_player
    while not theBoard.gameDone(current_player):
        if player == 1:
            ################# COMPUTER PLAYER #################
            location, thePiece, oldLoc, removedDisc = computer_player.pick_move(theBoard, human_player)
            
            # checks if they hopped
            didHop = False
            if location[0]-oldLoc[0] == -2 and location[1]-oldLoc[1] == -2:
                didHop = True
            if location[0]-oldLoc[0] == 2 and location[1]-oldLoc[1] == 2:
                didHop = True
            if location[0]-oldLoc[0] == -2 and location[1]-oldLoc[1] == 2:
                didHop = True
            if location[0]-oldLoc[0] == 2 and location[1]-oldLoc[1] == -2:
                didHop = True
            
            # make the move
            computer_player.move(theBoard, location[0], location[1], oldLoc[0], oldLoc[1], thePiece, didHop)
            theBoard.printBoard()
            if didHop:
                print("Drats! They took your piece! ", removedDisc.id, "\nLooks like a computer's smarter than you...")
            player = 2
            current_player = human_player
        else:
            ################# HUMAN PLAYER #################
            print()
            piece = input("Choose the piece you would like to move: ")
            while piece not in human_player.discs:
                piece = input("Choose the piece you would like to move (must be a piece left on the board): ")
            r = 0
            c = 0
            chosenPiece = None
            # find location of the piece the player wants to move
            for i, row in enumerate(theBoard.matrix):
                for j, item in enumerate(row):
                    if item != '--' and item.id == piece:
                        r = i
                        c = j
                        chosenPiece = item
                        break
            validLocations = human_player.moveDiagonal(theBoard, c, r, chosenPiece)
            validLocations += human_player.hop(theBoard, c, r, chosenPiece)
            while len(validLocations) == 0:
                piece = input("Choose the piece you would like to move (must be a piece left on the board that has valid locations): ")
                r = 0
                c = 0
                chosenPiece = None
                # find location of the piece the player wants to move
                for i, row in enumerate(theBoard.matrix):
                    for j, item in enumerate(row):
                        if item != '--' and item.id == piece:
                            r = i
                            c = j
                            chosenPiece = item
                            break
                validLocations = human_player.moveDiagonal(theBoard, c, r, chosenPiece)
                validLocations += human_player.hop(theBoard, c, r, chosenPiece)
            
            print("Where would you like to place your disc? Here are all of the valid locations:")
            for i in validLocations:
                for j in i:
                    print(j, end=" ")
                print()
            location = input("Must type the row and column. EXAMPLE: 4 5 (row 4 and column 5): ")
            loc = location.split()
            theLoc = []
            if len(loc) == 2:
                row = int(loc[0])
                column = int(loc[1])
                theLoc = [row, column]
            while len(loc) != 2 or theLoc not in validLocations:
                location = input("Invalid row or column. Must type the row and column. EXAMPLE: 4 5 (row 4 and column 5): ")
                loc = location.split()
                if len(loc) == 2:
                    row = int(loc[0])
                    column = int(loc[1])
                    theLoc = [row, column]
            print()
            
            # checks if you hopped
            didHop = False
            takenPiece = None
            if row-r == -2 and column-c == -2:
                didHop = True
                takenPiece = theBoard.matrix[r-1][c-1]
            if row-r == 2 and column-c == 2:
                didHop = True
                takenPiece = theBoard.matrix[r+1][c+1]
            if row-r == -2 and column-c == 2:
                didHop = True
                takenPiece = theBoard.matrix[r-1][c+1]
            if row-r == 2 and column-c == -2:
                didHop = True
                takenPiece = theBoard.matrix[r+1][c-1]
            human_player.move(theBoard, row, column, r, c, chosenPiece, didHop)
            theBoard.printBoard()
            if didHop:
                print("Great job! You took one of their pieces!", takenPiece.id)
            player = 1
            current_player = computer_player
    
    
    
if __name__ == "__main__":
    main()