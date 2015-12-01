'''Test Suite for GameOfLife

'''

from .test_cell import CellTestCase
from .test_world import WorldTestCase, OptimizedWorldTestCase
from .test_patterns import PatternsTestCase

__all__ = ['CellTestCase',
           'WorldTestCase',
           'OptimizedWorldTestCase',
           'PatternsTestCase']
