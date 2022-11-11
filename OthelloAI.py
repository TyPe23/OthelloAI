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

import tkinter as tk
import math
from time import sleep
import copy

window = tk.Tk()

boardHeur = [
    [10, -5, 8, 5, 5, 8, -5,10],
    [-5,-10,-3,-3,-3,-3,-10,-5],
    [ 8, -3, 6, 3, 3, 6, -3, 8],
    [ 5, -3, 3, 3, 3, 3, -3, 5],
    [ 5, -3, 3, 3, 3, 3, -3, 5],
    [ 8, -3, 6, 3, 3, 6, -3, 8],
    [-5,-10,-3,-3,-3,-3,-10,-5],
    [10, -5, 8, 5, 5, 8, -5,10],
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
turn = user
cpuOn = True

x = 0
y = 0
turnCount = 0
depth = 4

canvas = tk.Canvas(window, bg="green", height = 800, width=800)
score = tk.Label(window,  relief="raised",  font="Times 20 italic bold")
victor = tk.Label(window,  relief="raised",  font="Times 20 italic bold")


cpuBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"CPU: {cpuOn}") 
colorBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = f"Player 1: {user}\tPlayer 2: {cpu}") 
startBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = "Start Game") 
resetBtn = tk.Button(window,  relief="raised",  font="Times 20 italic bold", text = "Reset Game") 

def toggleCPU():
    print("toggled CPU")
    global cpuOn
    cpuOn = not(cpuOn)
    cpuBtn.config(text = f"CPU: {cpuOn}")

def toggleColor():
    print("toggled color")
    global user
    global cpu
    global turn
    user, cpu = cpu, user
    turn = user
    colorBtn.config(text = f"Player 1: {user}\tPlayer 2: {cpu}")



def placePiece(x, y, color):
    canvas.create_oval(x * 100 + 10, y * 100 + 10, x * 100 + 90, y * 100 + 90, fill=color)

def drawBoard():
    canvas.create_rectangle(0, 0, 800, 800, fill = "green")

    for i in range(1, 8):
        canvas.create_line(i * 100, 0, i * 100, 800)
        canvas.create_line(0, i * 100, 800, i * 100)

    #print("Board state:")
    for x in range(8):
        for y in range(8):
            if (boardArr[y][x] == 1):
                placePiece(x, y, "black")
            elif (boardArr[y][x] == 2):
                placePiece(x, y, "white")
        #print(f"{boardArr[x][0]},{boardArr[x][1]},{boardArr[x][2]},{boardArr[x][3]},{boardArr[x][4]},{boardArr[x][5]},{boardArr[x][6]},{boardArr[x][7]}")
    #print()

    blackScore, whiteScore = getScore()
    score.config(text = f"Black: {blackScore}\t\tWhite: {whiteScore}")


def getScore():
    blackScore = 0
    whiteScore = 0
    for x in range(8):
        for y in range(8):
            match boardArr[y][x]:
                case 0:
                    continue
                case 1:
                    blackScore += 1
                    continue
                case 2:
                    whiteScore += 1
                    continue
    return blackScore, whiteScore
    

def displayVictor():
    black, white = getScore()
    if (black > white):
        myText = "Black Wins!"
    elif (white > black):
        myText = "White Wins!"
    elif (white == black and white != 2):
        myText = "Tie!"
    else:
        myText = ""

    victor.grid(row=1, column=1, columnspan=3, ipadx = 185, ipady = 20, sticky="S")
    victor.config(text = myText)


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
            #print(f"{newX},{newY}")
            while (board[newY][newX] == valToCheck):
                board[newY][newX] = currVal
                newX -= xDir
                newY -= yDir
                if (newX > 7 or newX < 0 or newY > 7 or newY < 0):
                    break
                #print(f"{newX},{newY}")
    return board


def showValid(valid):
    for [x,y] in valid:
        placePiece(x, y, "yellow")
    window.update()


def validMoves(turn, board):

    valid = []

    for x in range(8):
        for y in range(8):
            if (checkPos(x, y, turn, board)):
                valid.append([x,y])
    #print(f"Valid moves: {valid}\n")

    return valid


def minimax(valid, depth, alpha, beta, turn, board):

    if (turn == user):
        nextTurn = cpu
    else:
        nextTurn = user
    
    tempBoard = copy.deepcopy(board)
    tempBoard = flipPieces(valid[0], valid[1], turn, tempBoard)
    next = validMoves(nextTurn, tempBoard) 

    if (depth == 0 or next == []) :
        return boardHeur[valid[1]][valid[0]]

    if (turn == user):
        maxEval = -100
        for [x,y] in next:
            #tempBoard = flipPieces(x, y, board)
            eval = minimax([x,y], depth - 1, alpha, beta, cpu, tempBoard)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if (beta <= alpha):
                break
        return maxEval

    else:
        minEval = 100
        for [x,y] in next:
            eval = minimax([x,y], depth - 1, alpha, beta, user, tempBoard)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if (beta <= alpha):
                break
        return minEval


def cpuMove(board):
    global turn
    global turnCount
    maxHeur = -11
    x = -1
    y = -1
    tempBoard = copy.deepcopy(board)
    valid = validMoves(turn, tempBoard)

    if (turnCount >= 2):
        displayVictor()

    for [tempx,tempy] in valid:
        tempVal = minimax([tempx, tempy], depth, -11, 11, cpu, tempBoard)
        if (tempVal > maxHeur):
            maxHeur = tempVal
            x = tempx
            y = tempy
    

    if (x != -1 or y != -1):
        print(f"CPU placed at: {x}, {y}\n")
        flipPieces(x, y, turn, board)
    elif (turnCount < 2):
        turnCount += 1
    else:
        displayVictor()

    turn = user
    showValid(valid)


def mouseXY(event):
    global x
    global y
    global turn
    x, y = math.floor(event.x / 100), math.floor(event.y / 100)

    valid = validMoves(turn, boardArr)

    if (valid == [] and turnCount <= 2):
        displayVictor()

    if (turn == user and [x,y] in valid):
        flipPieces(x,y, turn, boardArr)
        turn = cpu

    elif (not(cpuOn) and turn == cpu and [x,y] in valid):
        flipPieces(x,y, turn, boardArr)
        turn = user
    
    print(f"User placed at: {x}, {y}")
    print()

    
    drawBoard()

    if (cpuOn and turn == cpu):
        cpuMove(boardArr)
        sleep(0.5)
        drawBoard()

    showValid(validMoves(turn, boardArr))




def startGame():
    colorBtn.config(state="disabled")
    showValid(validMoves(turn, boardArr))
    window.bind("<Button-1>", mouseXY)

def resetGame():
    global boardArr
    global turn

    turn = user
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

    drawBoard()
    victor.config(text="")
    victor.grid(row=1, column=1, columnspan=3, ipadx = 260, ipady = 20, sticky="S")
    colorBtn.config(state="active")
    window.unbind("<Button-1>")



canvas.grid(row=0, column=0, rowspan=8)
score.grid(row=0, column=1, columnspan=3, ipadx = 96, ipady = 18, sticky="N")
colorBtn.grid(row=0, column=1, columnspan=3, ipadx = 50, ipady = 15, sticky= "S")
cpuBtn.grid(row=1, column=1, ipadx = 10, ipady = 15, sticky= "N")
startBtn.grid(row=1, column=2, ipadx = 10, ipady = 15, sticky="N")
resetBtn.grid(row=1, column=3, ipadx = 10, ipady = 15, sticky="N")
victor.grid(row=1, column=1, columnspan=3, ipadx = 260, ipady = 20, sticky="S")

cpuBtn.config(command=toggleCPU)
colorBtn.config(command=toggleColor)
startBtn.config(command=startGame)
resetBtn.config(command=resetGame)

drawBoard()

window.mainloop()