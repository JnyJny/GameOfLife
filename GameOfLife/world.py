"""
"""

from . import Cell
from .patterns import Patterns as BuiltinPatterns

import numpy as np
from itertools import product


class World:
    """
    The game World is a two dimensional grid populated with Cells.

    >>> w = World()
    >>> w[0]
    Cell(location=(0,0),...)

    >>> w[x,y]
    Cell(location=(x,y),...)

    >> w.step()
    >> print(w)

    """

    @classmethod
    def from_string(cls, world_string, cell_class=None, rule=None, eol="\n"):
        """
        XXX missing doc string
        """
        w = cls(cell_class, 0, 0)
        w.add_pattern(world_string, 0, 0, rule=rule, eol=eol, resize=True)
        return w

    @classmethod
    def from_file(cls, fileobj, cell_class=None, rule=None, eol="\n"):
        """
        XXX missing doc string
        """
        w = cls(cell_class, 0, 0)
        w.read(fileobj, rule=rule, eol=eol)
        return w

    def __init__(self, width=80, height=23, cell_class=None):
        """
        :param int width:
        :param int height:
        :param Cell cell_class:

        Creates a world populated with cells created with
        the cell_class.  The world is a rectangular grid
        whose dimensions are specified by width and height.

        Will raise a TypeError if the supplied cell_class is
        not a subclass of Cell.

        """
        self.generation = 0
        self.width = int(width)
        self.height = int(height)

        self.cell_class = cell_class or Cell

        if not issubclass(self.cell_class, Cell):
            raise TypeError("expecting subclass of Cell, got {type(cell_class)}")

        self.reset()

    @property
    def cells(self):
        """
        A list of all Cell objects managed by the world.
        """

        try:
            return self._cells
        except AttributeError:
            pass

        self._cells = []
        return self._cells

    def __str__(self):
        """
        """
        s = []
        for y in range(self.height):
            r = ""
            for x in range(self.width):
                r += str(self[x, y])
            s.append(r)
        return "\n".join(s)

    def __repr__(self):
        """
        """

        s = [
            "{self.__class__.__name__}",
            "(cell_class={self.cell_class.__name__},",
            "width={self.width},",
            "height={self.height})",
        ]

        return "".join(s).format(self=self)

    def write(self, fileobj):
        """
        :param: fileobj - File-like object or string
        :return: number of bytes written

        XXX missing doc string
        """
        try:
            nbytes = fileobj.write(str(self))
            return nbytes
        except AttributeError:
            pass

        f = open(fileobj, "w")
        nbytes = f.write(str(self))
        return nbytes

    def read(self, fileobj, rule=None, eol="\n"):
        """
        XXX missing doc string
        """
        try:
            pattern = fileobj.read()
        except AttributeError:
            # XXX could throw file not found
            pattern = open(fileobj, "r").read()

        self.add_pattern(pattern, resize=True)

    def _warp(self, key):
        """
        :param: key - tuple of x,y integer values

        Implements wrapping of x,y coordinates to form an wrapping grid.
        """
        x, y = map(int, key)
        x %= self.width
        y %= self.height
        return x, y

    def __getitem__(self, key):
        """
        :key: tuple, integer or slice
        :return: Cell or list of Cells

        If tuple, it should be a two entry tuple whose first item is
        the X coordinate and the second is the Y coordinate.

        :tuple: returns the Cell at (X,Y)
        :integer: returns the i-th Cell in the list
        :slice: returns Cells or Cell satisfying the slice.

        """
        try:
            x, y = self._warp(key)
            return self.cells[(y * self.width) + x]
        except TypeError:
            pass

        return self.cells[key]

    def reset(self):
        """
        Resets the simulation to base state:
        - sets generation to zero
        - deletes all cells and allocates a new set cells
        """
        self.generation = 0
        self.cells.clear()
        for y in range(self.height):
            for x in range(self.width):
                self.cells.append(self.cell_class(x, y))

        for cell in self:
            cell.neighbors.extend([self[loc] for loc in cell.neighbor_locations])

    def step(self):
        """
        :return: None

        This method advances the simulation one generation.

        First all cells are updated with the current count of alive
        neighbors (which drives the cell state).

        Second all cells are asked to determine their next state.

        """
        self.generation += 1

        for c in self:
            c.think()

        for c in self:
            c.act()

    def add_named_pattern(self, name, x=0, y=0, rule=None, eol="\n", resize=False):
        """
        :param str name:
        :param int x:
        :param int y:
        :param callable rule:
        :param str eol:
        :param bool resize:
        :return: set of visited cells
        """

        return self.add_pattern(
            BuiltinPatterns[name], x=x, y=y, rule=rule, eol=eol, resize=resize
        )

    def add_pattern(self, pattern, x=0, y=0, rule=None, eol="\n", resize=False):
        """
        :param str pattern:
        :param int x:
        :param int y:
        :param callable rule: optional function with signature 'f(x) returns boolean'
        :param str eol: optional character that marks the end of a line in
                      the string
        :param bool resize: optional boolean, resizes world to pattern
        :return: set of visited cells

        This method uses the pattern string to affect the alive/dead
        state of cells in the world.  The x and y paramters can be used
        to place the pattern at an arbitrary position in the world.

        The first character in the string corresponds to coordinate (0,0).

        The rule parameter can be used to specify the rule for determining
        how to interpret each item in the string in terms of alive or dead.

        """

        if rule is None:
            rule = lambda c: not c.isspace()

        if resize:
            self.height = len(pattern.split(eol))
            self.width = max([len(l) for l in pattern.split(eol)])
            self.reset()

        visited = set()
        for Y, line in enumerate(pattern.split(eol)):
            for X, c in enumerate(line):
                self[x + X, y + Y].alive = int(rule(c))
                visited.add(self[x + X, y + Y])
        return visited


class OptimizedWorld(World):
    """
    The game World is a two dimensional grid populated with Cells.

    >>> w = World()
    >>> w[0]
    Cell(location=(0,0),...)

    >>> w[x,y]
    Cell(location=(x,y),...)

    >> w.step()
    >> print(w)

    This world has an optimized step method that only updates live
    cells and their neighbors rather than all cells, live or dead.
    """

    @property
    def alive(self):
        try:
            return self._alive
        except AttributeError:
            pass
        self._alive = set()
        return self._alive

    def reset(self):
        """
        Resets the simulation to base state:
        - sets generation to zero
        - deletes all cells and allocates a new set cells
        - creates an empty list of live cells
        """
        super().reset()
        self.alive.clear()
        self.alive.update(set([c for c in self if c.alive]))

    def add_pattern(self, pattern, **kwds):
        """
        :param: pattern - string
        :param: x - optional integer
        :param: y - optional integer
        :param: rule - optional function with signature 'f(x) returns boolean'
        :param: eol - optional character that marks the end of a line in
                      the string
        :param: resize - optional boolean, resizes world to pattern
        :return: None

        This method uses the pattern string to affect the alive/dead
        state of cells in the world.  The x and y paramters can be used
        to place the pattern at an arbitrary position in the world.

        The first character in the string corresponds to coordinate (0,0).

        Updates the set of live cells.
        """

        visited = super().add_pattern(pattern, **kwds)

        self.alive.update(set([c for c in visited if c.alive]))

    def step(self):
        """
        :return: set of cells currently alive

        This method advances the simulation one generation.

        It is optimized to only update cells which are alive and
        their immediate neighbors which results in significant gains
        in preformance compared to the super class' step method.

        Set operations are used to ensure that alive and neighbor
        cells are only visited once during each phase; neighbor
        count and state update.
        """
        self.generation += 1

        borders = set()

        for c in self.alive:
            borders.update(c.neighbors)

        self.alive.update(borders)

        for cell in self.alive:
            cell.think()

        deaders = set()
        for cell in self.alive:
            cell.act()
            if not cell.alive:
                deaders.add(cell)

        return self.alive.difference_update(deaders)


class NumpyWorld(World):
    """
    """

    def __init__(self, width=80, height=23):
        """
        """
        self.generation = 0
        self.width = int(width)
        self.height = int(height)
        self.markers = [" ", "."]

    def __repr__(self):

        s = [
            "{self.__class__.__name__}",
            "(width={self.width},",
            "height={self.height})",
        ]

        return "".join(s).format(self=self)

    def __str__(self):

        s = []
        for y in range(self.height):
            r = ""
            for x in range(self.width):
                r += self.markers[self.cells[y, x] > 0]
            s.append(r)
        return "\n".join(s)

    @property
    def cells(self):
        """A 2-D numpy array of cells.
        """
        try:
            return self._cells
        except AttributeError:
            pass
        self._cells = np.zeros((self.height, self.width), dtype=np.int)
        return self._cells

    @property
    def state(self):
        """
        Intermediate buffer to hold cell state information.
        """
        try:
            return self._state
        except AttributeError:
            pass
        self._state = np.zeros((self.height, self.width), dtype=np.int)
        return self._state

    @property
    def alive(self):
        """
        Returns a list of (x,y) coordinates of cells that are alive.
        """
        coords = self.cells.nonzero()
        return [(x, y) for x, y in zip(coords[1], coords[0])]

    def _warp(self, key):
        """
        """
        x, y = key
        h, w = self.cells.shape
        return (x % (w - 1), y % (h - 1))

    def __getitem__(self, key):
        """
        """
        x, y = self._warp(key)
        return self.cells[y, x]

    def __setitem__(self, key, value):
        """
        """
        x, y = self._warp(key)
        self.cells[y, x] = value

    def __iter__(self):
        """
        """
        self._x = 0
        self._y = 0
        return self

    def next(self):
        """
        """
        v = self[self._x, self._y]
        x, y = self._x, self._y
        self._x += 1
        if self._x not in range(self.width):
            self._x = 0
            self._y += 1
        if self._y not in range(self.height):
            raise StopIteration()

        return x, y, v

    def read(self, fileobj):
        """
        """
        raise NotImplementedError("read")

    def write(self, fileobj):
        """
        """
        raise NotImplementedError("write")

    def add_pattern(self, pattern, x=0, y=0, rule=None, eol="\n", resize=False):
        """
        """

        if rule is None:
            rule = lambda c: not c.isspace()

        if resize:
            self.height = len(pattern.split(eol))
            self.width = max([len(l) for l in pattern.split(eol)])
            self.reset()

        visited = set()
        for Y, line in enumerate(pattern.split(eol)):
            for X, c in enumerate(line):
                coord = x + X, y + Y
                self[coord] = int(rule(c))
                visited.add(coord)
        return visited

    def reset(self):
        """
        """
        self.generation = 0
        self.cells.fill(0)

    def neighbors(self, x, y):
        """
        """
        return list(product([x - 1, x, x + 1], [y - 1, y, y + 1]))

    def calculate_state_for(self, x, y, born=None, live=None):
        """
        """

        born = born or [3]
        live = live or [2, 3]

        # build a 3x3 array of neighbor values for cell at x,y

        neighbors = np.array([self[key] for key in self.neighbors(x, y)]) > 0
        neighbors.shape = (3, 3)
        neighbors[1, 1] = 0  # target cell doesn't contribute to state

        # sum the state of the neighbors
        v = neighbors.sum()

        state = 0  # start off assuming dead

        if (self[x, y] == 0) and (v in born):
            state = 1

        if (self[x, y] > 0) and (v in live):
            state = self[x, y] + 1

        # XXX why are coords swapped?
        self.state[y, x] = state

    def update_state(self):
        """
        """

        self.state.fill(0)
        for x, y in self.candidates:
            self.calculate_state_for(x, y)

    def update_cells(self):
        """
        """

        alive = self.state.nonzero()

        self.cells.fill(0)

        self.cells[alive] = self.state[alive]

    @property
    def candidates(self):
        """
        A list of the x,y coordinates of all "cells" in the world.
        """

        try:
            return self._candidates
        except AttributeError:
            pass
        self._candidates = [
            (x, y) for x in range(self.width) for y in range(self.height)
        ]
        return self._candidates

    def step(self):
        """
        """
        self.update_state()
        self.update_cells()
        self.generation += 1

    def _go(self, steps=-1):
        try:
            while self.generation != steps:
                print(self)
                self.step()
        except KeyboardInterrupt:
            pass


class OptimizedNumpyWorld(NumpyWorld):
    @property
    def candidates(self):
        """
        A list of alive cells and their immediate (dead) neighbors.
        """
        n = set()
        for x, y in self.alive:
            for key in self.neighbors(x, y):
                n.add(self._warp(key))
        return n
