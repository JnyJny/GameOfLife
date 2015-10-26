#!/usr/bin/env python3

# Conway's Game of Life

import curses
import time

from GameOfLife import World, Cell, Patterns

from curses import ( COLOR_BLACK, COLOR_BLUE, COLOR_CYAN,
                     COLOR_GREEN, COLOR_MAGENTA, COLOR_RED,
                     COLOR_WHITE, COLOR_YELLOW )
                     

class CursesWorld(World):
    '''
    '''

    colors = [COLOR_WHITE,COLOR_YELLOW,COLOR_MAGENTA,
              COLOR_CYAN,COLOR_RED,COLOR_GREEN,COLOR_BLUE]

    def __init__(self,cellClass=None,window=None):
        h,w = window.getmaxyx()
        super(CursesWorld,self).__init__(cellClass,w,h-1)
        self.w = window
        for n,fg in enumerate(self.colors):
            curses.init_pair(n+1,fg,COLOR_BLACK)

    def colorForCell(self,cell):
        '''
        Returns a curses color_pair for a cell, chosen by the cell's age.
        '''

        n = min(cell.age // 100,len(self.colors)-1)
        
        return curses.color_pair(n+1)

    def handle_input(self):
        '''
        Accepts input from the user and acts on it.
        '''
        c = self.w.getch()
        if c == ord('q') or c == ord('Q'):
            exit()

    def step(self):
        '''
        :return: set of cells current alive

        This method advances the simulation one generation.

        Calculates the number of generations per second (gps)
        by timing how long the current step took to complete
        and taking the inverse. 

        '''
        t0 = time.time()
        ret = super(CursesWorld,self).step()
        t1 = time.time()
        self.gps = int(1/(t1 - t0))
        return ret
            
    @property
    def status(self):
        '''
        Format string for the status line.
        '''
        try:
            return self._status
        except AttributeError:
            pass

        s = ['Q to quit\t',
             'Generation: {self.generation:<10}',
             'GPS: {self.gps:>4}/s',
             'Cells: {a:>5}/{t:<5}']
            
        self._status = ' '.join(s)
        return self._status

    def draw(self):
        '''
        :return: None

        Updates each character at r,c in the curses window with
        the appropriate colored marker for each cell in the world.

        Moves the cursor to bottom-most line, left-most column.
        '''
        for y in range(self.height):
            for x in range(self.width):
                c = self[x,y]
                self.w.addch(y,x,str(c)[0],self.colorForCell(c))
        
        self.w.addstr(self.height,2,
                      self.status.format(self=self,
                                         a=len(self.alive),
                                         t=len(self.cells)))


        self.w.move(self.height,1)
        

    def run(self,stop=-1,interval=0):
        '''
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

        '''
        self.w.clear()
        try:
            while True:
                if self.generation == stop:
                    break
                self.handle_input()
                self.step()
                self.draw()
                
                self.w.refresh()
                
                if interval:
                    curses.napms(interval)
        except KeyboardInterrupt:
            pass
        

def main(stdscr,argv):

    w = CursesWorld(window=stdscr)

    if len(argv) == 1:
        raise ValueError("no patterns specified.")
    
    for thing in argv[1:]:
        x,y = 0,0
        name,_,where = thing.partition(',')
        try:
            if len(where):
                x,y = map(int,where.split(','))
        except:
            pass
        w.addPattern(Patterns[name],x=x,y=y)

    stdscr.nodelay(True)
        
    w.run()


def usage(argv,msg=None,exit_value=-1):
    usagefmt = 'usage: {name} [[pattern_name],[X,Y]] ...'
    namefmt = '\t{n}'
    print(usagefmt.format(name=os.path.basename(argv[0])))
    if msg:
        print(msg)
    print('pattern names:')
    [print(namefmt.format(n=name)) for name in Patterns.keys()]
    exit(exit_value)

if __name__ == '__main__':
    import sys
    import os

    from curses import wrapper
    try:
        wrapper(main,sys.argv)
    except KeyError as e:
        usage(sys.argv,'unknown pattern {p}'.format(p=str(e)))
    except ValueError as e:
        usage(sys.argv,str(e))
        
        
    



    
