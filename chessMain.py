"""This is our main driver file
It handles user input and current GameState
"""
import pygame as p
import chessEngine
import math

p.init()

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15 # for animations
IMAGES = {}

def loadImages():
    """
    Initialize a global dictionary of images
    This will be created exacly once
    """
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bR", "bN", "bB", "bQ", "bK", "bp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/'+piece+'.png'), (SQ_SIZE, SQ_SIZE))


def main():
    """
    The main driver for our code. Will handle user inputs and update graphics
    """
    screen = p.display.set_mode((WIDTH,HEIGHT))
    p.display.set_caption("Chess - 1.0")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable
    animate = False # flag variable to indicate when we should animate

    loadImages() # only once before the while loop
    running = True
    sqSelected =() # no square is selected initially, keep track of the last click of the user, tuple:(row, col)
    playerClicks = [] #keep track of player clicks
    gameOver = False

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos() # (x,y) location of the mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col): #the user clicked same row and column twice
                        sqSelected = () # deselect
                        playerClicks =[] # clear player selects
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2: # after the second click
                        move = chessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])

                                moveMade = True 
                                animate = True 

                                sqSelected =()
                                playerClicks =[]
                        if not moveMade:
                            playerClicks =[sqSelected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r: # reset the board
                    gs = chessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected =() 
                    playerClicks = []
                    moveMade = False
                    animate = False
        
        if moveMade :
             if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
             validMoves = gs.getValidMoves()
             moveMade = False
             animate = False

        if len(gs.getValidMoves())==0 and gs.inCheck():
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')

        elif len(gs.getValidMoves())==0 and not gs.inCheck():
            gameOver = True
            drawText(screen, 'Stalemate')
        drawState(screen, gs, validMoves, sqSelected)
        
        clock.tick(MAX_FPS)
        p.display.flip()


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r,c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            # highlight the selected square
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # highllight moves from the sqaure
            
            for move in validMoves:
                s.fill(p.Color('yellow'))
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))
                    if gs.board[move.endRow][move.endCol] != "--":
                        s.fill('white')
                        screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))
                        s.fill(p.Color('brown3'))
                        screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


              
def highlightCheckSquare(screen, gs):
    s = p.Surface((SQ_SIZE,SQ_SIZE))
    s.set_alpha(175)
    s.fill(p.Color("red"))

    if gs.whiteToMove:
        gs.whiteToMove = not gs.whiteToMove
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if move.endRow == gs.whiteKingPosition[0] and move.endCol == gs.whiteKingPosition[1]:
                screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))
        gs.whiteToMove = not gs.whiteToMove

    if not gs.whiteToMove:
        gs.whiteToMove = not gs.whiteToMove
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if move.endRow == gs.blackKingPosition[0] and move.endCol == gs.blackKingPosition[1]:
                screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

        gs.whiteToMove = not gs.whiteToMove



def drawState(screen, gs, validMoves, sqSelected):
    """
    Responsible for all the graphics within a gamestate
    """
    drawBoard(screen) # draw squares on the board
    highlightCheckSquare(screen, gs)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) # draw pieces on the board

def drawBoard(screen):
    global colors
    """Draw the squares on the board"""
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = (int(2/math.sqrt(abs(dR) + abs(dC)+1))+1) * 4 # frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount+1):
        r, c= (move.startRow + dR*frame/frameCount), (move.startCol + dC*frame/frameCount )
        drawBoard(screen)
        drawPieces(screen, board)

        # erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) %2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare )

        # draw the captured piece back
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)

        # draw the moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawPieces(screen, board):
    """Draw the pieces on the board using GameState.board"""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32 , True, False)
    textObject = font.render(text , True, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)


if __name__ == "__main__":
    main()

