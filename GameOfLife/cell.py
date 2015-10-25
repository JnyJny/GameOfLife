import hashlib

class Cell(object):
    '''
    '''

    born_rule = [3]
    die_rule = [0,1,4,5,6,7,8]
    
    def __init__(self,x,y,alive=False,markers=' .'):
        '''
        :param: x       - integer
        :param: y       - integer
        :param: alive   - boolean
        :param: markers - string
        '''
        if len(markers) < 2:
            raise ValueError("markers needs at least two characters")
        
        self.location = (x,y)
        self.markers = markers
        self.reset(alive)

    def __str__(self):
        '''
        A character indicator of the cell's state.
        '''
        return self.markers[int(self.alive)]

    def __repr__(self):
        '''
        '''
        s = [ '{self.__class__.__name__}',
              '(x={self.location[0]!r},',
              'y={self.location[1]!r},',
              'alive={self.alive!r},',
              'markers={self.markers!r})' ]

        return ''.join(s).format(self=self)

    def __hash__(self):
        '''
        Returns an integer hash that is invariant for the lifetime of the object.
        '''
        try:
            return self._hash
        except AttributeError:
            pass
        self._hash = int(hashlib.sha1(bytes(repr(self),'utf-8')).hexdigest(),16)
        return self._hash

    @property
    def alive(self):
        try:
            return self._alive
        except AttributeError:
            pass
        self._alive = False
        return self._alive
    
    @alive.setter
    def alive(self,newValue):
        self._alive = bool(newValue)
        if not self._alive:
            self.age = 0
            

    @property
    def neighbors(self):
        '''
        A list of this cell's neighbors coordinates, relative to this cell.
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

    def reset(self,alive=False):
        '''
        :param: alive - optional boolean
        Reset this cell to it's default state:
        - Zeros the alive neighbors count.
        - Updates the cells living status (default is False).
        - Age is set to zero.
        '''
        self.aliveNeighbors = 0
        self.alive = alive


    def update(self,aliveNeighbors):
        '''
        :param: aliveNeighbors - integer
        :return: None

        Updates the cell's live neighbor count and increments
        the cells age if it is currently alive.
        '''
        self.aliveNeighbors = aliveNeighbors
        if self.alive:
            self.age += 1
            
    def commit(self):
        '''
        :return: None

        This method causes the cell to determine it's new state based
        on how the number of alive neighbors. 

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
        Return self.alive + other.alive
        '''
        try:
            return self.alive + other.alive
        except AttributeError:
             self.__radd__(other)

    def __radd__(self,other):
        '''
        Return value + self.alive
        '''
        return self.alive + other
