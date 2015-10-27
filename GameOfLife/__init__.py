'''Conway's Game of Life

See: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

This particular Game of Life is implemented as a two dimensional
world populated with cells.
'''

__author__ = '\n'.join(["Erik O'Shaughnessy",
                        'erik.oshaughnessy@gmail.com',
                        'https://github.com/JnyJny/GameOfLife'])
__version__ = "0.0.13"

from .cell import Cell as Cell
from .world import OptimizedWorld as World
from .patterns import Patterns as Patterns

__all__ = [ 'Cell','World','Patterns','tests']




