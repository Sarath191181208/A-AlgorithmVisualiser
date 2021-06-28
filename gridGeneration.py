import random
import collections
import numpy as np


class Maze():
    """This class contains the relevant algorithms for creating and solving."""

    def __init__(self):
        """Constructor."""

        self._dir_one = [
            lambda x, y: (x + 1, y),
            lambda x, y: (x - 1, y),
            lambda x, y: (x, y - 1),
            lambda x, y: (x, y + 1)
        ]
        self._dir_two = [
            lambda x, y: (x + 2, y),
            lambda x, y: (x - 2, y),
            lambda x, y: (x, y - 2),
            lambda x, y: (x, y + 2)
        ]
        self._range = list(range(4))
        self.row_count = 10
        self.col_count = self.row_count
        self.maze = [[0 for i in range(self.row_count)]
                     for j in range(self.col_count)]

    @property
    def _random(self):
        """Returns a random range to iterate over."""
        random.shuffle(self._range)
        return self._range

    def _create_walk(self, x, y):
        """Randomly walks from one pointer within the maze to another one."""
        for idx in self._random:  # Check adjacent cells randomly
            tx, ty = self._dir_two[idx](x, y)
            # Check if unvisited
            if not self._out_of_bounds(tx, ty) and self.maze[tx][ty] == 0:

                self.maze[tx][ty] = self.maze[self._dir_one[idx](
                    x, y)[0]][self._dir_one[idx](x, y)[1]] = 1  # Mark as visited
                return tx, ty  # Return new cell

        return None, None  # Return stop values

    def _out_of_bounds(self, x, y):
        """Checks if indices are out of bounds."""
        return x < 0 or y < 0 or x >= self.row_count or y >= self.col_count

    def _create_backtrack(self, stack):
        """Backtracks the stack until walking is possible again."""
        while stack:
            x, y = stack.pop()
            for direction in self._dir_two:  # Check adjacent cells
                tx, ty = direction(x, y)
                # Check if unvisited
                if not self._out_of_bounds(tx, ty) and self.maze[tx][ty] == 0:
                    return x, y  # Return cell with unvisited neighbour

        return None, None  # Return stop values if stack is empty

    def _recursive_backtracking(self):
        """Creates a maze using the recursive backtracking algorithm."""
        stack = collections.deque()  # List of visited cells [(x, y), ...]

        x = random.randint(0, self.row_count - 1)
        y = random.randint(0, self.col_count - 1)
        self.maze[x][y] = 1  # Mark as visited

        while x and y:
            while x and y:
                stack.append((x, y))
                x, y = self._create_walk(x, y)
            x, y = self._create_backtrack(stack)


maze = Maze()
maze._recursive_backtracking()
print(maze.maze)
