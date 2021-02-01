# This Python file uses the following encoding: utf-8
import sys
import os
import copy

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt, QCoreApplication, QObject, Slot, Signal, Property
from PySide2.QtQml import QQmlApplicationEngine, QQmlDebuggingEnabler


class TicTacSolver(QObject):
    def __init__(self):
        super().__init__()

    makeMove = Signal(int, str, arguments=['index', 'player']) #tell QML which move to make

    zeroWon = Signal()

    matchDraw = Signal()

    # keeps track of board arrangement
    gridValues = [None] * 9

    # tell QML what python predicted
    @Slot(int, str)
    def updateGrid(self, index, value):
        self.gridValues[index] = value


    # this will be called by QML to test if player has won
    @Slot(result=bool)
    def isWinner(self):

        gridValues = self.gridValues
        for i in range(3):
            if gridValues[i] != None and gridValues[i] == gridValues[i+3] and gridValues[i] == gridValues[i+6]:
                self.gridValues = [None] * 9
                return True

            if gridValues[i*3] != None and gridValues[i*3] == gridValues[i*3+1] and gridValues[i*3] == gridValues[i*3+2]:
                self.gridValues = [None] * 9
                return True

        if gridValues[0] != None and gridValues[0] == gridValues[4] != None and gridValues[0] == gridValues[8] != None:
            self.gridValues = [None] * 9
            return True

        if gridValues[2] != None and gridValues[2] == gridValues[4] != None and gridValues[2] == gridValues[6] != None:
            self.gridValues = [None] * 9
            return True

        return False


    # this is used for internal purpose
    # same as above function but takes argument a temporary board arrangement
    def isWinner2(self, board):

        gridValues = board
        for i in range(3):
            if gridValues[i] != None and gridValues[i] == gridValues[i+3] and gridValues[i] == gridValues[i+6]:
                return True

            if gridValues[i*3] != None and gridValues[i*3] == gridValues[i*3+1] and gridValues[i*3] == gridValues[i*3+2]:
                return True

        if gridValues[0] != None and gridValues[0] == gridValues[4] != None and gridValues[0] == gridValues[8] != None:
            return True

        if gridValues[2] != None and gridValues[2] == gridValues[4] != None and gridValues[2] == gridValues[6] != None:
            return True

        return False

    def isDraw(self):
        if None in self.gridValues:
            return False
        else:
            return True


    @Slot()
    def smartAI(self):

        if self.isDraw():
            self.gridValues = [None] * 9
            self.matchDraw.emit()

        for i in range(9):
            boardCopy = copy.deepcopy(self.gridValues)

            if boardCopy[i] == None: #can play at position
                boardCopy[i] = '0'
                if self.isWinner2(boardCopy):
                    self.gridValues[i] = '0'
                    self.makeMove.emit(i, '0')
                    if self.isWinner():
                        self.zeroWon.emit()
                    return


        for i in range(9):
            boardCopy = copy.deepcopy(self.gridValues)

            if boardCopy[i] == None: #can play at position
                boardCopy[i] = 'X'
                if self.isWinner2(boardCopy):
                    self.gridValues[i] = '0'
                    self.makeMove.emit(i, '0')
                    if self.isWinner():
                        self.zeroWon.emit()
                    return

        def smartMoves(a, b, c):

            if boardCopy[a]== 'X':
                if boardCopy[b] == None:
                    self.gridValues[b] = '0'
                    self.makeMove.emit(b, '0')
                    if self.isWinner():
                        self.zeroWon.emit()
                    return True
                elif boardCopy[c] == None:
                    self.gridValues[c] = '0'
                    self.makeMove.emit(c, '0')
                    if self.isWinner():
                        self.zeroWon.emit()
                    return True

            return False

        if smartMoves(4, 0, 2):
            return

        if smartMoves(0, 4, 3):
            return

        if smartMoves(2, 4, 1):
            return

        if smartMoves(6, 4, 7):
            return

        if smartMoves(8, 4, 5):
            return

        if smartMoves(1, 4, 2):
            return

        if smartMoves(3, 4, 0):
            return

        if smartMoves(5, 4, 8):
            return

        if smartMoves(7, 4, 6):
            return

        #if nothing else works, just do what's possible
        for i in range(9):
            if boardCopy[i] == None:
                self.gridValues[i] = '0'
                self.makeMove.emit(i, '0')
                return



if __name__ == "__main__":
    QQmlDebuggingEnabler()
    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()

    tictac = TicTacSolver()
    ctx.setContextProperty("solver", tictac)

    engine.load("main.qml")

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
