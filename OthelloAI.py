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

window = tk.Tk()

canvas = tk.Canvas(window, bg="green", height = 800, width=800)
score = tk.Label(window, width=50, relief="raised", pady=10, font="Times 20 italic bold")
victor = tk.Label(window, width=50, relief="raised", pady=10, font="Times 20 italic bold")
score.pack(side="top")


x = 0
y = 0

valid = []

boardHeur = [
    [10,-5, 5, 5, 5, 5,-5,10],
    [-5,-5,-3,-3,-3,-3,-5,-5],
    [ 5,-3, 3, 3, 3, 3,-3,-5],
    [ 5,-3, 3, 3, 3, 3,-3,-5],
    [ 5,-3, 3, 3, 3, 3,-3,-5],
    [ 5,-3, 3, 3, 3, 3,-3,-5],
    [-5,-5,-3,-3,-3,-3,-5,-5],
    [10,-5, 5, 5, 5, 5,-5,10],
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




def placePiece(x, y, color):
    canvas.create_oval(x * 100 + 10, y * 100 + 10, x * 100 + 90, y * 100 + 90, fill=color)

def drawBoard():
    canvas.create_rectangle(0, 0, 800, 800, fill = "green")

    for i in range(1, 8):
        canvas.create_line(i * 100, 0, i * 100, 800)
        canvas.create_line(0, i * 100, 800, i * 100)

    for x in range(8):
        for y in range(8):
            if (boardArr[y][x] == 1):
                placePiece(x, y, "black")
            elif (boardArr[y][x] == 2):
                placePiece(x, y, "white")
        print(f"{boardArr[x][0]},{boardArr[x][1]},{boardArr[x][2]},{boardArr[x][3]},{boardArr[x][4]},{boardArr[x][5]},{boardArr[x][6]},{boardArr[x][7]}")
    print()

    blackScore, whiteScore = getScore()
    myText = f"Black: {blackScore}\t\t\tWhite: {whiteScore}"
    score.config(text = myText)


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
    else:
        myText = "Tie!"

    victor.config(text = myText)
    victor.pack(side="top")


def checkPos(x, y, board):

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


def flipPieces(x, y, board):
    valToCheck = 1
    currVal = 2

    if (turn == "black"):
        currVal, valToCheck = valToCheck, currVal

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
            print(f"{newX},{newY}")
            while (board[newY][newX] == valToCheck):
                board[newY][newX] = currVal
                newX -= xDir
                newY -= yDir
                if (newX > 7 or newX < 0 or newY > 7 or newY < 0):
                    break
                print(f"{newX},{newY}")


def validMoves(count, board):

    if (count >= 2):
        displayVictor()

    drawBoard()

    global valid
    global turn

    valid = []

    for x in range(8):
        for y in range(8):
            if (checkPos(x, y, board)):
                placePiece(x, y, "yellow")
                valid.append([x,y])
    print(valid)

    if (turn == user and valid == [] and count < 2):
        turn = cpu
        cpuMove(count + 1, board)

    elif (valid == [] and count < 2):
        turn = "black"
        validMoves(count + 1, board)



def cpuMove(count, board):
    global turn
    x = -1
    y = -1
    maxHeur = -11

    validMoves(count, board)

    for [tempx,tempy] in valid:
        if (boardHeur[tempy][tempx] > maxHeur):
            x = tempx
            y = tempy
            maxHeur = boardHeur[tempy][tempx]

    if (x != -1 or y != -1):
        if (cpu == "black"):
            boardArr[y][x] = 1
        else:
            boardArr[y][x] = 2
        print(f"CPU placed at: {x}, {y}")
        print()
        flipPieces(x,y, board)
    turn = user


def mouseXY(event):
    global x
    global y
    global turn
    x, y = math.floor(event.x / 100), math.floor(event.y / 100)

    if (turn == user and [x,y] in valid):
        flipPieces(x,y, boardArr)
        turn = cpu
        if (user == "black"):
            boardArr[y][x] = 1
        else:
            boardArr[y][x] = 2

    elif (not(cpuOn) and turn == cpu and [x,y] in valid):
        flipPieces(x,y, boardArr)
        turn = user
        if (cpu == "black"):
            boardArr[y][x] = 1
        else:
            boardArr[y][x] = 2
    
    print(f"User placed at: {x}, {y}")
    print()

    if (cpuOn and turn == cpu):
        cpuMove(0, boardArr)

    validMoves(0, boardArr)





validMoves(0, boardArr)

canvas.pack(side="left")
window.bind("<Button-1>", mouseXY)
window.mainloop()