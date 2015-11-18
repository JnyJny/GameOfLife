'''Conway's Game of Life

See: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

This particular Game of Life is implemented as a two dimensional
world populated with cells.
'''

__author__ = '\n'.join(["Erik O'Shaughnessy",
                        'erik.oshaughnessy@gmail.com',
                        'https://github.com/JnyJny/GameOfLife'])
__version__ = "0.1.3"

from .cell import Cell as Cell
from .world import OptimizedWorld as World
from .world import OptimizedNumpyWorld as NumpyWorld
from .patterns import Patterns


__all__ = [ 'Cell','World','Patterns','tests',
            'NumpyWorld']

