'''setup for GameOfLife

'''

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


long_description = '''
GameOfLife is a python3 package that provides two classes
that together implement Conway's Game of Life.

Install the GameOfLife package using pip::
   
   $ sudo pip3 install GameOfLife
   

Or clone the git repository::
   
   $ git clone https://github.com/JnyJny/GameOfLife.git
   $ cd GameOfLife
   $ sudo python3 setup.py install

Also included in the package is CGameOfLife, a python script that
displays the simulation in a terminal window using curses.

Old skool is best skool.
'''

try:    
    with open(path.join(here,'VERSION'), encoding='utf-8') as f:
        version = f.read()[:-1]
except FileNotFoundError:
    version = '0.0.0'

GITHUB='https://github.com/JnyJny/GameOfLife'

setup(name='GameOfLife',
      version=version,
      description = "Conway's Game of Life - Cellular Automata.",
      long_description = long_description,
      url = GITHUB,
      download_url = GITHUB,
      author="Erik O'Shaughnessy",
      author_email="erik.oshaughnessy@gmail.com",
      license='MIT',
      classifiers=[ 'Development Status :: 3 - Alpha',
                    'Intended Audience :: Developers',
                    'Topic :: Software Development :: Libraries :: Python Modules',
                    'Topic :: Scientific/Engineering :: Mathematics',
                    'License :: OSI Approved :: MIT License',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.4'],
      keywords = 'conway game life cellular automata',
      packages = find_packages(exclude=['contrib','tests']),
      scripts = ['contrib/CGameOfLife.py'],
      install_requires = [],
      extras_require = {},
      package_data = {},
      data_files= [],
)


