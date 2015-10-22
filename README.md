# GameOfLife
Conway's Game of Life - Cellular Automata in Python

This is one of those things that everybody writes once to just
see how it's done. Wikipedia was very helpful for getting
the [basics of the game][1] down.

My first design impulse was to have a group of cell objects that 
are organized by a 'world' object. This presented a few challenges:

1. cells need to know about the condition of their immediate neighbors
1. the world needs to visit all cells twice or keep a frame-buffer

I also wanted to have a simple display method so I could concentrate
on the implementation. So I made the world as big as my terminal
window and just printed the world on each generation.

Python doesn't have native two dimension data structures, so I
adapted the __getitem__ accessor (which implements subscripting on
container type object) to take a tuple of X and Y values and emulate
a two dimensional array on top of a one dimesional native list.

This made it easier to implement an infinite world by wrapping the
edges when accessed by (x,y) and still allowed iterating through
all the cells serially.

After I wrote it and started thinking about optimizations, I began
to think about replacing the Cell model with a numpy array to take
advantage of presumably optimized array accessors.  Or even just an
array of characters and letting the charcter value encode the cell
state in a more concise manner.

But I ran out of give a.. dang.

I've provided a few simple patterns to prove that the simulation
is working.

```python
from GameOfLife import *
w = World()
w.add(Pattern['glider'])
w.go(interavl=0.1)
```


[1]: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

