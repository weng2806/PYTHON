""" 
Author: Pamaran, Ruel Jr. P.                     
Date Started: November 13, 2025                  
Date Completed: December 25, 2025                
Description: Base class for Tetris blocks.      
"""                                             

import pygame                                    
from colors import Colors                       
from position import Position                   

class Block:                                    # main block class
	def __init__(self, blockId):                 # runs when block is created
		self.blockId = blockId                   # id of the block
		self.cells = {}                          # stores block shapes
		self.cellSize = 30                       # size of one square
		self.rowOffset = 0                       # how far down the block is
		self.columnOffset = 0                    # how far left or right the block is
		self.rotationState = 0                   # current rotation index
		self.colors = Colors.getCellColors()     # get all block colors

	def move(self, rows, columns):               # move the block
		self.rowOffset += rows                  # move up or down
		self.columnOffset += columns            # move left or right

	def getCellPositions(self):                  # get the block cells on the grid
		tiles = self.cells[self.rotationState]  # get cells for current rotation
		movedTiles = []                          # list for moved cells
		for position in tiles:                   # loop through each cell
			position = Position(                # make a new position
				position.row + self.rowOffset,  # add row offset
				position.column + self.columnOffset  # add column offset
			)
			movedTiles.append(position)         # save the new position
		return movedTiles                        # send back all positions

	def rotate(self):                            # rotate the block forward
		self.rotationState += 1                  # go to next rotation
		if self.rotationState == len(self.cells):# if rotation goes too far
			self.rotationState = 0               # reset rotation

	def undoRotation(self):                      # rotate the block backward
		self.rotationState -= 1                  # go back one rotation
		if self.rotationState == -1:             # if it goes below zero
			self.rotationState = len(self.cells) - 1  # wrap to last rotation

	def draw(self, screen, offsetX, offsetY):    # draw the block on screen
		tiles = self.getCellPositions()          # get where cells should be
		for tile in tiles:                       # draw each cell
			tileRect = pygame.Rect(              # create a rectangle
				offsetX + tile.column * self.cellSize,  # x position
				offsetY + tile.row * self.cellSize,     # y position
				self.cellSize - 1,               # width with gap
				self.cellSize - 1                # height with gap
			)
			pygame.draw.rect(                    # draw the rectangle
				screen,                          # where to draw
				self.colors[self.blockId],       # color of the block
				tileRect                         # rectangle shape
			)

	def clone(self):                             # make a copy of the block
		copyBlock = type(self)()                 # create same block type
		copyBlock.cells = self.cells             # copy block shapes
		copyBlock.cellSize = self.cellSize       # copy cell size
		copyBlock.rowOffset = self.rowOffset     # copy row offset
		copyBlock.columnOffset = self.columnOffset  # copy column offset
		copyBlock.rotationState = self.rotationState  # copy rotation
		return copyBlock                         # return the copy

	def validMove(self, deltaRow, deltaColumn, grid):  # check if move is allowed
		for cell in self.getCellPositions():     # loop through block cells
			newRow = cell.row + deltaRow          # new row after move
			newCol = cell.column + deltaColumn    # new column after move

			if not grid.isInside(newRow, newCol): # outside the grid
				return False                     # move is not allowed
			if not grid.isEmpty(newRow, newCol): # hits another block
				return False                     # move is not allowed
		return True                              # move is safe