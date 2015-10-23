'''Conway's Game of Life
'''

from . import Cell

class World(object):
    '''
    The game world is a two dimensional grid, each coordinate is the
    address of a Cell.

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
        msg = '{klass}(CellClass={cellKlass},width={w},height={h})'
        return msg.format(klass = self.__class__.__name__,
                          cellKlass = self.cellClass.__name__,
                          w = self.width,
                          h = self.height)

    def _clamp(self,key):
        '''
        '''
        
        x,y = key
        
        if x < 0:
            x = self.width + x
        if x >= self.width:
            x -= self.width
            
        if y < 0:
            y = self.height + y
        if y >= self.height:
            y -= self.height
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
        Resets the simulation to base state. 
        '''
        self.generation = 0
        self.cells.clear()
        for y in range(self.height):
            row = []
            for x in range(self.width):
                self.cells.append(self.cellClass(x,y))

    def neighborsFor(self,cell):
        '''
        :param: cell - Cell subclass in 
        Assuming a 
        '''
        return [self[key] for key in cell.neighbors]

    def step(self):
        '''
        
        '''
        self.generation += 1

        for c in self:
            c.update(sum(self.neighborsFor(c)))

        for c in self:
            c.commit(self.generation)
        
    def add(self,pattern,x=0,y=0):
        '''
        '''
        for Y,line in enumerate(pattern.split('\n')):
            for X,c in enumerate(line):
                self[x+X,y+Y].alive = not c.isspace()
        

class WorldOpt(World):

    def reset(self):
        super(WorldOpt,self).reset()
        self.live = set(self.alive)

    def add(self,pattern,x=0,y=0):
        super(WorldOpt,self).add(pattern,x,y)
        self.live = set(self.alive)
    
    def step(self):
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
            c.commit(self.generation)
            if not c.alive:
                deaders.add(c)
                
        return self.live.difference_update(deaders)
