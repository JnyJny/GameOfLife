#!/usr/bin/env python3 

'''Conway's Game of Life displayed with PyGame
'''

import os
import sys
import time
import math

import pygame
from pygame.gfxdraw import pixel
from pygame.locals import *

from GameOfLife import World, Cell, Patterns

_SurfaceDepth = 32


class ColorCell(Cell):
    '''
    '''
    
    @property
    def color(self):
        '''
        Cell foreground color.
        '''

        if not self.alive:
            return (0,0,0)
        
        if self.age == 1:
            return (255,255,255)

        frequency = 0.01
        width = 127
        center = 128

        c = []
        for phase in range(0,6,2):
            c.append((math.sin((frequency * self.age) + phase) * width) + center)

        return tuple(c)


class SpriteCell(ColorCell):
    '''
    '''
    
    def __init__(self,*args,**kwds):
        '''
        '''
        super(SpriteCell,self).__init__(*args,**kwds)
        try:
            self.size = kwds['size']
        except KeyError:
            pass

    @property
    def size(self):
        '''
        '''
        try:
            return self._size
        except AttributeError:
            pass
        self._size = (10,10)
        return self._size

    @size.setter
    def size(self,newValue):
        self._size = newValue
        del(self._surface)
        del(self._rect)

    @property
    def rect(self):
        '''
        '''
        try:
            return self._rect
        except AttributeError:
            pass
        self._rect = pygame.rect.Rect(self.location,self.size)
        return self._rect

    @property
    def surface(self):
        '''
        '''
        try:
            return self._surface
        except AttributeError:
            pass
        self._surface = pygame.surface.Surface(self.size,depth=_SurfaceDepth)
        return self._surface


class CircleCell(SpriteCell):
    '''
    '''
    def draw(self,fillColor,surface=None):
        '''

        '''

        if surface is None:
            surface = self.surface
        
        
        # draw to self.surface and then blit to surface

        if fillColor is not None:
            surface.fill(fillColor)

        x,y = self.rect.width // 2, self.rect.height//2
        r = (min(self.rect.size) // 2) - 2

        pygame.gfxdraw.filled_circle(surface,x,y,r,self.color)
        
        return surface

class SquareCell(SpriteCell):
    '''
    '''
    def draw(self,fillColor,surface=None):

        if surface is None:
            surface = self.surface

        if self.alive:
            surface.fill(self.color)
            pygame.draw.rect(surface,fillColor,self.surface.get_rect(),1)
        else:
            surface.fill(fillColor)
                         
        return surface
    
class PygameWorld(World):
    '''
    '''
    def __init__(self,width,height,cellClass=CircleCell):
        '''
        '''
        super(PygameWorld,self).__init__(width,height,cellClass)
        
        pygame.display.set_caption('PGameOfLife - {}'.format(cellClass.__name__))

        self.hudHeight = 100
        self.paused = False
        self.events = {QUIT:self.quit}
        self.controls = {K_ESCAPE:self.quit,
                         K_q:self.quit,
                         K_SPACE: self.togglePaused,
                         K_PAGEUP: self.incInterval,
                         K_PAGEDOWN: self.decInterval}

        

    @property
    def screen(self):
        '''
        '''
        try:
            return self._screen
        except AttributeError:
            pass

        offx,offy = self[0].size
        screensz = (self.width*offx,self.height*offy + self.hudHeight)
        self._screen = pygame.display.set_mode(screensz,0,_SurfaceDepth)
        self._screen.fill(self.background)
        return self._screen

    @property
    def buffer(self):
        '''
        '''
        try:
            return self._buffer
        except AttributeError:
            pass
        self._buffer = self.screen.copy()
        self._buffer.fill(self.background)
        return self._buffer

    @property
    def background(self):
        '''
        '''
        try:
            return self._background
        except AttributeError:
            pass
        self._background = self.cellClass(0,0,alive=False).color
        return self._background

    @property
    def font(self):
        try:
            return self._font
        except AttributeError:
            pass
        self._font = pygame.font.Font(pygame.font.get_default_font(),24)
        return self._font

    @property
    def hudRect(self):
        try:
            return self._hudRect
        except AttributeError:
            pass
        self._hudRect = self.screen.get_rect()
        self._hudRect.y = self.hudRect.height - self.hudHeight
        self._hudRect.height = self.hudHeight
        return self._hudRect


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
            self._interval = 0.0

    def incInterval(self):
        '''
        '''
        self.interval += 0.01

    def decInterval(self):
        '''
        '''
        self.interval -= 0.01

    def togglePaused(self):
        self.paused = not self.paused

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

        s = ['Generations: {self.generation:<10}',
             '{self.gps:>4} G/s',
             'Census: {nAlive}/{nTotal}']

        self._status = ' '.join(s)
        return self._status.format(self=self,
                                   nAlive=len(self.alive),
                                   nTotal=len(self.cells))

    def reset(self):
        '''
        '''
        super(PygameWorld,self).reset()
        for cell in self:
            cell.rect.x *= cell.size[0]
            cell.rect.y *= cell.size[1]

    def quit(self):
        '''
        '''
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

    def drawHud(self,surface,color,frame):
        '''
        '''
        labels = [ 'Generations:','Generations/Sec:',
                   '# Cells Alive:','# Total Cells:']

        values = ['{self.generation}'.format(self=self),
                  '{self.gps}'.format(self=self),
                  '{nAlive}'.format(nAlive=len(self.alive)),
                  '{nCells}'.format(nCells=len(self.cells))]
        
        for n,texts in enumerate(zip(labels,values)):
            label,value = texts
            l = self.font.render(label,True,color)
            r = l.get_rect()
            r.y = frame.y + (n * r.height)
            surface.blit(l,r)
            
            v = self.font.render(value,True,color)
            r = v.get_rect()
            r.y = frame.y + (n*r.height)
            r.x = 250
            surface.blit(v,r)

    def draw(self,allCells=False):
        '''
        '''
        self.buffer.fill(self.background)
        
        for cell in self.alive:
            self.buffer.blit(cell.draw(self.background),cell.rect)
                             
        
        self.drawHud(self.buffer,(255,255,255),self.hudRect)
                      
        return self.screen.blit(self.buffer,(0,0))

    def run(self,stop=-1,interval=0.01):
        '''
        '''

        self.interval = interval

        while self.generation != stop:
            self.handle_input()
            
            t0 = time.time()
            
            if not self.paused:
                self.step()
                
            rect = self.draw(allCells=self.generation==0)

            t1 = time.time()

            if self.paused:
                self.gps = 0
            else:
                self.gps = 1 / (t1-t0)
                
            pygame.display.update(rect)
            
            if self.writeGenerations:
                pygame.image.save(self.screen,
                                  'images/generation-{:05d}.bmp'.format(self.generation))
            time.sleep(self.interval)


def usage(argv,msg=None,exit_value=-1):
    '''
    '''
    usagefmt = 'usage: {name} [[pattern_name],[X,Y]] ...'
    namefmt = '\t{}'
    print(usagefmt.format(name=os.path.basename(argv[0])))
    if msg:
        print(msg)
    print('pattern names:')
    [print(namefmt.format(name)) for name in Patterns.keys()]
    exit(exit_value)
    

if __name__ == '__main__':

    pygame.init()    

    if len(sys.argv) == 1:
        usage(sys.argv,"no patterns specified.")

    w = PygameWorld(128,128,cellClass=SquareCell)

    w.writeGenerations = False

    for thing in sys.argv[1:]:
        name,_,where = thing.partition(',')
        try:
            x,y = map(int,where.split(','))
        except:
            x,y = 0,0
        w.addPattern(name,x=x,y=y)

    w.run()
    
    
    


