import argparse
import numpy as np


class Game:
	def __init__(self, xsize=50, ysize=50, file_path=None):
		self.xsize, self.ysize = xsize, ysize
		grid = []
		if file_path:
			grid = self.init_from_file(file_path)
		else:
			grid = self.init_random_board()
		self.state = self.initiliaze_state(grid)

	def is_valid_cell(self, x, y):
		return (0 <= x < self.xsize) and (0 <= y < self.ysize)

	def init_random_board(self):
		grid = np.random.binomial(1, .5, size=(self.xsize, self.ysize))

	def init_from_file(self, file_path):
		grid = np.loadtxt(file_path)
		self.xsize, self.ysize = grid.shape
		return grid

	def initiliaze_state(self, grid):
		for i in range(self.xsize):
			for j in range(self.ysize):
				cell = (i, j)
				if grid[i][j] == 1:
					self.state.add(cell)

	def toggle_state(self, x, y):
		if not self.is_valid_cell(x, y):
			raise ValueError("Coordinates ({}, {}) are out of bounds".format(x, y))
		cell = (x, y)
		if cell in self.state:
			self.state.remove(cell)
		else:
			self.state.add(cell)

	def get_neighbors(self, x, y):
		if not self.is_valid_cell(x, y):
			raise ValueError("Coordinates ({}, {}) are out of bounds".format(x, y))
		neighbors = []
		for i in range(max(0, x-1), min(x+2, self.xsize)):
			for j in range(max(0, y-1), min(y+2, self.ysize)):
				if i == x and j == y:
					continue
				neighbors.append((i, j))
		return neighbors

	def step(self):
		next_state = set()
		for i in range(self.xsize):
			for j in range(self.ysize):
				cell = (i, j)
				neighbors = self.get_neighbors(i, j)
				is_live = cell in self.state
				count = 0
				for m, n in neighbors:
					if (m, n) in self.state:
						count += 1
				if count == 3:
					next_state.add(cell)
				elif count == 2 and is_live:
					next_state.add(cell)
		self.state = next_state




