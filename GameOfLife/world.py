from . import Cell

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
    
    def __init__(self,CellClass=None,width=80,height=23):
        '''
        :param: CellClass - subclass of Cell
        :param: width - integer
        :param: height - integer

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

    def _clamp(self,key):
        '''
        :param: key - tuple of x,y integer values

        Implements wrapping of x,y coordinates to form an infinite grid.

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
            x,y = self._clamp(key)
            return self.cells[(y * self.width)+x]
        except TypeError:
            pass
        
        return self.cells[key]

    @property
    def alive(self):
        '''
        Returns a list of Cells that are currently alive.
        '''
        return [c for c in self if c.alive]

    @property
    def dead(self):
        '''
        Returns a list of Cells that are currently not alive.
        '''
        return [c for c in self if not c.alive]
            
    def reset(self):
        '''
        Resets the simulation to base state:
        - sets generation to zero
        - deletes all cells and allocates a new set cells
        '''
        self.generation = 0
        self.cells.clear()
        for y in range(self.height):
            row = []
            for x in range(self.width):
                self.cells.append(self.cellClass(x,y))

    def neighborsFor(self,cell):
        '''
        :param: cell - Cell subclass 

        Returns a list of all cells that are immediate neighbors
        of the target cell.
        '''
        return [self[key] for key in cell.neighbors]

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
            c.update(sum(self.neighborsFor(c)))

        for c in self:
            c.commit()

            
    def add(self,pattern,x=0,y=0):
        '''
        :param: pattern - string
        :param: x - integer
        :param: y - integer
        :return: None

        This method uses the pattern string to affect the alive/dead
        state of cells in the world.  The x and y paramters can be used
        to place the pattern at an arbitrary position in the world.

        The first character in the string corresponds to coordinate (0,0).
        '''
        for Y,line in enumerate(pattern.split('\n')):
            for X,c in enumerate(line):
                self[x+X,y+Y].alive = not c.isspace()


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
    def reset(self):
        '''
        Resets the simulation to base state:
        - sets generation to zero
        - deletes all cells and allocates a new set cells
        - creates an empty list of live cells
        '''
        super(OptimizedWorld,self).reset()
        self.live = set(self.alive)

    def add(self,pattern,x=0,y=0):
        '''
        :param: pattern - string
        :param: x - integer
        :param: y - integer
        :return: None

        This method uses the pattern string to affect the alive/dead
        state of cells in the world.  The x and y paramters can be used
        to place the pattern at an arbitrary position in the world.

        The first character in the string corresponds to coordinate (0,0).

        Updates the set of live cells.
        '''
        super(OptimizedWorld,self).add(pattern,x,y)
        self.live = set(self.alive)
    
    def step(self):
        '''
        :return: current set of live cells

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
        
        for c in self.live:
            neighbors = self.neighborsFor(c)
            borders.update(set(neighbors))

        self.live.update(borders)

        for c in self.live:
            c.update(sum(self.neighborsFor(c)))
            
        deaders = set()
        for c in self.live:
            c.commit()
            if not c.alive:
                deaders.add(c)
                
        return self.live.difference_update(deaders)
