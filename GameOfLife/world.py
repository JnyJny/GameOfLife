
from . import Cell
from .patterns import Patterns as BuiltinPatterns

import numpy as np

class World(object):
    '''
    The game World is a two dimensional grid populated with Cells.

    >>> w = World()
    >>> w[0]
    Cell(location=(0,0),...)

    >>> w[x,y] 
    Cell(location=(x,y),...)

    >> w.step()
    >> print(w)

    '''
    
    @classmethod
    def fromString(cls,worldString,CellClass=None,rule=None,eol='\n'):
        '''
        XXX missing doc string
        '''
        w = cls(CellClass,0,0,)
        w.addPattern(worldString,0,0,rule=rule,eol=eol,resize=True)
        return w

    @classmethod
    def fromFile(cls,fileobj,CellClass=None,rule=None,eol='\n'):
        '''
        XXX missing doc string
        '''
        w = cls(CellClass,0,0)
        w.read(fileobj,rule=rule,eol=eol)
        return w
    
    def __init__(self,width=80,height=23,CellClass=None):
        '''
        :param: width - integer
        :param: height - integer
        :param: CellClass - subclass of Cell

        Creates a world populated with cells created with
        the CellClass.  The world is a rectangular grid
        whose dimensions are specified by width and height.

        Will raise a TypeError if the supplied CellClass is
        not a subclass of Cell. 

        '''
        self.generation = 0
        self.width = int(width)
        self.height = int(height)

        if CellClass is None:
            CellClass = Cell
            
        if not issubclass(CellClass,Cell):
            msg = 'expecting subclass of Cell, got {klass}'
            raise TypeError(msg.format(klass=CellClass))
        
        self.cellClass = CellClass
        self.reset()

    @property
    def cells(self):
        '''
        A list of all Cell objects managed by the world.
        '''
        
        try:
            return self._cells
        except AttributeError:
            pass
        
        self._cells = []
        return self._cells

    def __str__(self):
        '''
        '''
        s = []
        for y in range(self.height):
            r = ''
            for x in range(self.width):
                r += str(self[x,y])
            s.append(r)
        return '\n'.join(s)

    def __repr__(self):
        '''
        '''
        
        s = [ '{self.__class__.__name__}',
              '(CellClass={self.cellClass.__name__},',
              'width={self.width},',
              'height={self.height})']
        
        return ''.join(s).format(self=self)

    def write(self,fileobj):
        '''
        :param: fileobj - File-like object or string
        :return: number of bytes written

        XXX missing doc string
        '''
        try:
            nbytes = fileobj.write(str(self))
            return nbytes
        except AttributeError:
            pass
        
        f = open(fileobj,'w')
        nbytes = f.write(str(self))
        return nbytes

    def read(self,fileobj,rule=None,eol='\n'):
        '''
        XXX missing doc string
        '''
        try:
            pattern = fileobj.read()
        except AttributeError:
            f = open(fileobj,'r')
            pattern = f.read()
            
        self.addPattern(pattern,resize=True)

    def _warp(self,key):
        '''
        :param: key - tuple of x,y integer values

        Implements wrapping of x,y coordinates to form an wrapping grid.
        '''
        x,y = map(int,key)
        x %= self.width
        y %= self.height
        return x,y
        
    def __getitem__(self,key):
        '''
        :key: tuple, integer or slice
        :return: Cell or list of Cells

        If tuple, it should be a two entry tuple whose first item is
        the X coordinate and the second is the Y coordinate.

        :tuple: returns the Cell at (X,Y)
        :integer: returns the i-th Cell in the list
        :slice: returns Cells or Cell satisfying the slice.

        '''
        try:
            x,y = self._warp(key)
            return self.cells[(y * self.width)+x]
        except TypeError:
            pass
        
        return self.cells[key]

            
    def reset(self):
        '''
        Resets the simulation to base state:
        - sets generation to zero
        - deletes all cells and allocates a new set cells
        '''
        self.generation = 0
        self.cells.clear()
        for y in range(self.height):
            for x in range(self.width):
                self.cells.append(self.cellClass(x,y))

        for cell in self:
            cell.neighbors.extend([self[loc] for loc in cell.neighborLocations])

    def step(self):
        '''
        :return: None

        This method advances the simulation one generation.

        First all cells are updated with the current count of alive
        neighbors (which drives the cell state).

        Second all cells are asked to determine their next state.

        '''
        self.generation += 1

        for c in self:
            c.think()

        for c in self:
            c.act()

            
    def addPattern(self,pattern,x=0,y=0,rule=None,eol='\n',resize=False):
        '''
        :param: pattern - string 
        :param: x - optional integer
        :param: y - optional integer
        :param: rule - optional function with signature 'f(x) returns boolean'
        :param: eol - optional character that marks the end of a line in the string
        :param: resize - optional boolean, resizes world to pattern

        :return: set of visited cells

        This method uses the pattern string to affect the alive/dead
        state of cells in the world.  The x and y paramters can be used
        to place the pattern at an arbitrary position in the world.

        The first character in the string corresponds to coordinate (0,0).

        The rule parameter can be used to specify the rule for determining
        how to interpret each item in the string in terms of alive or dead.

        '''

        try:
            pattern =  BuiltinPatterns[pattern]
        except KeyError:
            pass

        if rule is None:
            rule = lambda c: not c.isspace()

        if resize:
            self.height = len(pattern.split(eol))
            self.width  = max([len(l) for l in pattern.split(eol)])
            self.reset()
        
        visited = set()
        for Y,line in enumerate(pattern.split(eol)):
            for X,c in enumerate(line):
                self[x+X,y+Y].alive = int(rule(c))
                visited.add(self[x+X,y+Y])
        return visited
    

class OptimizedWorld(World):
    '''
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
    '''

    @property
    def alive(self):
        try:
            return self._alive
        except AttributeError:
            pass
        self._alive = set()
        return self._alive
    
    def reset(self):
        '''
        Resets the simulation to base state:
        - sets generation to zero
        - deletes all cells and allocates a new set cells
        - creates an empty list of live cells
        '''
        super(OptimizedWorld,self).reset()
        self.alive.clear()
        self.alive.update(set([c for c in self if c.alive]))

    def addPattern(self,pattern,**kwds):
        '''
        :param: pattern - string 
        :param: x - optional integer
        :param: y - optional integer
        :param: rule - optional function with signature 'f(x) returns boolean'
        :param: eol - optional character that marks the end of a line in the string
        :param: resize - optional boolean, resizes world to pattern
        :return: None

        This method uses the pattern string to affect the alive/dead
        state of cells in the world.  The x and y paramters can be used
        to place the pattern at an arbitrary position in the world.

        The first character in the string corresponds to coordinate (0,0).

        Updates the set of live cells.
        '''
        
        visited = super(OptimizedWorld,self).addPattern(pattern,**kwds)
        
        self.alive.update(set([c for c in visited if c.alive]))
    
    def step(self):
        '''
        :return: set of cells currently alive

        This method advances the simulation one generation.

        It is optimized to only update cells which are alive and
        their immediate neighbors which results in significant gains
        in preformance compared to the super class' step method. 

        Set operations are used to ensure that alive and neighbor
        cells are only visited once during each phase; neighbor
        count and state update.
        '''
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
    '''
    '''
    def __init__(self,width=80,height=23):
        '''
        '''
        self.generation = 0
        self.width = int(width)
        self.height = int(height)
        self.markers = [' ','.']

    def __str__(self):
        '''
        '''
        s = []
        for y in range(self.height):
            r = ''
            for x in range(self.width):
                r += self.markers[self.cells[y,x] > 0]
            s.append(r)
        return '\n'.join(s)

    def __repr__(self):
        '''
        '''
        s = [ '{self.__class__.__name__}',
              '(width={self.width},',
              'height={self.height})']
        
        return ''.join(s).format(self=self)

    @property
    def cells(self):
        '''
        '''
        try:
            return self._cells
        except AttributeError:
            pass
        self._cells = np.zeros((self.height,self.width),dtype=np.int)
        return self._cells

    @property
    def state(self):
        '''
        Intermediate buffer to hold cell state information.
        '''
        try:
            return self._state
        except AttributeError:
            pass
        self._state = np.zeros((self.height,self.width),dtype=np.int)
        return self._state

    @property
    def alive(self):
        '''
        Returns a list of (x,y) coordinates of cells that are alive.
        '''
        yxs = self.cells.nonzero()
        return [(x,y) for x,y in zip(yxs[1],yxs[0])]

    def _warp(self,key):
        '''
        '''
        x,y = key
        h,w = self.cells.shape
        return (x % (w-1),y % (h-1))

    def __getitem__(self,key):
        '''
        '''
        x,y = self._warp(key)
        return self.cells[y,x]

    def __setitem__(self,key,value):
        '''
        '''
        x,y = self._warp(key)
        self.cells[y,x] = value

    def __iter__(self):
        '''
        '''
        self._x = 0
        self._y = 0
        return self

    def next(self):
        '''
        '''
        v = self[self._x,self._y]
        x,y = self._x,self._y
        self._x += 1
        if self._x not in range(self.width):
            self._x = 0
            self._y += 1
        if self._y not in range(self.height):
            raise StopIteration()
        
        return x,y,v

    def read(self,fileobj):
        '''
        '''
        pass

    def write(self,fileobj):
        '''
        '''
        pass

    def addPattern(self,pattern,x=0,y=0,rule=None,eol='\n',resize=False):
        '''
        '''
        try:
            pattern = BuiltinPatterns[pattern]
        except KeyError:
            pass

        if rule is None:
            rule = lambda c: not c.isspace()

        if resize:
            self.height = len(pattern.split(eol))
            self.width  = max([len(l) for l in pattern.split(eol)])
            self.reset()
        
        visited = set()
        for Y,line in enumerate(pattern.split(eol)):
            for X,c in enumerate(line):
                self[x+X,y+Y] = int(rule(c))
                visited.add((x+X,y+Y))
        return visited
    
    def reset(self):
        '''
        '''
        self.generation = 0
        self.cells.fill(0)

    def neighbors(self,x,y):
        '''
        '''
        yield (x-1,y-1)
        yield (  x,y-1)
        yield (x+1,y-1)
        yield (x-1,  y)
        yield (  x,  y)
        yield (x+1,  y)
        yield (x-1,y+1)
        yield (  x,y+1)
        yield (x+1,y+1)
        

    def calculateStateFor(self,x,y,born=None,live=None):
        '''
        '''
        if born is None:
            born = [3]

        if live is None:
            live = [2,3]

        # build a 3x3 array of neighbor values for cell at x,y

        neighbors = np.array([self[key] for key in self.neighbors(x,y)]) > 0
        neighbors.shape = (3,3)
        neighbors[1,1] = 0      # target cell doesn't contribute to state

        # sum the state of the neighbors
        v = neighbors.sum()

        state = 0               # start off assuming dead

        if (self[x,y] == 0) and (v in born):
            state = 1
                
        if (self[x,y] > 0) and (v in live): 
            state = self[x,y]+1

        self.state[y,x] = state

    def updateState(self):
        '''
        '''
        
        self.state.fill(0)
        for x,y in self.candidates:
            self.calculateStateFor(x,y)

    def updateCells(self):
        '''
        '''

        alive = self.state.nonzero()

        self.cells.fill(0)

        self.cells[alive] = self.state[alive]

    @property
    def candidates(self):
        '''
        Generator method that returns the x,y coordinates of all "cells"
        in the world.
        '''
        for y in range(self.height):
            for x in range(self.width):
                yield (x,y)

    def step(self):
        '''
        '''
        self.updateState()
        self.updateCells()
        self.generation +=1 

    def _go(self,steps=-1):
        try:
            while self.generation != steps:
                print(self)
                self.step()
        except KeyboardInterrupt:
            pass

class OptimizedNumpyWorld(NumpyWorld):

    @property
    def candidates(self):
        n = set()
        for x,y in self.alive:
            for key in self.neighbors(x,y):
                n.add(self._warp(key))
        return n

        
