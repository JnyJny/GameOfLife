*GameOfLife*

Conway's Game of Life - Cellular Automata in Python

This is a python3 package that provides two classes
that together implement Conway's Game of Life.

``
>>> from GameOfLife import *
>>> w = World()
>>> w.addPattern('glider')
>>> while True:
>>>     w.step()
>>>     print(w)
``

*Install*

You can use pip to install ```GameOfLife``` (soon):

``
$ sudo pip3 install GameOfLife
``

You can clone this repository:

``
$ git clone http://github.com/JnyJny/GameOfLife.git
$ cd GameOfLife
$ python3 setup.py install
``

I've provided ```contrib/CGameOfLife```, a python script that
displays the simulation in a terminal window using curses.
Old skool.

``
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
``
