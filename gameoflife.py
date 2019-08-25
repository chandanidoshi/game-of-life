"""
This is a simulation of Conway's Game of Life
(https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
In the game, a cell evolves according to the following rules:
1. Any live cell with fewer than two live neighbours dies, as if by underpopulation
2. Any live cell with two or three live neighbours lives on to the next generation
3. Any live cell with more than three live neighbours dies, as if by overpopulation
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction
"""

import argparse
import numpy as np


class GameOfLife(object):
    """
    A class used to represent Conway's Game of Life.
    The state at each timestep is represented by a set of live cells, and at each step,
    the state is updated based on the four rules of the game.

    Attributes:
        xsize: number of rows in game grid
        ysize: number of columns in game grid
        state: set of coordinates of live cells in current state
    """

    def __init__(self, xsize, ysize, file_path=None):
        self.xsize, self.ysize = xsize, ysize
        # Initialize state
        # Loads from file, if provided,
        # else initializes a random grid
        self.state = set()
        if file_path:
            grid = self.init_from_file(file_path)
        else:
            grid = self.init_random_board()
        self.initialize_state(grid)

    def init_random_board(self):
        """
        Initialize random grid
        :return: state matrix
        """
        grid = np.random.binomial(1, .5, size=(self.xsize, self.ysize))
        return grid

    def init_from_file(self, file_path):
        """
        Load initial state from file
        :param file_path: path of input initial state
        :return: state matrix
        """
        grid = np.loadtxt(file_path)
        self.xsize, self.ysize = grid.shape
        return grid

    def initialize_state(self, grid):
        """
        Convert state matrix into sparse representation,
        i.e., set containing coordinates of all live cells
        :param grid: state matrix
        """
        for i in range(self.xsize):
            for j in range(self.ysize):
                cell = (i, j)
                if grid[i, j] == 1:
                    self.state.add(cell)

    def get_state(self):
        """
        Convert sparse representation into state matrix
        :return: state matrix
        """
        grid = np.zeros((self.xsize, self.ysize))
        for x, y in self.state:
            grid[x, y] = 1
        return grid

    def get_neighbors(self, x, y):
        """
        Get coordinates of neighboring cells of cell (x,y)
        :param x: x-coordinate of cell
        :param y: y-coordinate of cell
        :return: list of neighbors
        """
        neighbors = []
        for i in range(max(0, x - 1), min(x + 2, self.xsize)):
            for j in range(max(0, y - 1), min(y + 2, self.ysize)):
                if i == x and j == y:
                    continue
                neighbors.append((i, j))
        return neighbors

    def step(self):
        """
        Update state based on rules of game
        """
        next_state = set()
        for i in range(self.xsize):
            for j in range(self.ysize):
                cell = (i, j)
                neighbors = self.get_neighbors(i, j)
                is_live = cell in self.state
                count = 0
                for neighbor in neighbors:
                    if neighbor in self.state:
                        count += 1
                if count == 3:
                    next_state.add(cell)
                elif count == 2 and is_live:
                    next_state.add(cell)
        self.state = next_state

    def run(self, generations):
        """
        Run game for specified number of generations
        :param generations: number of iterations to update state
        """
        for i in range(generations):
            self.step()

    def save_state(self, output_path):
        """
        Save state of game to file
        :param output_path: path of output file
        """
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

    game = GameOfLife(xsize, ysize, input_path)
    game.run(generations)
    game.save_state(output_path)


if __name__ == '__main__':
    main()
