#!/usr/bin/env python3

# Conway's Game of Life

import hashlib
import time
import colorama

class Cell(object):
    colors = [ colorama.ansi.Fore.WHITE,
               colorama.ansi.Fore.YELLOW,
               colorama.ansi.Fore.GREEN,
               colorama.ansi.Fore.MAGENTA,
               colorama.ansi.Fore.CYAN,
               colorama.ansi.Fore.RED,
               colorama.ansi.Fore.BLUE ]
    born = [3]
    die = [0,1,4,5,6,7,8]

    def __init__(self,x,y,alive=False,markers=' .'):
        self.location = (x,y)
        self.alive = alive
        self.markers = markers
        self.reset()

    def __str__(self):
        m = self.markers[int(self.alive)]

        if self.alive:
            try:
                c = self.colors[self.age // 10]
            except:
                c = self.colors[-1]
        else:
            c = self.colors[0]
            
        return c + m + colorama.ansi.Fore.RESET

    def __repr__(self):
        msg = '{klass}(location={location},markers="{markers}")'
        return msg.format(klass = self.__class__.__name__,
                          location = self.location,
                          markers = self.markers)

    def __hash__(self):
        '''
        '''
        return int(hashlib.sha1(bytes(self.repr,'utf-8')).hexdigest(),16)

    @property
    def neighbors(self):
        '''
        '''
        try:
            return self._neighbors
        except AttributeError:
            pass
        # (x-1,y-1), (  x,y-1), (x+1,y-1)
        # (x-1,  y), (  x,  y), (x+1,  y)
        # (x-1,y+1), (  x,y+1), (x+1,y+1)
        x,y = self.location
        self._neighbors = [(x-1,y-1), (  x,y-1), (x+1,y-1),
                           (x-1,  y),            (x+1,  y),
                           (x-1,y+1), (  x,y+1), (x+1,y+1)]
        return self._neighbors

    def reset(self):
        '''
        '''
        self.aliveNeighbors = 0
        self.alive = False
        self.age = 0

    def update(self,aliveNeighbors):
        '''
        '''
        self.aliveNeighbors = aliveNeighbors
        if self.alive:
            self.age += 1
            
    def commit(self,generation):
        '''
        '''
        if not self.alive and self.aliveNeighbors in self.born:
            self.alive = True
            return
        
        if self.alive and self.aliveNeighbors in self.die:
            self.alive = False
            self.age = 0
            return

    def __add__(self,other):
        '''
        x + y
        '''
        try:
            return self.alive + other.alive
        except AttributeError:
             self.__radd__(other)

    def __radd__(self,other):
        '''
        x + y
        '''
        return self.alive + other


class World(list):
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
    
    def __init__(self,CellClass=None,width=80,height=65):
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
            x,y = key
            
            if x < 0:
                x = self.width + x
            if x >= self.width:
                x -= self.width
                
            if y < 0:
                y = self.height + y
            if y >= self.height:
                y -= self.height
                
            return self[(y * self.width)+x]
        except TypeError:
            pass
        
        return super(GameOfLife,self).__getitem__(key)

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
        self.clear()
        for y in range(self.height):
            row = []
            for x in range(self.width):
                self.append(self.cellClass(x,y))

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
            
        
    def go(self,stop=-1,interval=0.1):
        '''
        '''
        try:
            while True:
                if self.generation == stop:
                    break
                self.step()
                print(self)
                time.sleep(interval)
        except KeyboardInterrupt:
            pass

    def add(self,pattern,x=0,y=0):
        '''
        '''
        for Y,line in enumerate(pattern.split('\n')):
            for X,c in enumerate(line):
                self[x+X,y+Y].alive = not c.isspace()
        

Patterns = { 'glider':' x \n  x\nxxx',
             'LWS':'x  x\n    x\nx   x\n xxxx',
             
             'block':'xx\nxx',
             'beehive':' xx \nx  x\n xx ',
             'loaf':' xx \nx  x\n x x\n   x',
             'boat':'xx \nx x\n x ',
             
             'blinker': 'xxx',
             'toad': ' xxx\nxxx ',
             'beacon': 'xx  \nxx  \n  xx\n  xx\n',
             'pulsar':'  xxx   xxx\n\nx    x x    x\nx    x x    x\nx    x x    x\n  xxx   xxx\n\n  xxx   xxx\nx    x x    x\nx    x x    x\nx    x x    x\n\n  xxx   xxx'
             }

w = World()
w.add(Patterns['glider'])
w.go(interval=0.1)


    
