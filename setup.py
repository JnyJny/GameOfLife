'''setup for GameOfLife

'''

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here,'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

try:    
    with open(path.join(here,'VERSION'), encoding='utf-8') as f:
        version = f.read()[:-1]
except FileNotFoundError:
    version = '0.0.0'

setup(name='GameOfLife',
      version=version,
      description = "Conway's Game of Life - Cellular Automata.",
      long_description = long_description,
      url = 'https://github.com/JnyJny/GameOfLife',
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
      packages = find_packages(exclude=['contrib','docs','tests','bin']),
      scripts = ['contrib/CGameOfLife.py'],
      install_requires = [],
      extras_require = {},
      package_data = {},
      data_files= [],
)


