import argparse
import numpy as np


class Game:
	def __init__(self, xsize=50, ysize=50, file_path=None):
		self.xsize, self.ysize = xsize, ysize
		self.state = set()
		if file_path:
			grid = self.init_from_file(file_path)
		else:
			grid = self.init_random_board()
		self.initiliaze_state(grid)

	def init_random_board(self):
		grid = np.random.binomial(1, .5, size=(self.xsize, self.ysize))
		return grid

	def init_from_file(self, file_path):
		grid = np.loadtxt(file_path)
		self.xsize, self.ysize = grid.shape
		return grid

	def initiliaze_state(self, grid):
		for i in range(self.xsize):
			for j in range(self.ysize):
				cell = (i, j)
				if grid[i, j] == 1:
					self.state.add(cell)

	def get_state(self):
		grid = np.zeros((self.xsize, self.ysize))
		for x, y in self.state:
			grid[x, y] = 1
		return grid

	def get_neighbors(self, x, y):
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

	def run(self, generations):
		for i in range(generations):
			self.step()

	def save_state(self, output_path):
		np.savetxt(output_path, self.get_state())


def main():
	parser = argparse.ArgumentParser(description="Conway's Game of Life")

	parser.add_argument("-x", "--xsize", dest='xsize', required=False,
		default=50, help="specify number of rows (default: 50)")
	parser.add_argument("-y", "--ysize", dest='ysize', required=False, 
		default=50, help="specify number of columns (default: 50)")
	parser.add_argument("-i", "--input-path", dest='input_path', required=False, 
		help="path of input file (default: generate random board)")
	parser.add_argument("-o", "--output-path", dest='output_path', required=False,
		default="final_state.txt", help="path of output file")
	parser.add_argument("-n", "--generations", dest='generations', required=False,
		default=50, help="specify number of generations (default: 50)")

	args = parser.parse_args()

	xsize = int(args.xsize)
	ysize = int(args.ysize)
	generations = int(args.generations)
	input_path = None
	if args.input_path:
		input_path = args.input_path
	output_path = args.output_path

	game = Game(xsize, ysize, input_path)
	game.run(generations)
	game.save_state(output_path)


if __name__ == '__main__':
	main()


