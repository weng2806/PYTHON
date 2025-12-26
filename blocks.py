"""
Author: Pamaran, Ruel Jr. P.
Date Started: November 13, 2025
Date Completed: December 25, 2025
Description: Definitions for Tetris blocks.
""" 

from block import Block
from position import Position

class lBlock(Block):                             # l-shaped block
	def __init__(self):                          # runs when l block is made
		super().__init__(blockId = 1)              # call parent block with id 1
		self.cells = {                           # rotation states for l block
			0: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],  # rotation 0
			1: [Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],  # rotation 1
			2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0)],  # rotation 2
			3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)]   # rotation 3
		}
		self.move(0, 3)                          # push block to the middle

class jBlock(Block):                             # j-shaped block
	def __init__(self):                          # runs when j block is made
		super().__init__(blockId = 2)              # call parent block with id 2
		self.cells = {                           # rotation states for j block
			0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],  # rotation 0
			1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],  # rotation 1
			2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],  # rotation 2
			3: [Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]   # rotation 3
		}
		self.move(0, 3)                          # push block to the middle

class iBlock(Block):                             # i-shaped block
	def __init__(self):                          # runs when i block is made
		super().__init__(blockId = 3)              # call parent block with id 3
		self.cells = {                           # rotation states for i block
			0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],  # rotation 0
			1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],  # rotation 1
			2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],  # rotation 2
			3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]   # rotation 3
		}
		self.move(-1, 3)                         # adjust spawn height and center

class oBlock(Block):                             # square block
	def __init__(self):                          # runs when o block is made
		super().__init__(blockId = 4)              # call parent block with id 4
		self.cells = {                           # only one rotation needed
			0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)]   # square shape
		}
		self.move(0, 4)                          # center the block

class sBlock(Block):                             # s-shaped block
	def __init__(self):                          # runs when s block is made
		super().__init__(blockId = 5)              # call parent block with id 5
		self.cells = {                           # rotation states for s block
			0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],  # rotation 0
			1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],  # rotation 1
			2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],  # rotation 2
			3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]   # rotation 3
		}
		self.move(0, 3)                          # center the block

class tBlock(Block):                             # t-shaped block
	def __init__(self):                          # runs when t block is made
		super().__init__(blockId = 6)              # call parent block with id 6
		self.cells = {                           # rotation states for t block
			0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],  # rotation 0
			1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],  # rotation 1
			2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],  # rotation 2
			3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]   # rotation 3
		}
		self.move(0, 3)                          # center the block

class zBlock(Block):                             # z-shaped block
	def __init__(self):                          # runs when z block is made
		super().__init__(blockId = 7)              # call parent block with id 7
		self.cells = {                           # rotation states for z block
			0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],  # rotation 0
			1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],  # rotation 1
			2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],  # rotation 2
			3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]   # rotation 3
		}
		self.move(0, 3)                          # center the block