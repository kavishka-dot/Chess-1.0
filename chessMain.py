"""This is our main driver file
It handles user input and current GameState
"""
import pygame as p
import chessEngine

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
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable

    loadImages() # only once before the while loop
    running = True
    sqSelected =() # no square is selected initially, keep track of the last click of the user, tuple:(row, col)
    playerClicks = [] #keep track of player clicks

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
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
                            sqSelected =()
                            playerClicks =[]
                    if not moveMade:
                        playerClicks =[sqSelected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
        
        if moveMade :
             validMoves = gs.getValidMoves()
             moveMade = False

        drawState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawState(screen, gs):
    """
    Responsible for all the graphics within a gamestate
    """
    drawBoard(screen) # draw squares on the board
    drawPieces(screen, gs.board) # draw pieces on the board

def drawBoard(screen):
    """Draw the squares on the board"""
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        
    


def drawPieces(screen, board):
    """Draw the pieces on the board using GameState.board"""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()

