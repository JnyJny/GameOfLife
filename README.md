# GameOfLife
Conway's Game of Life - Cellular Automata in Python

This is a python3 package that provides two classes
that together implement Conway's Game of Life. 

```
>>> from GameOfLife import *
>>> w = World()
>>> w.addPattern('glider')
>>> while True:
>>>     w.step()
>>>     print(w)
```

## Install

You can use pip to install ```GameOfLife```:

```
$ sudo pip3 install GameOfLife
```

You can clone this repository

```
$ git clone https://github.com/JnyJny/GameOfLife.git
$ cd GameOfLife
$ python3 setup.py install
```

I've provided ```contrib/CGameOfLife```, a python script that
displays the simulation in a terminal window using curses.
Old skool.
!(CGameOfLife Demo)[2]

If you have [pygame][4] installed, ```contrib/PGameOfLife``` is
pretty much the same except drawing to a pygame window.
!(PGameOfLife Demo)[3]

```
$ CGameOfLife.py [pattern_name[,X,Y]] ...
...
$ CGameOfLife.py foo
unknown pattern: 'foo'
known patterns:
	block
	lws
	toad
	pulsar
	loaf
	glider
	blinker
	beehive
	beacon
	boat
$ CGameOfLife.py glider,10,10 pulsar,0,0 lws,0,20
...	
```

## Design

There are lots of ways of representing a Game of Life board but I
decided to write it as a two dimensional grid of cell objects. The
grid would organize the cells and the cells would implement the
rules that would determine their state: alive or dead. The grid
is called the ```World``` and the cells are called... ```Cell```.

The first problem, of course, is that python doesn't have a native two
dimensional grid object. I picked a list object as my foundational
grid object and overrode the ```__getitem__``` method to implement
accessing elements using x and y coordinates.

This also made it easier to implement an infinite grid by wrapping
the edges when accessed by (x,y) and still allowed iterating through
all the cells serially.

The cells don't really need to know where they are in the world, they
only care about the current state of their neighbors. However the cells
cannot directly access neighboring cells, it would violate division of
labor between the cell and grid data structures. I decided since the
cells know their own address, they can know the addresses of their
neighbors. This simplifies the grid somewhat since it doesn't need
to figure out a cell's neighbors as it iterates through all the cells.

At the end of the day, the step function was a O(2*n) method since
each cell was visited in two batches: the first to record the number
of alive neighbors for each cell and the second to change state based
on the number of alive neighbors. Most of the time this is implemented
as a frame buffer type data structure, with one frame indicating the
n-th step and the other frame the n+1-th step. It's a classic space
for time trade off.

### Patterns

I have provided a few simple patterns to prove that the simulation is
working. The ```Patterns``` dictionary is keyed with each pattern's
name and then a string representing cell states: spaces are not-alive
cells, non-spaces are alive cells. A newline in the string indicates a
new row.

### Optimizations

After I wrote it and started thinking about optimizations, I began
to think about replacing the ```Cell``` model with a numpy array to take
advantage of presumably optimized array accessors.  Or even just an
array of characters and letting the character value encode the cell
state in a more compact (and obtuse) manner. Those changes are pretty
disruptive and I decided to postpone them.

As far as simple but useful optimizations, caching each cell's
neighbor coordinates traded space for time when calculating the status
of each cell's neighbors in the step method. This simplifies the step
method since we don't need to pretend the list is a two dimension
object and just iterate through all the cells and ask each cell who
it's neighbors are. A better optimization might be to calculate the 1D
index rather than the 2D, but I think this brings too much knowledge
of the world's implementation into the cell.

The best optimization came when I realized that the world is only
affected by living cells and I could achieve a more efficient step
method if I only visited living cells and their immediate
surroundings. It is not a perfect solution as a grid could have nearly
all cells living and thus the number of alive cells would tend to the
number of total cells. However, that case is pretty rare and the number
of live cells is usually much less than the total number of cells in
the world.

I added a new class, ```OptimizedWorld```, and overrode only a couple
of methods on ```World```: reset, add, and step. I then imbued the
class with a new property, a set named ```alive``` which is
initialized with all the live cells in the ```addPattern``` method. 

The magic happens in the step method:

1. Build a set of all the neighbors of all the live cells in the world
2. Update each cell with the number of live neighbors it has
2. Apply the live neighbor count to the cell to drive a state change
3. Finally, pull out any dead cells from the live set.
4. Rinse and repeat.

In order for a python object to participate in a set container, it
needs to implement a ```__hash__``` method which should return a
unique hash value for the object. One lesson I learned: cache the hash
value of an object. It is much more efficient that computing the hash
value everytime the method is called. I suppose this is not a valid
optimization for object's whose hash value can mutate over time,
however cells do not migrate around the world and the uniqueness of
the hash is driven by the location of the cell.

This optimization resulted in some very impressive gains in speed;
from roughly 10 generations a second to around 100 generations a second.

[1]: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
[2]: https://github.com/JnyJny/GameOfLife/blob/master/Screenshots/CGameOfLife-demo.gif
[3]: https://github.com/JnyJny/GameOfLife/blob/master/Screenshots/PGameOfLife-demo.gif
[4]: http://pygame.org
