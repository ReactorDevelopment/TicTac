import Board
from Point import Point
import sys
import random

#class that represents a computer object
class TacAi:
    id = 0
    scanStr = "X"
    ourStr = "X"

    #sets the id and initalizes the board for the computer
    def __init__(self, id: int):
        self.id = id
        self.checked = [[0] * Board.Board.boardSize for _ in range(Board.Board.boardSize)]

    #resets the memory of which moves the computer has scanned for
    def clearChecked(self):
        self.checked = [[0] * Board.Board.boardSize for _ in range(Board.Board.boardSize)]

    #returns a relative point from a given directional string
    def coordsFromDir(self, x, y, direct: str):
        if direct == "LF":
            return Point(x-1, y)
        if direct == "RI":
            return Point(x+1, y)
        if direct == "TP":
            return Point(x, y-1)
        if direct == "BT":
            return Point(x, y+1)

        if direct == "BL":
            return Point(x-1, y+1)
        if direct == "TL":
            return Point(x-1, y-1)
        if direct == "BR":
            return Point(x+1, y+1)
        if direct == "TR":
            return Point(x+1, y-1)

    #switches between looking for ways for the computer or player to win
    def toggleScan(self):
        if self.scanStr == "X":
            self.scanStr = "O"
        else:
            self.scanStr = "X"

    #Scans each space of the board and uses recursion to check if a player has 2 or 3 tiles in a row
    def scanRecur(self, x, y, prevCmd: str):
        print("ScanCheck", x, y, prevCmd, "owner: "+Board.Board.board[y][x])
        self.checked[y][x] = 1
        numFound = int(prevCmd[2:3])
        if numFound == Board.Board.boardSize - 2 and self.scanStr != self.ourStr:
            blockingAt = self.coordsFromDir(x, y, prevCmd[0:2])
            if 0 <= blockingAt.x < Board.Board.boardSize and 0 <= blockingAt.y < Board.Board.boardSize:
                if Board.Board.board[blockingAt.y][blockingAt.x] == "":
                    print("Block: " + Board.Board.playerStr+" at "+str(blockingAt))
                    return Point(blockingAt.x, blockingAt.y)

        if numFound == Board.Board.boardSize - 1:
            print("winner: " + Board.Board.board[y][x])
            for i in range(len(Board.Board.board)):
                print()
                for j in range(len(Board.Board.board)):
                    if Board.Board.board[i][j] != "":
                        sys.stdout.write(str(Board.Board.board[i][j]) + " ")
                    else:
                        sys.stdout.write("_ ")

            return Point(0, 0)

        if x > 0 and Board.Board.board[y][x - 1] == self.scanStr and (prevCmd[0:2] == "LF" or prevCmd[0:2] == "NN") and self.checked[y][x - 1] != 1:
            # print("Current: "+prevCmd+" to LF")
            testPt = self.scanRecur(x - 1, y, "LF" + str(numFound + 1))
            if testPt is not None:
                return testPt
        if x < Board.Board.boardSize - 1 and Board.Board.board[y][x + 1] == self.scanStr and (prevCmd[0:2] == "RI" or prevCmd[0:2] == "NN") and self.checked[y][x + 1] != 1:
            testPt = self.scanRecur(x + 1, y, "RI" + str(numFound + 1))
            if testPt is not None:
                return testPt
        if y > 0 and Board.Board.board[y - 1][x] == self.scanStr and (prevCmd[0:2] == "TP" or prevCmd[0:2] == "NN") and self.checked[y - 1][x] != 1:
            testPt = self.scanRecur(x, y - 1, "TP" + str(numFound + 1))
            if testPt is not None:
                return testPt
        if y < Board.Board.boardSize - 1 and Board.Board.board[y + 1][x] == self.scanStr and (prevCmd[0:2] == "BT" or prevCmd[0:2] == "NN") and self.checked[y + 1][x] != 1:
            testPt = self.scanRecur(x, y + 1, "BT" + str(numFound + 1))
            if testPt is not None:
                return testPt

        if x > 0 and y > 0:
            if Board.Board.board[y - 1][x - 1] == self.scanStr and (prevCmd[0:2] == "TL" or prevCmd[0:2] == "NN") and self.checked[y - 1][x - 1] != 1:
                testPt = self.scanRecur(x - 1, y - 1, "TL" + str(numFound + 1))
                if testPt is not None:
                    return testPt
        if x < Board.Board.boardSize - 1 and y < Board.Board.boardSize - 1:
            if Board.Board.board[y + 1][x + 1] == self.scanStr and (prevCmd[0:2] == "BR" or prevCmd[0:2] == "NN") and self.checked[y + 1][x + 1] != 1:
                testPt = self.scanRecur(x + 1, y + 1, "BR" + str(numFound + 1))
                if testPt is not None:
                    return testPt
        if x < Board.Board.boardSize - 1 and y > 0:
            if Board.Board.board[y - 1][x + 1] == self.scanStr and (prevCmd[0:2] == "TR" or prevCmd[0:2] == "NN") and self.checked[y - 1][x + 1] != 1:
                testPt = self.scanRecur(x + 1, y - 1, "TR" + str(numFound + 1))
                if testPt is not None:
                    return testPt
        if x > 0 and y < Board.Board.boardSize - 1:
            if Board.Board.board[y + 1][x - 1] == self.scanStr and (prevCmd[0:2] == "BL" or prevCmd[0:2] == "NN") and self.checked[y + 1][x - 1] != 1:
                testPt = self.scanRecur(x - 1, y + 1, "BL" + str(numFound + 1))
                if testPt is not None:
                    return testPt
        return None

    #calls scanRecur for each space on the board
    def scanMoves(self):
        print("Scan moves")
        for i in range(Board.Board.boardSize):
            for j in range(Board.Board.boardSize):
                print("inloop", Board.Board.board[j][i], self.scanStr)
                if Board.Board.board[j][i] == self.scanStr:
                    self.clearChecked()
                    choice = self.scanRecur(i, j, "NN0")
                    if choice is not None:
                        if Board.Board.board[choice.y][choice.x] == "":
                            return choice
        return None

    #bases on the results of scanRecur, the computer decides which more is the best to make, if none then a random move is played
    def makeMove(self):
        choice = Point(0, 0)
        if Board.Board.board[int(Board.Board.boardSize / 2)][int(Board.Board.boardSize / 2)] == "":
            choice = Point(int(Board.Board.boardSize / 2), int(Board.Board.boardSize / 2))
            print("to middle", int(Board.Board.boardSize / 2), int(Board.Board.boardSize / 2), choice)
        else:
            self.scanStr = "O"
            choice = self.scanMoves()
            self.scanStr = "X"
        if choice is None:
            tmpX, tmpY = 0, 0
            while Board.Board.board[tmpY][tmpX] != "":
                tmpY = random.randint(0, Board.Board.boardSize-1)
                tmpX = random.randint(0, Board.Board.boardSize - 1)
            choice = Point(tmpX, tmpY)
        return choice
