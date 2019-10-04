#!/usr/bin/env python3

"""Conway's Game of Life in a Curses Terminal Window
"""

import curses
import time

from GameOfLife import World, Cell, Patterns

from curses import (
    COLOR_BLACK,
    COLOR_BLUE,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_MAGENTA,
    COLOR_RED,
    COLOR_WHITE,
    COLOR_YELLOW,
)


class CursesWorld(World):
    """
    Display a Game of Life in a terminal window using curses.
    """

    colors = [
        COLOR_WHITE,
        COLOR_YELLOW,
        COLOR_MAGENTA,
        COLOR_CYAN,
        COLOR_RED,
        COLOR_GREEN,
        COLOR_BLUE,
    ]

    def __init__(self, window, cell_class=None):
        """
        :param: window    - curses window
        :param: cell_class - optional Cell subclass
        
        """
        h, w = window.getmaxyx()
        super().__init__(w, h - 1, cell_class)
        self.w = window
        self.interval = 0
        for ndx, fg in enumerate(self.colors):
            curses.init_pair(ndx + 1, fg, COLOR_BLACK)

    @property
    def gps(self):
        """
        Generations per second.
        """
        try:
            return self._gps
        except AttributeError:
            pass
        self._gps = 0
        return self._gps

    @gps.setter
    def gps(self, newValue):
        self._gps = int(newValue)

    def color_for_cell(self, cell):
        """
        Returns a curses color_pair for a cell, chosen by the cell's age.
        """

        n = min(cell.age // 100, len(self.colors) - 1)

        return curses.color_pair(n + 1)

    def handle_input(self):
        """
        Accepts input from the user and acts on it.
        
        Key        Action
        -----------------
        q          exit()
        Q          exit()
        +          increase redraw interval by 10 milliseconds
        -          decrease redraw interval by 10 milliseconds

        """
        c = self.w.getch()
        if c == ord("q") or c == ord("Q"):
            exit()
        if c == ord("+"):
            self.interval += 10

        if c == ord("-"):
            self.interval -= 10
            if self.interval < 0:
                self.interval = 0

    @property
    def status(self):
        """
        Format string for the status line.
        """
        try:
            return self._status.format(self=self, a=len(self.alive), t=len(self.cells))
        except AttributeError:
            pass

        s = [
            "Q to quit\t",
            "{self.generation:>10} G",
            "{self.gps:>4} G/s",
            "Census: {a:>5}/{t:<5}",
            "{self.interval:>4} ms +/-",
        ]

        self._status = " ".join(s)
        return self._status.format(self=self, a=len(self.alive), t=len(self.cells))

    def draw(self):
        """
        :return: None

        Updates each character in the curses window with
        the appropriate colored marker for each cell in the world.

        Moves the cursor to bottom-most line, left-most column
        when finished.
        """
        for y in range(self.height):
            for x in range(self.width):
                c = self[x, y]
                self.w.addch(y, x, str(c)[0], self.color_for_cell(c))

        self.w.addstr(self.height, 2, self.status)

        self.w.move(self.height, 1)

    def run(self, stop=-1, interval=0):
        """
        :param: stop     - optional integer
        :param: interval - optional integer
        :return: None

        This method will run the simulation described by world until the
        given number of generations specified by ''stop'' has been met. 
        The default value will cause the simulation to run until interrupted
        by the user. 

        The interval is number of milliseconds to pause between generations.
        The default value of zero allows the simulation to run as fast as
        possible.

        The simulation is displayed via curses in a terminal window and
        displays a status line at the bottom of the window.

        The simulation can be stopped by the user pressing the keys 'q' or
        'Q'. The interval between simulation steps can be increased with
        the plus key '+' or decreased with the minus key '-' by increments
        of 10 milliseconds.

        """
        self.w.clear()
        self.interval = interval
        try:
            while True:
                if self.generation == stop:
                    break
                self.handle_input()
                t0 = time.time()
                self.step()
                self.draw()
                self.w.refresh()
                if self.interval:
                    curses.napms(self.interval)
                t1 = time.time()
                self.gps = 1 / (t1 - t0)
        except KeyboardInterrupt:
            pass


def main(stdscr, argv):

    w = CursesWorld(stdscr)

    if len(argv) == 1:
        raise ValueError("no patterns specified.")

    for thing in argv[1:]:
        name, _, where = thing.partition(",")
        try:
            x, y = map(int, where.split(","))
        except:
            x, y = 0, 0
        w.add_pattern(Patterns[name], x=x, y=y)

    stdscr.nodelay(True)

    w.run()


def usage(argv, msg=None, exit_value=-1):
    usagefmt = "usage: {name} [[pattern_name],[X,Y]] ..."
    namefmt = "\t{n}"
    print(usagefmt.format(name=os.path.basename(argv[0])))
    if msg:
        print(msg)
    print("pattern names:")
    [print(namefmt.format(n=name)) for name in Patterns.keys()]
    exit(exit_value)


if __name__ == "__main__":
    import sys
    import os

    from curses import wrapper

    try:
        wrapper(main, sys.argv)
    except KeyError as e:
        usage(sys.argv, "unknown pattern {p}".format(p=str(e)))
    except ValueError as e:
        usage(sys.argv, str(e))
