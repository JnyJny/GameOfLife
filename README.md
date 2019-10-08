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
$ pip install GameOfLife
```


## Command-line Interface

```
$ gameoflife --help

```

## Development

To hack on this, you can clone this repository and install it with
[poetry][5]:
```
$ git clone https://github.com/JnyJny/GameOfLife.git
$ cd GameOfLife
$ poetry install --develop gameoflife
```



[1]: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
[2]: https://github.com/JnyJny/GameOfLife/blob/master/Screenshots/CGameOfLife-Demo.gif
[3]: https://github.com/JnyJny/GameOfLife/blob/master/Screenshots/PGameOfLife-Demo.gif
[4]: http://pygame.org
[5]: https://poetry.eustace.io
[6]: https://github.com/peterbrittain/asciimatics

