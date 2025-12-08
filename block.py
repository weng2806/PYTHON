import pygame
from colors import Colors
from position import Position

class Block:
	def __init__(self, id):
		self.id = id
		self.cells = {}
		self.cell_size = 30
		self.row_offset = 0
		self.column_offset = 0
		self.rotation_state = 0
		self.colors = Colors.get_cell_colors()

	def move(self, rows, columns):
		self.row_offset += rows
		self.column_offset += columns

	def get_cell_positions(self):
		tiles = self.cells[self.rotation_state]
		moved_tiles = []
		for position in tiles:
			position = Position(position.row + self.row_offset, position.column + self.column_offset)
			moved_tiles.append(position)
		return moved_tiles

	def rotate(self):
		self.rotation_state += 1
		if self.rotation_state == len(self.cells):
			self.rotation_state = 0

	def undo_rotation(self):
		self.rotation_state -= 1
		if self.rotation_state == -1:
			self.rotation_state = len(self.cells) - 1

	def draw(self, screen, offset_x, offset_y):
		tiles = self.get_cell_positions()
		for tile in tiles:
			tile_rect = pygame.Rect(offset_x + tile.column * self.cell_size, 
				offset_y + tile.row * self.cell_size, self.cell_size -1, self.cell_size -1)
			pygame.draw.rect(screen, self.colors[self.id], tile_rect)

	def clone (self):
		copy = type(self)()   # Create a new instance of the same block class
		copy.cells = self.cells
		copy.cell_size = self.cell_size
		copy.row_offset = self.row_offset
		copy.column_offset = self.column_offset
		copy.rotation_state = self.rotation_state
		return copy
	
	def valid_move(self, delta_row, delta_column, grid):
		for cell in self.get_cell_positions():
			new_row = cell.row + delta_row
			new_col = cell.column + delta_column

			if not grid.is_inside(new_row, new_col):
				return False
			if not grid.is_empty(new_row, new_col):
				return False
		return True




   
        	