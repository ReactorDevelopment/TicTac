from tkinter import *
import TacAi
from Point import Point


class Board(Frame):
    # Stores the canvas
    canvas: Canvas = None
    # Stores the player turn
    smolCanvas: Canvas = None
    # Width of canvas
    canvas_width = 600
    # Height of cancas
    canvas_height = 600
    # Color of current square
    currentColor = 476042
    # Weather currentColor is incrementing of decrementing
    upColor = True
    # Coordinates in pixels of last click on canvas
    x0, y0 = 0, 0
    # dimensions of one side of the board
    boardSize = 3
    # Tracks the player
    player = 0
    # Tracks the player symbol
    playerStr = "O"
    # keeps track of the board
    board = [[]]
    # Computer for the game
    ai = None

    # initializes window and calls make_widgets
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        Board.make_widgets(self, master)
        Board.board = [[""] * self.boardSize for _ in range(self.boardSize)]

        self.ai = TacAi.TacAi(0)
        self.smolCanvas.create_text(27, 27, text="0", anchor=CENTER, font=("Purisa", 20))
    # starts a turn, if the current player is a human, it awaits input, if a computer, it activates the computer
    def gameTurn(self):
        print("\nStart of turn", self.player)
        print("going in", self.player)
        #player cycling
        if self.player < 1:
            self.player = self.player + 1
        else:
            self.player = 0
        Board.playerStr = "O"
        if self.player == 1:
            Board.playerStr = "X"
        self.smolCanvas.delete("all")
        if self.player == 0:
            self.smolCanvas.create_text(27, 27, text="0", anchor=CENTER, font=("Purisa", 20))
        else:
            self.smolCanvas.create_text(27, 27, text="X", anchor=CENTER, font=("Purisa", 20))
        print("going out", self.player)
        #computer logic
        if self.player == 1:
            self.ai.clearChecked()
            choice = self.ai.makeMove()
            print("choice", choice)
            self.writeBox(choice.x*self.canvas_width/self.boardSize, choice.y*self.canvas_height/self.boardSize)
            self.gameTurn()
    #writes an x or an o to the inputed box
    def writeBox(self, x, y):
        print("writeBox", x, y, "(", int(self.boardSize * x / self.canvas_width), int(self.boardSize * y / self.canvas_height), ")")
        Board.board[int(self.boardSize * y / self.canvas_height)][
            int(self.boardSize * x / self.canvas_width)] = self.playerStr
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.canvas_width / self.boardSize * j <= x < self.canvas_width / self.boardSize * (
                        j + 1) and self.canvas_height / self.boardSize * i <= y < self.canvas_height / self.boardSize * (
                        i + 1):
                    self.canvas.create_text(
                        self.canvas_width / self.boardSize * j + self.canvas_width / self.boardSize / 2,
                        self.canvas_height / self.boardSize * i + self.canvas_height / self.boardSize / 2,
                        text=self.playerStr, anchor=CENTER, font=("Purisa", 30))

    #writes a symbol when clicking on the board, as well as updating the board for the computer
    def click(self, event):
        self.writeBox(event.x, event.y)
        self.gameTurn()
        print("Out of turn")
        self.ai.scanMoves()
    #rewrites the board to be blank
    def refreshCanvas(self):
        self.smolCanvas.create_rectangle(5, 5, 50, 50)
        for i in range(self.boardSize):
            self.canvas.create_line(self.canvas_width / self.boardSize * i, 0, self.canvas_width / self.boardSize * i,
                                    self.canvas_height)
            self.canvas.create_line(0, self.canvas_height / self.boardSize * i, self.canvas_width,
                                    self.canvas_height / self.boardSize * i)
    #completley resets the canvas
    def clearCanvas(self):
        self.canvas.delete("all")
        self.refreshCanvas()
        Board.board = [[""] * self.boardSize for _ in range(self.boardSize)]
        self.ai = TacAi.TacAi(0)

    #creates the board and applet
    def make_widgets(self, master):
        self.smolCanvas = Canvas(master, width=50, height=50)
        self.smolCanvas.grid(row=0, column=1, sticky=E, padx=2)
        reset = Button(master, width=10, height=2, text="Reset", command=self.clearCanvas)
        reset.grid(row=0, column=0, sticky=N, pady=5)
        self.canvas = Canvas(master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.bind("<ButtonPress-1>", self.click)
        self.canvas.grid(row=1, column=0, sticky=W, pady=2)
        self.refreshCanvas()
