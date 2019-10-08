"""
"""

import click
import time

from ..version import __version__
from .. import Patterns

_display_types = ["curses", "pygame", "asciimatics"]


@click.command()
@click.option(
    "-p", "--pattern", "patterns", type=(str, int, int), default=None, multiple=True
)
@click.option("--output", type=click.Choice(_display_types), default="curses")
@click.option("-l", "--list-patterns", is_flag=True)
@click.version_option(__version__)
def cli(patterns, output, list_patterns):

    if list_patterns:
        print("Available patterns")
        for name in Patterns.keys():
            print(f" - {name}")
        return

    if output == "curses":
        from .curses_world import CursesWorld as World
    if output == "pygame":
        from .pygame_world import PygameWorld as World
    if output == "asciimatics":
        from .asciimatics_world import AsciimaticsWorld as World

    patterns = patterns or [("glider", 0, 0)]

    World.start(patterns)
