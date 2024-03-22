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
        # store king's position
        self.whiteKingPosition = (7,4)
        self.blackKingPosition = (0,4)
        self.checkMate = False
        self.staleMate = False
        self.currentCastlingRights = CastleRights(True, True, True, True) # ath the start, no rule is broken
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks,self.currentCastlingRights.bks,
                                             self.currentCastlingRights.wqs,self.currentCastlingRights.bqs)]

    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != "--": # first cell shold not be an empty cell
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)
            self.whiteToMove = not self.whiteToMove # swap players

            if move.pieceMoved == "wK":
                self.whiteKingPosition = (move.endRow, move.endCol)
            elif move.pieceMoved == "bK":
                self.blackKingPosition = (move.endRow, move.endCol)

            # pawn promotion
            if move.isPawnPromotion:
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = "--"
                else:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                    self.board[move.endRow][move.endCol-2] = "--" 


            # update calstling rights
            self.updateCastleRights(move)
            self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks,self.currentCastlingRights.bks,
                                                     self.currentCastlingRights.wqs,self.currentCastlingRights.bqs))

            

    def undoMove(self):
        if len(self.moveLog) != 0: # make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # swap players

            if move.pieceMoved == "wK":
                self.whiteKingPosition = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingPosition = (move.startRow, move.startCol)

            # undo the castling rights
            self.castleRightsLog.pop()
            self.currentCastlingRights = self.castleRightsLog[-1]

            # undo the castle moves
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = "--"
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = "--" 

    def updateCastleRights(self,move):
        '''update the castle right given the move'''
        if move.pieceMoved == "wK":
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        if move.pieceMoved == "bK":
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False

        if move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 7: # right rook
                    self.currentCastlingRights.wks = False
                if move.startCol == 0: # right rook
                    self.currentCastlingRights.wqs = False
        if move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 7: # right rook
                    self.currentCastlingRights.bks = False
                if move.startCol == 0: # right rook
                    self.currentCastlingRights.bqs = False
                
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
        ''' All possible moves considering checks'''
        tempCurrentCastlingRight = CastleRights(self.currentCastlingRights.wks,self.currentCastlingRights.bks,
                                                       self.currentCastlingRights.wqs,self.currentCastlingRights.bqs)
        # get all possible moves
        moves = self.getAllPosiibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingPosition[0], self.whiteKingPosition[1],moves)
        else:
            self.getCastleMoves(self.blackKingPosition[0], self.blackKingPosition[1],moves)
        # make all possible moves.
        # we may remove some moves. Thus, traverse the moves list backwards
        for i in range(len(moves)-1, -1, -1):
            # make the move
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0: # check mate or stale mate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True

        else:
            self.checkMate = False
            self.staleMate = False

        self.currentCastlingRights = tempCurrentCastlingRight
        return moves
    
    def inCheck(self):
        '''Determines if the current player is in check'''
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingPosition[0], self.whiteKingPosition[1])
        else:
            return self.squareUnderAttack(self.blackKingPosition[0], self.blackKingPosition[1])
    
    def squareUnderAttack(self, r, c):
        '''Detrmines if the enemy can attack the current square'''
        self.whiteToMove = not self.whiteToMove # switch to opponents turn

        oppMoves = self.getAllPosiibleMoves()

        self.whiteToMove = not self.whiteToMove # switch back to current turn

        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False
    
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

        directions = [(1,0),(-1,0),(0,1),(0,-1)]

        for direction in directions:
            for i in range(1,8):
                pos = (r + direction[0]*i, c + direction[1]*i)
                if (pos[0] > 7) or (pos[1] > 7) or (pos[0]<0) or (pos[1]<0): # out of the board
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

        directions = [(1,1),(1,-1),(-1,1),(-1,-1)]

        for direction in directions:
            for i in range(1,8):
                pos = (r + direction[0]*i, c + direction[1]*i)
                if (pos[0] > 7) or (pos[1] > 7) or (pos[0]<0) or (pos[1]<0): # out of the board
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

        directions = [(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)]
        
        for direction in directions:
            for i in range(1,8):
                pos = (r + direction[0]*i, c + direction[1]*i)
                if (pos[0] > 7) or (pos[1] > 7) or (pos[0]<0) or (pos[1]<0): # out of the board
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

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r,c):
            return # cannot perform castling
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingSideCastlingMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueenSideCastlingMoves(r, c, moves)

    def getKingSideCastlingMoves(self, r, c, moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if not self.squareUnderAttack(r,c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r,c), (r,c+2), self.board, isCastleMove=  True))


    def getQueenSideCastlingMoves(self, r, c, moves): 
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            if not self.squareUnderAttack(r,c-1) and not self.squareUnderAttack(r, c-2) :
                moves.append(Move((r,c), (r,c-3), self.board, isCastleMove=  True))
        

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

    

class Move():

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k,v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k,v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = False
        self.isCastleMove = isCastleMove

        if (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7):
            self.isPawnPromotion = True


        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 +self.endCol

    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID

    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol)+ self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c]+self.rowsToRanks[r]
    