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

## Examples

I've provided two examples in the contrib directory of the
repo: **CGameOfLife** and **PGameOfLife**. The **C** stands for
curses and will show a simulation in a terminal window using
the time-honored curses library. The **P** in PGameOfLife stands
for [**PyGame**][4] and draws the simulation in a pygame window.

### CGameOfLife Demo

![CGameOfLife Demo][2]

### PGameOfLife Demo

![PGameOfLife Demo][3]

### [CP]GameOfLife Usage
```
$ [CP]GameOfLife.py [pattern_name[,X,Y]] ...
...
$ [CP]GameOfLife.py foo
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
$ [CP]GameOfLife.py glider,10,10 pulsar,0,0 lws,0,20
...	
```

## Design Notes - The Fun Stuff

There are lots of ways of representing a Game of Life board but I
decided to write it as a two dimensional grid of cell objects. The
grid would organize the cells and the cells would implement the
rules that would determine their state: alive or dead. The grid
is called the ```World``` and the cells are called... ```Cell```.

An obvious drawback of this design is that it is memory inefficient:
each display element is represented by a Cell object. Assuming a two
color display, you would only need one bit per display element to
model the state of each state. A Cell object is much larger than
that. That said, my goal was to practice writing good objects 
and then experiencing how this solution would evolve.

The first technical problem, of course, is that python doesn't have a
native two dimensional grid object. I picked a list object as my
foundational grid object and overrode the ```__getitem__``` method to
implement accessing elements using x and y coordinates.

This also made it easier to implement an "infinite" grid by wrapping
the edges when accessed by (x,y) and still allowed iterating through
all the cells serially.

Now that we can access ```Cell```s, it's time to decide what the
```Cell``` should do. Each cell tracks it's current state: alive or
dead and has to know what rules it should be following. In order to to
compute it's next state, it requires the number of living cells in
it's immediate environ.  Consider a cell embedded in a rectangular
matrix; this cell has eight neigbors in the 3x3 sub-matrix where the
target cell has coordinates (1,1). 

Technically, cells don't really need to know where they are in the
world, they only care about the current state of their
neighbors. However the cells cannot directly access neighboring cells,
as that would violate division of labor between the cell and grid data
structures. I also didn't want the ```Cell``` to have some weird back
reference to the ```World``` object. 

Because the cells know their own address, they can compute the
addresses of their neighbors. This simplifies the ```World.step```
method since it doesn't need to compute each cell's neighbors as it
iterates through all the cells. One step further would be to keep
a list of the actual neighbor cells. The ```World.step``` method
would become even more simple since it would not have to provide
any information to a cell other than it's time to compute the next
state.

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

#### Neigbors

As far as simple but useful optimizations, caching each cell's
neighbor coordinates traded space for time when calculating the status
of each cell's neighbors in the ```step``` method. This simplifies the
method since it isn't necessary to pretend the list is a two dimension
object; just iterate through all the cells and ask each cell who
it's neighbors are. A better optimization might be to calculate the 1D
index rather than the 2D, but I think this brings too much knowledge
of the ```World```'s implementation into the cell.

#### Hash Cache FTW

In order for a python object to participate in a set container, it
needs to implement a ```__hash__``` method which should return a
unique hash value for the object. One lesson I learned: cache the hash
value of an object. It is much more efficient that computing the hash
value everytime the method is called. I suppose this is not a valid
optimization for object's whose hash value can mutate over time,
however ```Cell```s do not migrate around the ```World``` and the
uniqueness of the hash is driven by the location of the cell.

#### Dead Cells Don't Matter

The best optimization came when I realized that the ```World``` is
only affected by living cells and I could achieve a more efficient
```step``` method if I only visited living cells and their immediate
surroundings. It is not a perfect solution as a ```World``` could have
nearly all cells living and thus the number of alive cells would tend
to the number of total cells. However, that case is generally rare and
the number of live cells is usually much less than the total number of
cells in the world. [Cite needed :]

#### OptimizedWorld

I added a new class, ```OptimizedWorld```, and overrode only a couple
of methods on ```World```: ```reset```, ```addPattern```, and
```step```. I then imbued the class with a new property, a set named
```alive``` which is initialized with all the live cells in the
```addPattern``` method.

The magic happens in the ```step``` method:

1. Build a set of all the neighbors of all the live cells in the world.
2. Update each cell with the number of live neighbors it has.
2. Apply the live neighbor count to the cell to drive a state change.
3. Finally, pull out any dead cells from the live set.
4. Rinse and repeat.

This optimization resulted in some very impressive gains in speed;
from roughly 10 generations a second to around 100 generations a second
measured in the curses CGameOfLife implementation (on a Mid 2014 Mac Book
Pro with a 2.8Ghz i7, 16G of memory and NVIDIA graphics).

The algorithm is O((alive+neighbors)*2) where normally alive << total
number of cells and neighbors is bounded by [0,alive*8]. I think, my
algorithm analysis is admittedly rusty. 

[1]: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
[2]: https://github.com/JnyJny/GameOfLife/blob/master/Screenshots/CGameOfLife-Demo.gif
[3]: https://github.com/JnyJny/GameOfLife/blob/master/Screenshots/PGameOfLife-Demo.gif
[4]: http://pygame.org
