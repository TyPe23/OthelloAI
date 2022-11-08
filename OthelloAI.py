import tkinter as tk
import math

window = tk.Tk()

canvas = tk.Canvas(window, bg="green", height = 800, width=800)

x = 0
y = 0

def placePiece(x, y, color):
    canvas.create_oval(x * 100, y * 100, x * 100 + 100, y * 100 + 100, fill=color)

for i in range(1, 8):
    canvas.create_line(i * 100, 0, i * 100, 800)
    canvas.create_line(0, i * 100, 800, i * 100)

def mouseXY(event):
    global x
    global y
    x, y = math.floor(event.x / 100), math.floor(event.y / 100)
    print(f"{x}, {y}")




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

placePiece(4, 4, "black")
placePiece(3, 3, "black")
placePiece(3, 4, "white")
placePiece(4, 3, "white")

canvas.pack()
window.bind("<Motion>", mouseXY)
window.mainloop()