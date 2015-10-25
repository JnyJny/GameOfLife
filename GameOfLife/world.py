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
    
    @classmethod
    def fromString(cls,worldString,CellClass=None,rule=None,eol='\n'):
        '''
        XXX missing doc string
        '''
        w = cls(CellClass,0,0,)
        w.add(worldString,0,0,rule=rule,eol=eol,resize=True)

    @classmethod
    def fromFile(cls,fileobj,CellClass=None,rule=None,eol='\n'):
        '''
        XXX missing doc string
        '''
        w = cls(CellClass,0,0)
        w.read(fileobj,rule=rule,eol=eol)
    
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
            s = fileobj.read()
        except AttributeError:
            f = open(fileobj,'r')
            s = f.read()
        self.add(s,0,0,rule=rule,eol=eol,resize=True)

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

            
    def add(self,pattern,x=0,y=0,rule=None,eol='\n',resize=False):
        '''
        :param: pattern - string 
        :param: x - integer
        :param: y - integer
        :param: rule - function with signature 'f(x) returns boolean'
        :param: eol - character that marks the end of a line in the string
        :param: resize - boolean, resizes world to pattern

        :return: set of visited cells

        This method uses the pattern string to affect the alive/dead
        state of cells in the world.  The x and y paramters can be used
        to place the pattern at an arbitrary position in the world.

        The first character in the string corresponds to coordinate (0,0).

        The rule parameter can be used to specify the rule for determining
        how to interpret each item in the string in terms of alive or dead.

        '''

        if resize:
            self.height = len(pattern.split(eol))
            self.width  = max([len(l) for l in pattern.split(eol)])
            self.reset()

        if rule is None:
            rule = lambda x: not x.isspace()
        
        visited = set()
        for Y,line in enumerate(pattern.split(eol)):
            for X,c in enumerate(line):
                self[x+X,y+Y].alive = rule(c)
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
        
        visited = super(OptimizedWorld,self).add(pattern,x,y)
        
        self.alive.update(set([c for c in visited if c.alive]))
    
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
        
        for c in self.alive:
            neighbors = self.neighborsFor(c)
            borders.update(set(neighbors))

        self.alive.update(borders)

        for c in self.alive:
            c.update(sum(self.neighborsFor(c)))
            
        deaders = set()
        for c in self.alive:
            c.commit()
            if not c.alive:
                deaders.add(c)
                
        return self.alive.difference_update(deaders)
