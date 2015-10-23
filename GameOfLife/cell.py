'''Cell for Conway's Game of Life
'''

import hashlib

class Cell(object):
    born_rule = [3]
    die_rule = [0,1,4,5,6,7,8]
    
    def __init__(self,x,y,alive=False,markers=' .'):
        self.location = (x,y)
        self.alive = alive
        self.markers = markers
        self.reset()

    def __str__(self):
        return self.markers[int(self.alive)]

    def __repr__(self):
        msg = '{klass}(location={location},markers="{markers}")'
        return msg.format(klass = self.__class__.__name__,
                          location = self.location,
                          markers = self.markers)

    def __hash__(self):
        '''
        '''
        try:
            return self._hash
        except AttributeError:
            pass
        self._hash = int(hashlib.sha1(bytes(repr(self),'utf-8')).hexdigest(),16)
        return self._hash

    @property
    def neighbors(self):
        '''
        '''
        try:
            return self._neighbors
        except AttributeError:
            pass
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
        if not self.alive and self.aliveNeighbors in self.born_rule:
            self.alive = True
            return
        
        if self.alive and self.aliveNeighbors in self.die_rule:
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
