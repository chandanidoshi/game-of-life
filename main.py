import argparse
import numpy as np


class Game:
	def __init__(self, xsize=50, ysize=50, file_path=None):
		self.xsize, self.ysize = xsize, ysize
		self.state = []
		if file_path:
			self.init_from_file(file_path)
		else:
			self.init_random_board()

	def is_valid_cell(self, x, y):
		return (0 <= x < self.xsize) and (0 <= y < self.ysize)

	def init_random_board(self):
		self.state = np.random.binomial(1, .5, size=(self.xsize, self.ysize))

	def init_from_file(self, file_path):
		self.state = np.loadtxt(file_path)

	def toggle_state(self, x, y):
		if not self.is_valid_cell(x, y):
			raise ValueError("Coordinates ({}, {}) are out of bounds".format(x, y))
		if self.state[x][y] == 1:
			self.state[x][y] = 0
		else:
			self.state[x][y] = 1

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
		pass




