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

try:
    from anytree import Node, RenderTree
    AT = True
except:
    AT = False
    def Node(name, parent=None):
        pass
    def RenderTree(name):
        pass
    print("anytree could not be imported")

import tkinter as tk
import math
from time import sleep
import copy

window = tk.Tk()

boardHeur = [
            [200, -3, 11, 8, 8, 11, -3, 200],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [11, -4,  2, 2, 2,  2, -4, 11],
            [ 8,  1,  2,-3,-3,  2,  1,  8],
            [ 8,  1,  2,-3,-3,  2,  1,  8],
            [11, -4,  2, 2, 2,  2, -4, 11],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [200, -3, 11, 8, 8, 11, -3, 200]
        ]

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

user = "black"
cpu = "white"
globalTurn = user
cpuOn = True
alphaBeta = True
debug = False
heuristics = True
tree = False
boardDisp = True

x = 0
y = 0
turnCount = 0
depth = 3
numStates = 0

canvas = tk.Canvas(window, bg="green", height = 800, width=800)

score = tk.Label(window,  relief="raised",  font="Times 20 italic bold")

colorBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"Player 1: {user}\tPlayer 2: {cpu}") 

cpuBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"CPU: {cpuOn}") 
startBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = "Start Game") 
resetBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = "Reset Game") 

ABBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"Alpha-Beta Pruning: {alphaBeta}") 
debugBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"Debug: {debug}") 

heurBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"Heuristics: {heuristics}")
treeBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"Tree: {tree}")
boardBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"Board: {boardDisp}")

depthBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"Depth: {depth}")

victor = tk.Label(window,  relief="raised",  font="Times 20 italic bold")


def placePiece(x, y, color):
    canvas.create_oval(x * 100 + 10, y * 100 + 10, x * 100 + 90, y * 100 + 90, fill=color)

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


def drawBoard():
    canvas.create_rectangle(0, 0, 800, 800, fill = "green")

    for i in range(1, 8):
        canvas.create_line(i * 100, 0, i * 100, 800)
        canvas.create_line(0, i * 100, 800, i * 100)

    if (debug and boardDisp):
        print("Board state:")
    for x in range(8):
        for y in range(8):
            if (boardArr[y][x] == 1):
                placePiece(x, y, "black")
            elif (boardArr[y][x] == 2):
                placePiece(x, y, "white")
        if (debug and boardDisp):
            print(f"{boardArr[x][0]},{boardArr[x][1]},{boardArr[x][2]},{boardArr[x][3]},{boardArr[x][4]},{boardArr[x][5]},{boardArr[x][6]},{boardArr[x][7]}")
    if (debug and boardDisp):
        print()

    blackScore, whiteScore = getScore(boardArr)
    score.config(text = f"Black: {blackScore}\t\tWhite: {whiteScore}")
    


def checkPos(x, y, turn, board):

    valToCheck = 1
    currVal = 2

    if (turn == "black"):
        currVal, valToCheck = valToCheck, currVal

    

    if (board[y][x] != 0):
        return False

    for xDir, yDir in [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]:
        newX, newY = x, y
        newX += xDir
        newY += yDir
        
        if (newX > 7 or newX < 0 or newY > 7 or newY < 0 or board[newY][newX] == currVal):
            continue

        while (board[newY][newX] == valToCheck):
            newX += xDir
            newY += yDir

            if (newX > 7 or newX < 0 or newY > 7 or newY < 0):
                newX -= xDir
                newY -= yDir
                break

        if (board[newY][newX] == currVal):
            return True

    return False


def flipPieces(x, y, turn, board):
    valToCheck = 1
    currVal = 2

    if (turn == "black"):
        currVal, valToCheck = valToCheck, currVal

    board[y][x] = currVal

    for xDir, yDir in [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]:
        newX, newY = x, y
        newX += xDir
        newY += yDir
        
        if (newX > 7 or newX < 0 or newY > 7 or newY < 0 or board[newY][newX] == currVal):
            continue
        
        while (board[newY][newX] == valToCheck):
            newX += xDir
            newY += yDir

            if (newX > 7 or newX < 0 or newY > 7 or newY < 0):
                newX -= xDir
                newY -= yDir
                break

        if (board[newY][newX] == currVal):
            newX -= xDir
            newY -= yDir
            while (board[newY][newX] == valToCheck):
                board[newY][newX] = currVal
                newX -= xDir
                newY -= yDir
                if (newX > 7 or newX < 0 or newY > 7 or newY < 0):
                    break
    return board


def showValid(valid):
    for [x,y] in valid:
        placePiece(x, y, globalTurn)
        canvas.create_oval(x * 100 + 20, y * 100 + 20, x * 100 + 80, y * 100 + 80, fill="green")

    if (debug and boardDisp):
        print(f"Valid {globalTurn} moves: {valid}\n")

    window.update()


def validMoves(turn, board):

    valid = []

    for x in range(8):
        for y in range(8):
            if (checkPos(x, y, turn, board)):
                valid.append([x,y])

    return valid


def getHeur(xpos, ypos, board):
    if (user == "black"):
        p1 = 1
        p2 = 2
        blackScore, whiteScore = getScore(board)
    else:
        p1 = 2
        p2 = 1
        whiteScore, blackScore = getScore(board)

    #difference between scores
    if (whiteScore > blackScore):
        score = (100 * whiteScore) / (whiteScore + blackScore)
    elif (whiteScore < blackScore):
        score = -(100 * blackScore) / (whiteScore + blackScore)
    else:
        score = 0
    

    #corners occupied
    userCorners = 0
    cpuCorners = 0
    for x, y in [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]:
        if (board[y][x] == p1):
            userCorners += 1
        elif (board[y][x] == p2):
            cpuCorners += 1

    corners = (userCorners - cpuCorners)

    BH = boardHeur[ypos][xpos]
    heuristic = round(score + BH * 10 + corners * 10000 )
    return heuristic


def minimax(xpos, ypos, depth, alpha, beta, maximizingPlayer, board, stem):

    global numStates

    if (maximizingPlayer):
        nextTurn = user
    else:
        nextTurn = cpu
    
    tempBoard = copy.deepcopy(board)
    tempBoard = flipPieces(xpos, ypos, nextTurn, tempBoard)
    next = validMoves(nextTurn, tempBoard) 

    if (depth == 0 or next == []) :
        heur = getHeur(xpos, ypos, tempBoard)
        if (tree):
            stem.name = f"[{xpos},{ypos}] : {heur}"
        else:
            numStates += 1
        return heur

    if (maximizingPlayer):
        maxEval = -100000
        for [x,y] in next:
            if (tree):
                tile = Node(f"[{x},{y}]", parent=stem)
                eval = minimax(x, y, depth - 1, alpha, beta, False, tempBoard, tile)
            else:
                numStates += 1
                eval = minimax(x, y, depth - 1, alpha, beta, False, tempBoard, stem)
            maxEval = max(maxEval, eval)
            if (alphaBeta):
                alpha = max(alpha, eval)
                if (beta <= alpha):
                    break
            if (tree):    
                tile.name = f"[{x},{y}] : {maxEval}"
        return maxEval

    else:
        minEval = 100000
        for [x,y] in next:
            if (tree):
                tile = Node(f"[{x},{y}]", parent=stem)
                eval = minimax(x, y, depth - 1, alpha, beta, True, tempBoard, tile)
            else:
                numStates += 1
                eval = minimax(x, y, depth - 1, alpha, beta, True, tempBoard, stem)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if (alphaBeta):
                if (beta <= alpha):
                    break
            if (tree):    
                tile.name = f"[{x},{y}] : {minEval}"
        return minEval


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


def cpuMove(board):
    global globalTurn
    global turnCount
    global numStates

    maxHeur = -10000000000
    x = -1
    y = -1
    numStates = 0

    tempBoard = copy.deepcopy(board)
    valid = validMoves(globalTurn, tempBoard)
    showValid(valid)

    if (turnCount >= 1):
        displayVictor()


    moveHeur = []
    if (tree):
        root = Node("root")
    else:
        node = 0

    for [tempx,tempy] in valid:
        if (tree):
            node = Node([tempx,tempy], parent=root)
        tempVal = minimax(tempx, tempy, depth - 1, -100000, 100000, False, tempBoard, node)
        moveHeur.append(tempVal)
        if (tempVal > maxHeur):
            maxHeur = tempVal
            x = tempx
            y = tempy

    if (debug and tree and AT):
        for pre, fill, node in RenderTree(root):
            print("%s%s" % (pre, node.name))
            numStates +=1
        numStates -= 1
        print()
    
    if (debug and heuristics):
        showValid(valid)
        print(f"Heuristics per position: {moveHeur}\n")
        print(f"Number of States Searched: {numStates}\n")

    if (x != -1 or y != -1):
        turnCount = 0
        if (debug and boardDisp):
            print(f"CPU placed at: {x}, {y}\n")
        flipPieces(x, y, globalTurn, board)

    elif (turnCount < 1):
        turnCount += 1
    else:
        displayVictor()

    globalTurn = user


def mouseXY(event):
    global x
    global y
    global globalTurn
    global turnCount
    x, y = math.floor(event.x / 100), math.floor(event.y / 100)

    valid = validMoves(globalTurn, boardArr)

    if (valid == [] and turnCount >= 1):
        displayVictor()

    if (globalTurn == user and [x,y] in valid):
        turnCount = 0
        flipPieces(x,y, globalTurn, boardArr)
        globalTurn = cpu

    elif (not(cpuOn) and globalTurn == cpu and [x,y] in valid):
        turnCount = 0
        flipPieces(x,y, globalTurn, boardArr)
        globalTurn = user
    elif (globalTurn == cpu and valid == []):
        turnCount += 1
        globalTurn = user
    elif (globalTurn == user and valid == []):
        turnCount += 1
        globalTurn = cpu
    
    if (debug and boardDisp):
        print(f"User placed at: {x}, {y}\n")

    
    drawBoard()

    if (cpuOn and globalTurn == cpu):
        cpuMove(boardArr)
        sleep(0.5)
        drawBoard()

    showValid(validMoves(globalTurn, boardArr))




def startGame():
    colorBtn.config(state="disabled")
    showValid(validMoves(globalTurn, boardArr))
    window.bind("<Button-1>", mouseXY)

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


def toggleAB():
    if (debug):
        print("Toggled AB")
    global alphaBeta
    alphaBeta = not(alphaBeta)
    ABBtn.config(text=f"Alpha-Beta Pruning: {alphaBeta}")


def toggleCPU():
    if (debug):
        print("toggled CPU")
    global cpuOn
    cpuOn = not(cpuOn)
    cpuBtn.config(text = f"CPU: {cpuOn}")


def toggleColor():
    if (debug):
        print("toggled color")
    global user
    global cpu
    global globalTurn
    user, cpu = cpu, user
    globalTurn = user
    colorBtn.config(text = f"Player 1: {user}\tPlayer 2: {cpu}")

def toggleDebug():
    print("toggled debug")
    global debug
    debug = not(debug)
    debugBtn.config(text = f"Debug: {debug}")

def toggleHeur():
    if (debug):
        print("toggled heuristics")
    global heuristics
    heuristics = not(heuristics)
    heurBtn.config(text = f"Heuristics: {heuristics}")

def toggleTree():
    if (debug):
        print("toggled tree")
    global tree
    tree = not(tree)
    treeBtn.config(text = f"Tree: {tree}")

def toggleBoard():
    if (debug):
        print("toggled board")
    global boardDisp
    boardDisp = not(boardDisp)
    boardBtn.config(text = f"Board: {boardDisp}")

def toggleDepth():
    global depth

    depth += 1

    if (depth >= 11):
        depth = 1

    if (depth >= 5 and tree == True):
        toggleTree()

    if (debug):
        print(f"Depth changed to {depth}")

    depthBtn.config(text=f"Depth: {depth}")


canvas.grid(row=0, column=0, rowspan=8)
score.grid(row=0, column=1, columnspan=6, ipadx = 135, ipady = 20)

colorBtn.grid(row=1, column=1, columnspan=6, ipadx = 88, ipady = 20)

cpuBtn.grid(row=2, column=1, columnspan=2, ipadx = 40, ipady = 20)
startBtn.grid(row=2, column=3, columnspan=2, ipadx = 12, ipady = 20)
resetBtn.grid(row=2, column=5, columnspan=2, ipadx = 12, ipady = 20)

ABBtn.grid(row=3, column=1, columnspan=3, ipadx = 35, ipady = 20)
debugBtn.grid(row=3, column=4, columnspan=3, ipadx = 8, ipady = 20)

heurBtn.grid(row=4, column=1, columnspan=2, ipadx = 10, ipady = 20)
treeBtn.grid(row=4, column=3, columnspan=2, ipadx = 10, ipady = 20)
boardBtn.grid(row=4, column=5, columnspan=2, ipadx = 10, ipady = 20)

depthBtn.grid(row=5, column=1, columnspan=6, ipadx = 235, ipady = 20)

victor.grid(row=6, column=1, columnspan=6, ipadx = 295, ipady = 30)


colorBtn.config(command=toggleColor)

cpuBtn.config(command=toggleCPU)
startBtn.config(command=startGame)
resetBtn.config(command=resetGame)

ABBtn.config(command=toggleAB)
debugBtn.config(command=toggleDebug)

heurBtn.config(command=toggleHeur)
treeBtn.config(command=toggleTree)
boardBtn.config(command=toggleBoard)

depthBtn.config(command=toggleDepth)

drawBoard()

window.mainloop()