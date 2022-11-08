import tkinter as tk
import math

window = tk.Tk()

canvas = tk.Canvas(window, bg="green", height = 800, width=800)

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


def checkPos(x, y):

    valToCheck = 1
    currVal = 2

    if (turn == "black"):
        currVal, valToCheck = valToCheck, currVal

    

    if (boardArr[y][x] != 0):
        return False

    for xDir, yDir in [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]:
        newX, newY = x, y
        newX += xDir
        newY += yDir
        
        if (newX > 7 or newX < 0 or newY > 7 or newY < 0 or boardArr[newY][newX] == currVal):
            continue

        while (boardArr[newY][newX] == valToCheck):
            newX += xDir
            newY += yDir

            if (newX > 7 or newX < 0 or newY > 7 or newY < 0):
                newX -= xDir
                newY -= yDir
                break

        if (boardArr[newY][newX] == currVal):
            return True

    return False

def flipPieces(x, y):
    valToCheck = 1
    currVal = 2

    if (turn == "black"):
        currVal, valToCheck = valToCheck, currVal

    for xDir, yDir in [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]:
        newX, newY = x, y
        newX += xDir
        newY += yDir
        
        if (newX > 7 or newX < 0 or newY > 7 or newY < 0 or boardArr[newY][newX] == currVal):
            continue
        
        while (boardArr[newY][newX] == valToCheck):
            newX += xDir
            newY += yDir

            if (newX > 7 or newX < 0 or newY > 7 or newY < 0):
                newX -= xDir
                newY -= yDir
                break

        if (boardArr[newY][newX] == currVal):
            newX -= xDir
            newY -= yDir
            print(f"{newX},{newY}")
            while (boardArr[newY][newX] == valToCheck):
                boardArr[newY][newX] = currVal
                newX -= xDir
                newY -= yDir
                if (newX > 7 or newX < 0 or newY > 7 or newY < 0):
                    break
                print(f"{newX},{newY}")


def validMoves(count):
    drawBoard()

    global valid
    global turn

    valid = []

    for x in range(8):
        for y in range(8):
            if (checkPos(x, y)):
                placePiece(x, y, "yellow")
                valid.append([x,y])
    #print(valid)

    if (turn == "black" and valid == [] and count < 2):
        turn = "white"
        validMoves(count + 1)

    elif (valid == [] and count < 2):
        turn = "black"
        validMoves(count + 1)



def cpuMove():
    global turn
    x = -1
    y = -1
    maxHeur = -11

    validMoves(0)

    for [tempx,tempy] in valid:
        if (boardHeur[tempy][tempx] > maxHeur):
            x = tempx
            y = tempy
            maxHeur = boardHeur[tempy][tempx]

    
    if (x, y != -1, -1 and cpu == "black"):
        boardArr[y][x] = 1
    else:
        boardArr[y][x] = 2
    flipPieces(x,y)
    turn = user


def mouseXY(event):
    global x
    global y
    global turn
    x, y = math.floor(event.x / 100), math.floor(event.y / 100)

    if (turn == user and [x,y] in valid):
        flipPieces(x,y)
        turn = cpu
        if (user == "black"):
            boardArr[y][x] = 1
        else:
            boardArr[y][x] = 2

    elif (not(cpuOn) and turn == cpu and [x,y] in valid):
        flipPieces(x,y)
        turn = user
        if (cpu == "black"):
            boardArr[y][x] = 1
        else:
            boardArr[y][x] = 2
    
    print(f"Piece placed at: {x}, {y}")
    print()

    if (cpuOn and turn == cpu):
        cpuMove()
        print(f"Piece placed at: {x}, {y}")
        print()

    validMoves(0)


validMoves(0)


canvas.pack()
window.bind("<Button-1>", mouseXY)
window.mainloop()