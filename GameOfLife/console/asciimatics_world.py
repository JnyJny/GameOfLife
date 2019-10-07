"""
"""

from asciimatics.screen import ManagedScreen, Screen
from time import sleep

from .. import World
from .. import Patterns


class AsciimaticsWorld(World):
    @classmethod
    def start(cls, patterns=None):

        with ManagedScreen() as screen:
            world = cls(screen)
            for (name, x, y) in patterns:
                world.add_named_pattern(name, x=x, y=y)
            world.run()

    def __init__(self, screen):
        w, h = screen.dimensions
        super().__init__(w, h - 1)
        self.screen = screen

    def handle_input(self):

        event = self.screen.get_event()
        if not event:
            return
        try:
            if chr(event.key_code) in "Qq":
                raise StopIteration()
        except AttributeError:
            pass

    def draw(self):

        for (x, y) in self.alive:
            self.screen.print_at("O", x, y, Screen.COLOUR_GREEN)

    def run(self, stop=-1, interval=10):

        while True:
            try:
                self.handle_input()
            except StopIteration:
                break
            self.screen.clear()
            self.draw()
            self.screen.refresh()
            self.step()
            sleep(interval / 1000)
