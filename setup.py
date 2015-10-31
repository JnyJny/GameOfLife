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

Also included in the package are:

CGameOfLife: displays the simulation in a terminal window using curses.
PGameOfLife: displays the simulation in a PyGame window with pretty pictures.
'''

try:    
    with open(path.join(here,'VERSION'), encoding='utf-8') as f:
        version = f.read()[:-1]
except FileNotFoundError:
    version = '0.0.0'

download_url = 'https://github.com/JnyJny/GameOfLife/archive/{}.tar.gz'

setup(name='GameOfLife',
      version=version,
      description = "Conway's Game of Life - Cellular Automata.",
      long_description = long_description,
      url = 'https://github.com/JnyJny/GameOfLife',
      download_url = download_url.format(version),
      author="Erik O'Shaughnessy",
      author_email="erik.oshaughnessy@gmail.com",
      license='MIT',
      classifiers=[ 'Development Status :: 3 - Alpha',
                    'Intended Audience :: Developers',
                    'Operating System :: POSIX',
                    'Environment :: Console :: Curses',
                    'Topic :: Software Development :: Libraries :: Python Modules',
                    'Topic :: Scientific/Engineering :: Mathematics',
                    'Topic :: Scientific/Engineering :: Artificial Life',
                    'Topic :: Games/Entertainment :: Simulation',
                    'License :: OSI Approved :: MIT License',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.4'],
      keywords = 'conway game life cellular automata simulation',
      packages = find_packages(exclude=['contrib']),
      test_suite = 'GameOfLife.tests',
      scripts = ['contrib/CGameOfLife.py','contrib/PGameOfLife.py'],
      install_requires = [],
      extras_require = {},
      package_data = {},
      data_files= [],
)


