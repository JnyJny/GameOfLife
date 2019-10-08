"""
"""

from asciimatics.screen import ManagedScreen, Screen
from time import sleep
from .. import World


class AsciimaticsWorld(World):
    """
    """

    @classmethod
    def start(cls, patterns=None) -> None:
        """
        :param list patterns:
        """
        with ManagedScreen() as screen:
            world = cls(screen)
            for (name, x, y) in patterns:
                world.add_named_pattern(name, x=x, y=y)
            world.run()

    def __init__(self, screen):
        """
        :param asciimatics.screen.Screen screen:
        """
        h, w = screen.dimensions
        super().__init__(w, h - 1)
        self.screen = screen

    @property
    def status(self):
        return f" Q to quit\tGenerations: {self.generation:>10} Census: {len(self.alive):>5}"

    def handle_input(self):
        """
        """
        event = self.screen.get_event()
        if not event:
            return
        try:
            if event.key_code == Screen.KEY_ESCAPE:
                raise StopIteration()
            if chr(event.key_code) in "Qq":
                raise StopIteration()
        except AttributeError:
            pass
        except ValueError:
            pass

    def draw(self):
        """
        """

        for (x, y) in self.alive:
            self.screen.print_at(self.markers[1], x, y, Screen.COLOUR_GREEN)

        self.screen.print_at(self.status, 0, self.height, Screen.COLOUR_WHITE)

    def run(self, stop=-1, interval=50):

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
