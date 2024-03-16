"""
Stores all the current information about the current gamestate
Determines the valid moves at the current state. 
It will also keep a move log.
"""
class GameState():
    def __init__(self):
        # board is a 8x8 2d list. Each element in the list has 2 characters
        # first charcter represents the colour of the pieace. "b" or "w"
        # second character represents the type of the piece.
        # "--" represents an empty space.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != "--": # first cell shold not be an empty cell
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)
            self.whiteToMove = not self.whiteToMove # swap players

    def undoMove(self):
        if len(self.moveLog) != 0: # make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # swap players
    
    def getAllPosiibleMoves(self):
        '''All possible moves without considering checks'''
        moves =[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves
    def getValidMoves(self):
        return self.getAllPosiibleMoves()
    
    def getPawnMoves(self, r, c, moves):
        
        # get white pawn moves

        if self.whiteToMove: # white pawn moves

            if self.board[r-1][c] == "--" and r-1>=0: # one square pawn advance
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c] == "--": # two square pawn advance
                    moves.append(Move((r,c),(r-2,c),self.board))
            if (c-1>=0):  # captures to left
                if (self.board[r-1][c-1][0] == "b"):
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            if  (c+1<=7): # captures to right
                if (self.board[r-1][c+1][0] == "b"):
                    moves.append(Move((r,c),(r-1,c+1),self.board))
        
        # get black pawn moves
        
        if not self.whiteToMove and r+1<=7: # black pawn moves

            if self.board[r+1][c] == "--": # one square pawn advance
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c] == "--": # two square pawn advance
                    moves.append(Move((r,c),(r+2,c),self.board))
            if (c-1>=0):  # captures to left
                if (self.board[r+1][c-1][0] == "w"):
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if  (c+1<=7): # captures to right
                if (self.board[r+1][c+1][0] == "w"):
                    moves.append(Move((r,c),(r+1,c+1),self.board))

    
    def getRookMoves(self, r, c, moves):

        color = self.board[r][c][0]
        opColor = "w" if color == "b" else "b"
        
        # up 
        for i in range(1,8):
            pos = (r-i , c)
            if (pos[0] <0 ): # out of the board
                break
            if self.board[pos[0]][pos[1]][0] == color: # same type piece
                break
            if self.board[pos[0]][pos[1]][0]  == opColor: # capture an enemy piece
                moves.append(Move((r,c), pos, self.board))
                break
            moves.append(Move((r,c), pos, self.board))

        # down
        for i in range(1,8):
            pos = (r+i , c)
            if (pos[0] >7 ): # out of the board
                break
            if self.board[pos[0]][pos[1]][0] == color: # same type piece
                break
            if self.board[pos[0]][pos[1]][0]  == opColor: # capture an enemy piece
                moves.append(Move((r,c), pos, self.board))
                break
            moves.append(Move((r,c), pos, self.board))

        # left
        for i in range(1,8):
            pos = (r , c-i)
            if (pos[1] <0 ): # out of the board
                break
            if self.board[pos[0]][pos[1]][0] == color: # same type piece
                break
            if self.board[pos[0]][pos[1]][0]  == opColor: # capture an enemy piece
                moves.append(Move((r,c), pos, self.board))
                break
            moves.append(Move((r,c), pos, self.board))

        # right
        for i in range(1,8):
            pos = (r , c+i)
            if (pos[1] > 7 ): # out of the board
                break
            if self.board[pos[0]][pos[1]][0] == color: # same type piece
                break
            if self.board[pos[0]][pos[1]][0]  == opColor: # capture an enemy piece
                moves.append(Move((r,c), pos, self.board))
                break
            moves.append(Move((r,c), pos, self.board))
            


    def getKnightMoves(self, r, c, moves):

        # all possible moves
        positions =[(r+2 , c+1),(r+2 , c-1),(r-1 , c+2),(r+1 , c+2),
                    (r-2 , c+1),(r-2 , c-1),(r-1 , c-2),(r+1 , c-2)]
        
        for pos in positions:
            if (pos[0]>7) or (pos[0]<0) or (pos[1]>7) or (pos[1]<0) or self.board[r][c][0] == self.board[pos[0]][pos[1]][0]:
                continue
            moves.append(Move((r,c), pos, self.board))

    def getBishopMoves(self, r, c, moves):

        color = self.board[r][c][0]
        opColor = "w" if color == "b" else "b"

        # down-right
        for i in range(1,8):
            pos = (r+i , c+i)
            if (pos[0] > 7) or (pos[1] > 7): # out of the board
                break
            if self.board[pos[0]][pos[1]][0] == color: # same type piece
                break
            if self.board[pos[0]][pos[1]][0]  == opColor: # capture an enemy piece
                moves.append(Move((r,c), pos, self.board))
                break
            moves.append(Move((r,c), pos, self.board))

        # down-left
        for i in range(1,8):
            pos = (r+i , c-i)
            if (pos[0] >7) or (pos[1] <0): # out of the board
                break
            if self.board[pos[0]][pos[1]][0] == color: # same type piece
                break
            if self.board[pos[0]][pos[1]][0]  == opColor: # capture an enemy piece
                moves.append(Move((r,c), pos, self.board))
                break
            moves.append(Move((r,c), pos, self.board))

        # up - right
        for i in range(1,8):
            pos = (r-i , c+i)
            if (pos[0] <0) or (pos[1] >7): # out of the board
                break
            if self.board[pos[0]][pos[1]][0] == color: # same type piece
                break
            if self.board[pos[0]][pos[1]][0]  == opColor: # capture an enemy piece
                moves.append(Move((r,c), pos, self.board))
                break
            moves.append(Move((r,c), pos, self.board))

        # up - left
        for i in range(1,8):
            pos = (r-i , c-i)
            if (pos[0] <0) or (pos[1] <0): # out of the board
                break
            if self.board[pos[0]][pos[1]][0] == color: # same type piece
                break
            if self.board[pos[0]][pos[1]][0]  == opColor: # capture an enemy piece
                moves.append(Move((r,c), pos, self.board))
                break
            moves.append(Move((r,c), pos, self.board))
            
        

    def getQueenMoves(self, r, c, moves):
        color = self.board[r][c][0]
        opColor = "w" if color == "b" else "b"
        
        # up 
        for i in range(1,8):
            pos = (r-i , c)
            if (pos[0] <0 ): # out of the board
                break
            if self.board[pos[0]][pos[1]][0] == color: # same type piece
                break
            if self.board[pos[0]][pos[1]][0]  == opColor: # capture an enemy piece
                moves.append(Move((r,c), pos, self.board))
                break
            moves.append(Move((r,c), pos, self.board))

        # down
        for i in range(1,8):
            pos = (r+i , c)
            if (pos[0] >7 ): # out of the board
                break
            if self.board[pos[0]][pos[1]][0] == color: # same type piece
                break
            if self.board[pos[0]][pos[1]][0]  == opColor: # capture an enemy piece
                moves.append(Move((r,c), pos, self.board))
                break
            moves.append(Move((r,c), pos, self.board))

        # left
        for i in range(1,8):
            pos = (r , c-i)
            if (pos[1] <0 ): # out of the board
                break
            if self.board[pos[0]][pos[1]][0] == color: # same type piece
                break
            if self.board[pos[0]][pos[1]][0]  == opColor: # capture an enemy piece
                moves.append(Move((r,c), pos, self.board))
                break
            moves.append(Move((r,c), pos, self.board))

        # right
        for i in range(1,8):
            pos = (r , c+i)
            if (pos[1] > 7 ): # out of the board
                break
            if self.board[pos[0]][pos[1]][0] == color: # same type piece
                break
            if self.board[pos[0]][pos[1]][0]  == opColor: # capture an enemy piece
                moves.append(Move((r,c), pos, self.board))
                break
            moves.append(Move((r,c), pos, self.board))

        # down-right
        for i in range(1,8):
            pos = (r+i , c+i)
            if (pos[0] > 7) or (pos[1] > 7): # out of the board
                break
            if self.board[pos[0]][pos[1]][0] == color: # same type piece
                break
            if self.board[pos[0]][pos[1]][0]  == opColor: # capture an enemy piece
                moves.append(Move((r,c), pos, self.board))
                break
            moves.append(Move((r,c), pos, self.board))

        # down-left
        for i in range(1,8):
            pos = (r+i , c-i)
            if (pos[0] >7) or (pos[1] <0): # out of the board
                break
            if self.board[pos[0]][pos[1]][0] == color: # same type piece
                break
            if self.board[pos[0]][pos[1]][0]  == opColor: # capture an enemy piece
                moves.append(Move((r,c), pos, self.board))
                break
            moves.append(Move((r,c), pos, self.board))

        # up - right
        for i in range(1,8):
            pos = (r-i , c+i)
            if (pos[0] <0) or (pos[1] >7): # out of the board
                break
            if self.board[pos[0]][pos[1]][0] == color: # same type piece
                break
            if self.board[pos[0]][pos[1]][0]  == opColor: # capture an enemy piece
                moves.append(Move((r,c), pos, self.board))
                break
            moves.append(Move((r,c), pos, self.board))

        # up - left
        for i in range(1,8):
            pos = (r-i , c-i)
            if (pos[0] <0) or (pos[1] <0): # out of the board
                break
            if self.board[pos[0]][pos[1]][0] == color: # same type piece
                break
            if self.board[pos[0]][pos[1]][0]  == opColor: # capture an enemy piece
                moves.append(Move((r,c), pos, self.board))
                break
            moves.append(Move((r,c), pos, self.board))
            

    def getKingMoves(self, r, c, moves):
        
        # all possible moves
        positions = [(r-1 , c),(r-1 , c+1),(r-1 , c-1),(r , c-1),
                     (r , c+1),(r+1 , c),(r+1 , c-1),(r+1 , c+1)]
        
        for pos in positions:
            if (pos[0]>7) or (pos[0]<0) or (pos[1]>7) or (pos[1]<0) or self.board[r][c][0] == self.board[pos[0]][pos[1]][0]:
                continue
            moves.append(Move((r,c), pos, self.board))

class Move():

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k,v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k,v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 +self.endCol

    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID

    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol)+ self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c]+self.rowsToRanks[r]