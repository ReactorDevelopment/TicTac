from Board import Board
from tkinter import *
from TacAi import TacAi

#initalizes program, and creates window
root = Tk()
root.title("Simple Pathfinder")
app = Board(root)

root.mainloop()