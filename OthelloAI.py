""" 
Ty Pederson
10349042
11/6/22
CSC 475 001
Fall 2022

Assignment 3
An Intelligent Othello Player

Othello game that can be played against either another person
or against an AI which uses mini-max with alpha-beta pruning
"""

# try to import a library called anytree that is used to diplay a tree of all the possible moves
# to use this library use "pip install anytree" in powershell or terminal
try:
    from anytree import Node, RenderTree
    AT = True
# if unable to import anytree then create fake methods and print an error message
except:
    AT = False
    def Node(name, parent=None):
        pass
    def RenderTree(name):
        pass
    print("anytree could not be imported")

import tkinter as tk
import math
import copy

# window using tkinter to be drawn to
window = tk.Tk()

# board with heuristic values for each position
boardHeur = [
            [20, -3, 11, 8, 8, 11, -3, 20],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [11, -4,  2, 2, 2,  2, -4, 11],
            [ 8,  1,  2,-3,-3,  2,  1,  8],
            [ 8,  1,  2,-3,-3,  2,  1,  8],
            [11, -4,  2, 2, 2,  2, -4, 11],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [20, -3, 11, 8, 8, 11, -3, 20]
        ]

# starting arrangement for the board
boardArr = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,1,2,0,0,0],
    [0,0,0,2,1,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
]

#global variables used throughout program
user = "black"
AI = "white"
globalTurn = user
AIOn = True
alphaBeta = True
debug = False
heuristics = True
tree = False
boardDisp = True

x = 0
y = 0
depth = 3
numStates = 0


# creates each item to be drawn by tkinter
canvas = tk.Canvas(window, bg="green", height = 800, width=800)

score = tk.Label(window,  relief="raised",  font="Times 20 italic bold")

colorBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"Player 1: {user}\tPlayer 2: {AI}") 

AIBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"AI: {AIOn}") 
startBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = "Start Game") 
resetBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = "Reset Game") 

ABBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"Alpha-Beta Pruning: {alphaBeta}") 
debugBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"Debug: {debug}") 

heurBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"Heuristics: {heuristics}")
treeBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"Tree: {tree}")
boardBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"Board: {boardDisp}")

depthBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"Depth: {depth}")

victor = tk.Label(window,  relief="raised",  font="Times 20 italic bold")


# places pieces on the board
def placePiece(x, y, color):
    canvas.create_oval(x * 100 + 10, y * 100 + 10, x * 100 + 90, y * 100 + 90, fill=color)

# gets the score by counting the values of each position and incrementing each side's score
def getScore(board):
    blackScore = 0
    whiteScore = 0
    for x in range(8):
        for y in range(8):
            match board[y][x]:
                case 0:
                    continue
                case 1:
                    blackScore += 1
                    continue
                case 2:
                    whiteScore += 1
                    continue
    return blackScore, whiteScore

# draws the board at the beginning of the game and after each turn to cover the valid moves not used
def drawBoard():
    # creates the board
    canvas.create_rectangle(0, 0, 800, 800, fill = "green")

    # creates the lines on the board
    for i in range(1, 8):
        canvas.create_line(i * 100, 0, i * 100, 800)
        canvas.create_line(0, i * 100, 800, i * 100)

    # debug if board is true
    if (debug and boardDisp):
        print("Board state:")

    # creates each piece on the board
    for x in range(8):
        for y in range(8):
            if (boardArr[y][x] == 1):
                placePiece(x, y, "black")
            elif (boardArr[y][x] == 2):
                placePiece(x, y, "white")
        
        # one row of the debug board display
        if (debug and boardDisp):
            print(f"{boardArr[x][0]},{boardArr[x][1]},{boardArr[x][2]},{boardArr[x][3]},{boardArr[x][4]},{boardArr[x][5]},{boardArr[x][6]},{boardArr[x][7]}")
    # just an extra line after the board has been displayed
    if (debug and boardDisp):
        print()

    # updates the scoreboard
    blackScore, whiteScore = getScore(boardArr)
    score.config(text = f"Black: {blackScore}\t\tWhite: {whiteScore}")
    

# checks the validity of the position
def checkPos(x, y, turn, board):

    valToCheck = 1
    currVal = 2

    if (turn == "black"):
        currVal, valToCheck = valToCheck, currVal

    
    # if the spot is taken the position is invalid
    if (board[y][x] != 0):
        return False

    # checks in each of the 8 directions outward from the position
    for xDir, yDir in [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]:
        newX, newY = x, y
        newX += xDir
        newY += yDir
        
        # continues to the next direction if the direction being checked leaves the board
        if (newX > 7 or newX < 0 or newY > 7 or newY < 0 or board[newY][newX] == currVal):
            continue

        # continues to check the direction if the opposite color piece is found
        while (board[newY][newX] == valToCheck):
            newX += xDir
            newY += yDir

            # breaks from the while loop if the direction being checked leaves the board
            if (newX > 7 or newX < 0 or newY > 7 or newY < 0):
                newX -= xDir
                newY -= yDir
                break

        # if the direction being checked has a line of the opposite color and ends on the same color 
        # it is a valid position and the other directions do not need to be checked
        if (board[newY][newX] == currVal):
            return True

    # return false if no direction is valid
    return False


# operates very similarly to checkPos but flips peices in the valid directions
def flipPieces(x, y, turn, board):
    valToCheck = 1
    currVal = 2

    if (turn == "black"):
        currVal, valToCheck = valToCheck, currVal

    board[y][x] = currVal

    # checks in each of the 8 directions outward from the position
    for xDir, yDir in [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]:
        newX, newY = x, y
        newX += xDir
        newY += yDir
        
        # continues to the next direction if the direction being checked leaves the board
        if (newX > 7 or newX < 0 or newY > 7 or newY < 0 or board[newY][newX] == currVal):
            continue
        
        # continues to check the direction if the opposite color piece is found
        while (board[newY][newX] == valToCheck):
            newX += xDir
            newY += yDir

            # breaks from the while loop if the direction being checked leaves the board
            if (newX > 7 or newX < 0 or newY > 7 or newY < 0):
                newX -= xDir
                newY -= yDir
                break

        # if the direction being checked has a line of the opposite color and ends on the same color 
        # the direction is valid begin back tracking while flipping colors by updating the values of the board
        if (board[newY][newX] == currVal):
            newX -= xDir
            newY -= yDir

            # begin back tracking while flipping colors by updating the values of the board
            while (board[newY][newX] == valToCheck):
                board[newY][newX] = currVal
                newX -= xDir
                newY -= yDir

    # returns the board with updated values
    return board


# shows the valid moves for each turn
def showValid(valid):
    for [x,y] in valid:
        placePiece(x, y, globalTurn)
        canvas.create_oval(x * 100 + 20, y * 100 + 20, x * 100 + 80, y * 100 + 80, fill="green")

    # prints the valid moves of the player whose turn it is
    if (debug and boardDisp):
        print(f"Valid {globalTurn} moves: {valid}\n")

    # force the window to update now instead of later, this is mostly used to ensure the AI's moves are displayed
    window.update()


# gets a list of the valid moves for the player and board provided
def validMoves(turn, board):

    valid = []

    # checks the validity of each position by calling checkPos()
    for x in range(8):
        for y in range(8):
            if (checkPos(x, y, turn, board)):
                valid.append([x,y])

    return valid


# heuristic function used for minimax
def getHeur(x, y, board):
    # grabs the score but only the AI's score is needed so the color of the player is checked
    if (user == "black"):
        blackScore, whiteScore = getScore(board)
    else:
        whiteScore, blackScore = getScore(board)

    # heuristic is simply white score plus the heuristic value of the x, y at the root of the tree
    return whiteScore + boardHeur[y][x]

# minimax function performed on each valid move
def minimax(startx, starty, xpos, ypos, depth, alpha, beta, maximizingPlayer, board, stem):

    global numStates

    if (maximizingPlayer):
        nextTurn = user
    else:
        nextTurn = AI
    
    # create a deep copy of the board before flippling pieces because original board would have pieces flipped as well
    tempBoard = copy.deepcopy(board)
    # board state tracked for each node
    tempBoard = flipPieces(xpos, ypos, nextTurn, tempBoard)
    # next set of valid moves
    next = validMoves(nextTurn, tempBoard) 

    # return the heuristic value of the position if depth is zero or no valid moves
    if (depth == 0 or next == []) :
        # get heuristic value here to be used in tree and then return
        heur = getHeur(startx, starty, tempBoard)

        # if tree is enabled and anytree is imported, 
        # change the name of the node to the position and heuristic
        if (tree and AT):
            stem.name = f"[{xpos},{ypos}] : {heur}"
        # if not then just increment the number of states checked
        else:
            numStates += 1
        return heur

    # maximizing player
    if (maximizingPlayer):

        # large neg starting value for max eval
        maxEval = -100000

        # iterates through next set of valid moves
        for [x,y] in next:

            # if tree is enabled and anytree is imported, 
            # create a node for the move then make recursive minimax call
            if (tree and AT):
                node = Node(f"[{x},{y}]", parent=stem)
                eval = minimax(startx, starty, x, y, depth - 1, alpha, beta, False, tempBoard, node)

            # if not, save memory by simply reusing the parent node
            # and increment number of states checked
            else:
                numStates += 1
                eval = minimax(startx, starty, x, y, depth - 1, alpha, beta, False, tempBoard, stem)

            # set max eval to larger value
            maxEval = max(maxEval, eval)

            # if AB pruning is enabled
            if (alphaBeta):
                # set alpha to larger value
                alpha = max(alpha, eval)

                # if beta is smaller than alpha, prune
                if (beta <= alpha):

                    # if tree is enabled and anytree is imported,
                    # set the node's name to reflect that it has been pruned
                    if (tree and AT):    
                        node.name = f"[{x},{y}] : {maxEval} (pruned)"
                    break

            # if tree is enabled and anytree is imported,
            # set the node's name to reflect it's heuristic
            if (tree and AT):    
                node.name = f"[{x},{y}] : {maxEval}"

        return maxEval

    # minimizing player
    else:
        # large pos starting value for max eval
        minEval = 100000

        # iterates through next set of valid moves
        for [x,y] in next:

            # if tree is enabled and anytree is imported, 
            # create a node for the move then make recursive minimax call
            if (tree and AT):
                node = Node(f"[{x},{y}]", parent=stem)
                eval = minimax(startx, starty, x, y, depth - 1, alpha, beta, True, tempBoard, node)

            # if not, save memory by simply reusing the parent node
            # and increment number of states checked
            else:
                numStates += 1
                eval = minimax(startx, starty, x, y, depth - 1, alpha, beta, True, tempBoard, stem)

            # set min eval to smaller value
            minEval = min(minEval, eval)

            # if AB pruning is enabled
            if (alphaBeta):

                # set bata to the smaller value
                beta = min(beta, eval)

                # if beta is smaller than alpha, prune
                if (beta <= alpha):

                    # if tree is enabled and anytree is imported,
                    # set the node's name to reflect that it has been pruned
                    if (tree and AT):    
                        node.name = f"[{x},{y}] : {minEval} (pruned)"
                    break

            # if tree is enabled and anytree is imported,
            # set the node's name to reflect it's heuristic
            if (tree and AT):    
                node.name = f"[{x},{y}] : {minEval}"

        return minEval

# displays the victor
def displayVictor():
    black, white = getScore(boardArr)
    if (black > white):
        myText = "Black Wins!"
    elif (white > black):
        myText = "White Wins!"
    elif (white == black and white != 2):
        myText = "Tie!"
    else:
        myText = ""

    victor.grid(row=6, column=1, columnspan=6, ipadx = 225, ipady = 25)
    victor.config(text = myText)


# function that controls the AI
def AIMove(board):
    global globalTurn
    global numStates


    maxHeur = -10000
    x = -1
    y = -1
    numStates = 0

    # another deep copy of the board used for passing to minimax
    tempBoard = copy.deepcopy(board)
    valid = validMoves(globalTurn, tempBoard)
    showValid(valid)


    moveHeur = []

    # if displaying the tree create a root node for minimax
    if (tree):
        root = Node("root")
    # if not just give it a throw away variable
    else:
        node = 0

    # iterates through each valid move
    for [tempx,tempy] in valid:

        # if displaying tree create a node for each valid move
        if (tree):
            node = Node([tempx,tempy], parent=root)

        # get heuristic for each valid move
        tempVal = minimax(tempx, tempy, tempx, tempy, depth - 1, -100000, 100000, False, tempBoard, node)

        # if displaying tree set node name to reflect heuristic
        if (tree):
            node.name = f"[{tempx}, {tempy}]: {tempVal}"

        
        moveHeur.append(tempVal)

        # replace max heuristic if larger one is found
        if (tempVal > maxHeur):
            maxHeur = tempVal
            x = tempx
            y = tempy

        # if displaying tree set root name to reflect max heuristic
        if (tree):
            root.name = f"[{x}, {y}]: {maxHeur}"

    # displays tree
    if (debug and tree and AT):
        for pre, fill, node in RenderTree(root):
            print("%s%s" % (pre, node.name))
            numStates +=1
        numStates -= 1
        print()
    
    # displays valid moves, heuristics per move and number of moves searched
    if (debug and heuristics):
        showValid(valid)
        print(f"Heuristics per position: {moveHeur}\n")
        print(f"Number of States Searched: {numStates}\n")

    # if a valid move was found place the piece and flip other pieces
    if (x != -1 or y != -1):
        flipPieces(x, y, globalTurn, board)

        # diplays where the piece was placed
        if (debug and boardDisp):
            print(f"AI placed at: {x}, {y}\n")

    # switch the turn to user
    globalTurn = user


# function that handles mouse click event
def mouseXY(event):
    global x
    global y
    global globalTurn

    # takes the mouse position and turns it into integers
    x, y = math.floor(event.x / 100), math.floor(event.y / 100)

    # find the valid moves
    valid = validMoves(globalTurn, boardArr)

    # if user mouse is over a valid position place the piece and switch turns
    if (globalTurn == user and [x,y] in valid):
        flipPieces(x,y, globalTurn, boardArr)
        globalTurn = AI

        # displays where player 1 placed piece
        if (debug and boardDisp):
            print(f"Player 1 placed at: {x}, {y}\n")

    # if AI mouse is over a valid position place the piece and switch turns (only works if AI is not playing)
    elif (not(AIOn) and globalTurn == AI and [x,y] in valid):
        flipPieces(x,y, globalTurn, boardArr)
        globalTurn = user

        # displays where player 2 placed piece
        if (debug and boardDisp):
            print(f"Player 2 placed at: {x}, {y}\n")

    
    drawBoard()

    # calls AI function to play after user takes turn
    if (AIOn and globalTurn == AI):
        AIMove(boardArr)
        drawBoard()

    # displays victor if no players have a valid move to make
    if (validMoves(user, boardArr) == [] and validMoves(AI, boardArr) == []):
        displayVictor()

    showValid(validMoves(globalTurn, boardArr))



# function that starts the game
def startGame():
    colorBtn.config(state="disabled")
    showValid(validMoves(globalTurn, boardArr))
    window.bind("<Button-1>", mouseXY)

# function that resets the game
def resetGame():
    global boardArr
    global globalTurn

    globalTurn = user
    boardArr = [
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,1,2,0,0,0],
        [0,0,0,2,1,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
    ]

    victor.config(text="")
    victor.grid(row=6, column=1, columnspan=6, ipadx = 295, ipady = 25)
    colorBtn.config(state="active")
    window.unbind("<Button-1>")
    drawBoard()

# function that toggles alpha-beta pruning
def toggleAB():
    if (debug):
        print("Toggled AB")
    global alphaBeta
    alphaBeta = not(alphaBeta)
    ABBtn.config(text=f"Alpha-Beta Pruning: {alphaBeta}")

# function that toggles AI
def toggleAI():
    if (debug):
        print("toggled AI")
    global AIOn
    AIOn = not(AIOn)
    AIBtn.config(text = f"AI: {AIOn}")

# function that switches the players colors
def toggleColor():
    if (debug):
        print("toggled color")
    global user
    global AI
    global globalTurn
    user, AI = AI, user
    globalTurn = user
    colorBtn.config(text = f"Player 1: {user}\tPlayer 2: {AI}")

# function that toggles debug
def toggleDebug():
    print("toggled debug")
    global debug
    debug = not(debug)
    debugBtn.config(text = f"Debug: {debug}")

# function that toggles heurisitcs shown during debuging
def toggleHeur():
    if (debug):
        print("toggled heuristics")
    global heuristics
    heuristics = not(heuristics)
    heurBtn.config(text = f"Heuristics: {heuristics}")

# function that toggles tree shown durning debugging
def toggleTree():
    if (debug):
        print("toggled tree")
    global tree
    tree = not(tree)
    treeBtn.config(text = f"Tree: {tree}")

# function that toggles board state shown during debugging
def toggleBoard():
    if (debug):
        print("toggled board")
    global boardDisp
    boardDisp = not(boardDisp)
    boardBtn.config(text = f"Board: {boardDisp}")

# function that cycles the depth of the minimax function from 1 - 10
def toggleDepth():
    global depth

    depth += 1

    if (depth >= 11):
        depth = 1

    # tree is automatically toggled off for depth 
    # of 5 and above to save resources and speed up 
    # minimax but can be forced on 
    if (depth >= 5 and tree == True):
        toggleTree()

    if (debug):
        print(f"Depth changed to {depth}")

    depthBtn.config(text=f"Depth: {depth}")



# layout of everything being drawn to the screen
canvas.grid(row=0, column=0, rowspan=8)
score.grid(row=0, column=1, columnspan=6, ipadx = 135, ipady = 20)

colorBtn.grid(row=1, column=1, columnspan=6, ipadx = 88, ipady = 20)

AIBtn.grid(row=2, column=1, columnspan=2, ipadx = 55, ipady = 20)
startBtn.grid(row=2, column=3, columnspan=2, ipadx = 12, ipady = 20)
resetBtn.grid(row=2, column=5, columnspan=2, ipadx = 12, ipady = 20)

ABBtn.grid(row=3, column=1, columnspan=3, ipadx = 35, ipady = 20)
debugBtn.grid(row=3, column=4, columnspan=3, ipadx = 8, ipady = 20)

heurBtn.grid(row=4, column=1, columnspan=2, ipadx = 10, ipady = 20)
treeBtn.grid(row=4, column=3, columnspan=2, ipadx = 10, ipady = 20)
boardBtn.grid(row=4, column=5, columnspan=2, ipadx = 10, ipady = 20)

depthBtn.grid(row=5, column=1, columnspan=6, ipadx = 235, ipady = 20)

victor.grid(row=6, column=1, columnspan=6, ipadx = 295, ipady = 30)

# links the buttons to their respective functions
colorBtn.config(command=toggleColor)

AIBtn.config(command=toggleAI)
startBtn.config(command=startGame)
resetBtn.config(command=resetGame)

ABBtn.config(command=toggleAB)
debugBtn.config(command=toggleDebug)

heurBtn.config(command=toggleHeur)
treeBtn.config(command=toggleTree)
boardBtn.config(command=toggleBoard)

depthBtn.config(command=toggleDepth)

# draw the board and start the program
drawBoard()

window.mainloop()