'''Conway's Game of Life

Canned patterns.

'''

from pkg_resources import ResourceManager

Patterns = {}
_EXT = '.life'
_rm = ResourceManager()
_pkg = 'GameOfLife.patterns.data'
for fname in [f for f in _rm.resource_listdir(_pkg,'.') if f.endswith(_EXT)]:
    with _rm.resource_stream(_pkg,fname) as f:
        Patterns.setdefault(fname.split('.')[0].lower(),
                            f.read().decode('utf-8'))

class Pattern(object):
    def __init__(self,name,data=None):
        pass
