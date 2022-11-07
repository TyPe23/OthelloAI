import tkinter as tk

window = tk.Tk()

for i in range(8):
    for j in range(8):
        frame = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1,
			highlightcolor="red",
			bg="green"
        )
        frame.grid(row=i, column=j)
        button = tk.Button(master=frame, text=f"\t\n\t", bg="green", fg="black", command=update())
        button.pack()

def update():
	pass



window.mainloop()