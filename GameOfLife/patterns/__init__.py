'''Conway's Game of Life
'''

static = { 
    'block':'xx\nxx',
    'beehive':' xx \nx  x\n xx ',
    'loaf':' xx \nx  x\n x x\n   x',
    'boat':'xx \nx x\n x '
}

movers = {
    'glider':' x \n  x\nxxx',
    'lws':'x  x\n    x\nx   x\n xxxx'
}

blinkers = {             
    'blinker': 'xxx',
    'toad': ' xxx\nxxx ',
    'beacon': 'xx  \nxx  \n  xx\n  xx\n',
    'pulsar':'  xxx   xxx\n\nx    x x    x\nx    x x    x\nx    x x    x\n  xxx   xxx\n\n  xxx   xxx\nx    x x    x\nx    x x    x\nx    x x    x\n\n  xxx   xxx'
}

factories = {

}

Patterns = {}
for _ in [ static, movers, blinkers, factories ]:
    Patterns.update(_)


class Pattern(object):
    pass


def pattern_dimesions(pattern):
    '''
    :return: tuple(nRows,nColumns)

    '''
    return len(pattern),max([len(r) for r in pattern])


def rotate_90(pattern,ccw=False):
    '''
    :param: pattern - list of strings
    :param: ccw - boolean
    :return: list of strings

    '''
    
    nRows,nCols = pattern_dimensions(pattern)

    for y in range(nRows):
        for x in range(nCols):
            pass
    
    return ''
