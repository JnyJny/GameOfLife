#!/usr/bin/env python3

'''Conway's Game of Life displayed with PyGame
'''

import os
import sys
import time

import pygame
from pygame.gfxdraw import pixel
from pygame.locals import *

from GameOfLife import World, Cell, Patterns

class TwoSixteen(list):
    def __init__(self,*args,**kwds):
        super(TwoSixteen,self).__init__(args,**kwds)
        v = [00,33,66,99,0xcc,0xff]
        for r in v:
            for g in v:
                for b in v:
                    self.append((r,g,b))
        del(self[-1])
        self.insert(1,(255,255,255))

    def __getitem__(self,key):
        key %= len(self)
        return super(TwoSixteen,self).__getitem__(key)


class PygameCell(Cell):
    _colors = TwoSixteen()
    @property
    def color(self):
        return self._colors[self.age]

    def draw(self,surface):
        x,y = self.location
        pygame.gfxdraw.pixel(surface,x,y,self.color)

        
class PygameWorld(World):
    '''
    '''
    def __init__(self,screen,cellClass=PygameCell):
        '''
        '''
        sz = screen.get_size()
        super(PygameWorld,self).__init__(cellClass,width=sz[0],height=sz[1])
        self.screen = screen
        self.buffer = screen.copy() # resize?
        self.events = {QUIT:self.quit}
        self.controls = {K_ESCAPE:self.quit,
                         K_q:self.quit,
                         K_PLUS: self.incInterval,
                         K_MINUS: self.decInterval}
        self.buffer.fill(self.background)


    @property
    def background(self):
        '''
        '''
        try:
            return self._background
        except AttributeError:
            pass
        self._background = TwoSixteen()[0]
        return self._background

    @property
    def interval(self):
        '''
        '''
        try:
            return self._interval
        except AttributError:
            pass
        self._interval = 0.01
        return self._interval

    @interval.setter
    def interval(self,newValue):
        self._interval = float(newValue)
        if self._interval < 0:
            self._interval = 0

    def incInterval(self):
        '''
        '''
        self.interval += 0.01

    def decInterval(self):
        '''
        '''
        self.interval -= 0.01

    @property
    def gps(self):
        '''
        '''
        try:
            return self._gps
        except AttributeError:
            pass
        self._gps = 0
        return self._gps

    @gps.setter
    def gps(self,newValue):
        self._gps = int(newValue)

    @property
    def status(self):
        '''
        '''
        try:
            return self._status.format(self=self,
                                       nAlive=len(self.alive),
                                       nTotal=len(self.cells))
        except AttributeError:
            pass

        s = ['Generations: {self.generation:<}',
             'Cells Alive: {nAlive}',
             'Total Cells: {nTotal}']

        self._status = '\n'.join(s)
        return self._status.format(self=self,
                                   nAlive=len(self.alive),
                                   nTotal=len(self.cells))

    def quit(self):
        '''
        '''
        print(self.status)
        exit()

    def handle_input(self):
        '''
        '''
        # first key presses
        pressed = pygame.key.get_pressed()
        for key,action in self.controls.items():
            if pressed[key]:
                action()
        # next events
        for event in pygame.event.get():
            name = pygame.event.event_name(event.type)
            try:
                self.events[name](event)
            except KeyError:
                pass



    def draw(self):
        '''
        '''
        
        self.buffer.fill(self.background)
        
        for cell in self.alive:
            cell.draw(self.buffer)
              
        rect = self.screen.blit(self.buffer,(0,0))
        
        return rect

    def run(self,stop=-1,interval=0):
        '''
        '''

        self.interval = interval

        while self.generation != stop:
            self.handle_input()
            self.step()
            rect = self.draw()
            pygame.display.update(rect)
            time.sleep(self.interval)


def usage(argv,msg=None,exit_value=-1):
    '''
    '''
    usagefmt = 'usage: {name} [[pattern_name],[X,Y]] ...'
    namefmt = '\t{n}'
    print(usagefmt.format(name=os.path.basename(argv[0])))
    if msg:
        print(msg)
    print('pattern names:')
    [print(namefmt.format(n=name)) for name in Patterns.keys()]
    exit(exit_value)
    

if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode((128,128),0,32)

    if len(sys.argv) == 1:
        usage(sys.argv,"no patterns specified.")

    w = PygameWorld(screen)

    for thing in sys.argv[1:]:
        name,_,where = thing.partition(',')
        try:
            x,y = map(int,where.split(','))
        except:
            x,y = 0,0
        w.addPattern(name,x=x,y=y)

    w.run()
    
    
    


