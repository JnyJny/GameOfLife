# GameOfLife
Conway's Game of Life - Cellular Automata in Python

![](https://github.com/JnyJny/GameOfLife/blob/master/Screenshots/demo-2.gif)

This is one of those things that everybody writes once to just
see how it's done. Wikipedia was very helpful for getting
the [basics of the game][1] down.

My first design impulse was to have a group of cell objects that 
are organized by a 'world' object. This presented a few challenges:

1. cells need to know about the condition of their immediate neighbors
1. the world needs to visit all cells twice or keep a frame-buffer

I also wanted to have a simple display method so I could concentrate
on the implementation. So I made the world as big as my terminal
window and just printed the world on each generation. I think a --curses--
or pygame interface would also be quick and fun to write.

Curses turned out to be relatively easy to add, so pygame is next.

Python doesn't have a native two dimensional data structure, so I
adapted the __getitem__ accessor (which implements subscripting on
container type object) to take a tuple of X and Y values and emulate
a two dimensional array on top of a one dimesional native list.

This made it easier to implement an infinite world by wrapping the
edges when accessed by (x,y) and still allowed iterating through
all the cells serially.

After I wrote it and started thinking about optimizations, I began
to think about replacing the Cell model with a numpy array to take
advantage of presumably optimized array accessors.  Or even just an
array of characters and letting the character value encode the cell
state in a more compact (and obtuse) manner. Those changes are pretty
disruptive and I decided to post-pone them.

As far as simple but useful optimizations, caching each cell's
neighbor coordinates traded space for time when calculating the status
of each cell's neighbors in the step method. This simplifies the step
method since we don't need to pretend the list is a two dimension
object and just iterate through all the cells and ask each cell who
it's neighbors are. A better optimization might be to calculate the 1D
index rather than the 2D, but I think this brings too much knowledge
of the world's implementation into the cell. 

Some other useful optimizations could include changing the base data
structure from list to dictionary or a set. The idea is to make it
easier to differentiate live cells from dead cells and only work on
live cells and their neighbors. This avoids having to iterate through
all the cells in the world and concentrate only on the live ones which
have the power to affect the state of the world.

I have provided a few simple patterns to prove that the simulation
is working.

```python
from GameOfLife import *
w = World()
w.add(Patterns['glider'])
w.go(interavl=0.1)
```

The Patterns dictionary is keyed with each pattern's name and
then a string representing cell states: spaces are not-alive cells,
non-spaces are alive cells. A newline in the string indicates
a new row.

For instance a glider would look like:

```python
glider = '''
 x 
  x
xxx
''' 
```

Or the compact version I chose for the dictionary:

```python
 Patterns = { 'glider':' x \n  x\nxxxx',
              ...
		    }
```

###Usage

GameOfLife now has curses support and dodgy command-line parsing!

```
$ GameOfLife [pattern_name[,X,Y]] ...
...
$ GameOfLife.py foo
Unknown pattern named ''foo''
Known pattern names:
	block
	LWS
	toad
	pulsar
	loaf
	glider
	blinker
	beehive
	beacon
	boat
```


[1]: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

