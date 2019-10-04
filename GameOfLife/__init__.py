"""Conway's Game of Life

See: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

This particular Game of Life is implemented as a two dimensional
world populated with cells.
"""


from .cell import Cell as Cell
from .world import OptimizedNumpyWorld as World
from .patterns import Patterns

__all__ = ["Cell", "World", "Patterns", "console"]
