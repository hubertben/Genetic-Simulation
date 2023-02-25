from tkinter import *
import random
import time

tk = Tk()
tk.title = "Simulation"
tk.resizable(0,0)
tk.wm_attributes("-topmost", 1)

canvas = Canvas(tk, width = 1000, height = 1000, bd = 0, highlightthickness = 0)
canvas.pack()

CELL_SIZE = 100

class Unit:

    def __init__(self, ID, genome, x, y, canvas, color):
        self.ID = ID
        self.genome = genome
        self.x = x
        self.y = y
        self.canvas = canvas
        self.color = color

class Grid:

    def __init__(self, canvas, width, height, cellSize):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.cellSize = cellSize

        self.units = []
        self.grid = []

        for i in range(self.width // self.cellSize): 
            self.grid.append([])
            for j in range(self.height // self.cellSize):
                self.grid[i].append([])

    def draw(self):
        for i in range(self.width // self.cellSize):
            for j in range(self.height // self.cellSize):
                self.canvas.create_rectangle(i * self.cellSize, j * self.cellSize, i * self.cellSize + self.cellSize, j * self.cellSize + self.cellSize, fill = "white", outline = "#cccccc")



def draw():
    tk.after(1, draw)


grid = Grid(canvas, 1000, 1000, CELL_SIZE)
grid.draw()
tk.mainloop()