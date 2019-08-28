"""
Test Conway's Game of Life

Get neighbors:
- neighbors of middle cell
- neighbors of corner cell
- neighbors when focal cell is included

Step:
- all cells are dead
- Rule 1: Any live cell with fewer than two live neighbours dies
- Rule 2: Any live cell with two or three live neighbours lives on
- Rule 3: Any live cell with more than three live neighbours dies
- Rule 4: Any dead cell with exactly three live neighbours becomes a live cell

Run:
- Run for more than 1 generation
"""

import unittest
import numpy as np
from gameoflife import GameOfLife


class TestGameOfLife(unittest.TestCase):

    def test_get_neighbors(self):
        game = GameOfLife(xsize=3, ysize=3)
        neighbors = game.get_neighbors(1, 1)
        self.assertEqual(len(neighbors), 8)
        self.assertIn((0, 0), neighbors)
        self.assertIn((0, 1), neighbors)
        self.assertIn((0, 2), neighbors)
        self.assertIn((1, 0), neighbors)
        self.assertIn((1, 2), neighbors)
        self.assertIn((2, 0), neighbors)
        self.assertIn((2, 1), neighbors)
        self.assertIn((2, 2), neighbors)

    def test_get_neighbors_corner(self):
        game = GameOfLife(xsize=3, ysize=3)
        neighbors = game.get_neighbors(0, 0)
        self.assertEqual(len(neighbors), 3)
        self.assertIn((0, 1), neighbors)
        self.assertIn((1, 0), neighbors)
        self.assertIn((1, 1), neighbors)

    def test_get_neighbors_with_focal(self):
        game = GameOfLife(xsize=3, ysize=3)
        game.set_include_focal()
        neighbors = game.get_neighbors(1, 0)
        self.assertEqual(len(neighbors), 6)
        self.assertIn((0, 0), neighbors)
        self.assertIn((0, 1), neighbors)
        self.assertIn((1, 0), neighbors)
        self.assertIn((1, 1), neighbors)
        self.assertIn((2, 0), neighbors)
        self.assertIn((2, 1), neighbors)

    def test_step_all_dead(self):
        initial_state = [[0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0]]
        next_state = np.array([[0, 0, 0],
                               [0, 0, 0],
                               [0, 0, 0]])

        game = GameOfLife(initial_state=initial_state)
        game.step()
        game_state = game.get_state()
        self.assertTrue(np.array_equal(game_state, next_state))

    def test_step_rule_1(self):
        initial_state = [[0, 1, 0],
                         [0, 1, 0],
                         [0, 0, 0]]
        next_state = np.array([[0, 0, 0],
                               [0, 0, 0],
                               [0, 0, 0]])

        game = GameOfLife(initial_state=initial_state)
        game.step()
        game_state = game.get_state()
        self.assertTrue(np.array_equal(game_state, next_state))

    def test_step_rule_2(self):
        initial_state = [[1, 1, 0],
                         [1, 1, 0],
                         [0, 0, 0]]
        next_state = np.array([[1, 1, 0],
                               [1, 1, 0],
                               [0, 0, 0]])

        game = GameOfLife(initial_state=initial_state)
        game.step()
        game_state = game.get_state()
        self.assertTrue(np.array_equal(game_state, next_state))

    def test_step_rule_3(self):
        initial_state = [[1, 1, 1],
                         [1, 1, 1],
                         [1, 1, 1]]
        next_state = np.array([[1, 0, 1],
                               [0, 0, 0],
                               [1, 0, 1]])

        game = GameOfLife(initial_state=initial_state)
        game.step()
        game_state = game.get_state()
        self.assertTrue(np.array_equal(game_state, next_state))

    def test_step_rule_4(self):
        initial_state = [[0, 1, 0],
                         [0, 1, 1],
                         [0, 0, 0]]
        next_state = np.array([[0, 1, 1],
                               [0, 1, 1],
                               [0, 0, 0]])

        game = GameOfLife(initial_state=initial_state)
        game.step()
        game_state = game.get_state()
        self.assertTrue(np.array_equal(game_state, next_state))

    def test_run(self):
        initial_state = [[1, 1, 1],
                         [1, 1, 1],
                         [1, 1, 1]]
        final_state = np.array([[0, 0, 0],
                                [0, 0, 0],
                                [0, 0, 0]])

        game = GameOfLife(initial_state=initial_state)
        game.run(generations=2)
        game_state = game.get_state()
        self.assertTrue(np.array_equal(game_state, final_state))


if __name__ == '__main__':
    unittest.main()
