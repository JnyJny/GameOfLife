"""
"""


import click

from .version import __version__


@click.command()
@click.version_option(__version__)
def cli():
    print("Do you want to play a game? [y/n] ")
