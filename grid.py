"""
Author: Pamaran, Ruel Jr. P.
Date Started: November 13, 2025
Date Completed: December 25, 2025
Description: Grid management for Tetris.
""" 

import pygame
from colors import Colors

class Grid:                                      # grid class for the board
    def __init__(self):                          # runs when grid is created
        self.numRows = 20                        # number of rows
        self.numCols = 10                        # number of columns
        self.cellSize = 30                       # size of each cell
        self.grid = [                            # 2d list for the grid
            [0 for j in range(self.numCols)]     # one row filled with zeros
            for i in range(self.numRows)         # repeat for each row
        ]
        self.colors = Colors.getCellColors()     # get colors for cells

    def printGrid(self):                         # print grid to console
        for row in range(self.numRows):          # loop through rows
            for column in range(self.numCols):   # loop through columns
                print(self.grid[row][column], end=" ")  # print cell value
            print()                              # new line after row

    def isInside(self, row, column):              # check if inside grid
        if row >= 0 and row < self.numRows and column >= 0 and column < self.numCols:
            return True                          # position is valid
        return False                             # position is outside

    def isEmpty(self, row, column):               # check if cell is empty
        if self.grid[row][column] == 0:           # zero means empty
            return True
        return False

    def isRowFull(self, row):                     # check if row is full
        for column in range(self.numCols):        # loop through columns
            if self.grid[row][column] == 0:       # found an empty cell
                return False
        return True                               # no empty cells found

    def clearRow(self, row):                      # clear one row
        for column in range(self.numCols):        # loop through columns
            self.grid[row][column] = 0            # set cell to empty

    def moveRowDown(self, row, numRows):          # move a row down
        for column in range(self.numCols):        # loop through columns
            self.grid[row + numRows][column] = self.grid[row][column]  # copy cell
            self.grid[row][column] = 0            # clear original cell

    def clearFullRows(self):                      # clear all full rows
        completed = 0                             # counter for cleared rows
        for row in range(self.numRows - 1, -1, -1):  # go bottom to top
            if self.isRowFull(row):               # if row is full
                self.clearRow(row)                # clear it
                completed += 1                    # add to counter
            elif completed > 0:                   # if rows were cleared below
                self.moveRowDown(row, completed)  # move row down
        return completed                          # return cleared count

    def reset(self):                              # reset the whole grid
        for row in range(self.numRows):           # loop through rows
            for column in range(self.numCols):    # loop through columns
                self.grid[row][column] = 0        # clear cell

    def draw(self, screen):                       # draw grid on screen
        for row in range(self.numRows):           # loop through rows
            for column in range(self.numCols):    # loop through columns
                cellValue = self.grid[row][column]  # get cell value
                cellRect = pygame.Rect(           # make cell rectangle
                    column * self.cellSize + 11,  # x position
                    row * self.cellSize + 11,     # y position
                    self.cellSize - 1,            # width
                    self.cellSize - 1             # height
                )
                pygame.draw.rect(                 # draw the cell
                    screen,                       # where to draw
                    self.colors[cellValue],       # color based on value
                    cellRect                      # rectangle shape
                )