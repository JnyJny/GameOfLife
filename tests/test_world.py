import unittest

from GameOfLife import Cell, Patterns
from GameOfLife.world import World, OptimizedWorld
from GameOfLife.world import NumpyWorld, OptimizedNumpyWorld
import numpy


class WorldTestCase(unittest.TestCase):
    def assertIsWorld(self, obj):
        self.assertIsInstance(obj, World)

    #    def assertIsGoodWorld(self,width=None,height=None,cellClass=None):
    #
    #        if width is not None:
    #            self.assertEqual(obj.width,width)
    #
    #        if height is not None:
    #            self.assertEqual(obj.height,height)
    #
    #        if cellClass is None:
    #            cellClass = Cell
    #
    #        self.assertEqual(obj.cellClass,cellClass)
    #
    #        self.assertEqual(len(obj.cells),obj.width * obj.height)
    #
    #        for c in obj:
    #            self.assertIsInstance(c,obj.cellClass)

    def testWorldCreation(self):

        self.assertIsWorld(World())

        class TestCell(Cell):
            pass

        self.assertIsWorld(World(cell_class=TestCell))

        dim = 10
        self.assertIsWorld(World(width=dim))
        self.assertIsWorld(World(height=dim))
        self.assertIsWorld(World(width=dim, height=dim))
        self.assertIsWorld(World(dim, dim, TestCell))

    def testCellsProperty(self):
        w = World()
        self.assertIsInstance(w.cells, list)
        self.assertEqual(len(w.cells), w.width * w.height)

    def testFromFile(self):
        pass

    def testFromString(self):
        pass

    def testWriteMethod(self):
        pass

    def testReadMethod(self):
        pass

    def testClampMethod(self):
        w = World(width=10, height=10)
        for y in range(10):
            for x in range(10):
                xy = (x, y)
                self.assertSequenceEqual(xy, w._warp(xy))

        for y in range(10, 20):
            for x in range(10, 20):
                xy = (x, y)
                XY = (x - 10, y - 10)
                self.assertSequenceEqual(XY, w._warp(xy))

        # test wrapping here?

    def testGetitemMethod(self):
        world = World(width=10, height=10)
        for cell in world:
            self.assertTrue(cell is world[cell.location])

    def testResetMethod(self):

        world = World(width=10, height=10)

        self.assertEqual(len([c for c in world if c.alive]), 0)

        world[0, 0].alive = True
        world[1, 0].alive = True
        world[0, 1].alive = True
        world[1, 1].alive = True

        self.assertEqual(len([c for c in world if c.alive]), 4)

        world.step()

        self.assertEqual(len([c for c in world if c.alive]), 4)
        self.assertEqual(world.generation, 1)

        world.reset()
        self.assertEqual(len(world.cells), world.width * world.height)
        self.assertEqual(len([c for c in world if c.alive]), 0)
        self.assertEqual(world.generation, 0)

    def testStepMethod(self):
        world = World(width=10, height=10)

        # this is a static pattern for classic game of life rules
        world[0, 0].alive = True
        world[0, 1].alive = True
        world[1, 0].alive = True
        world[1, 1].alive = True

        # these cells will never transition from alive to dead as
        # long as no other neighbor cells become alive.
        self.assertEqual(world[0, 0].age, 0)
        self.assertEqual(world[0, 1].age, 0)
        self.assertEqual(world[1, 0].age, 0)
        self.assertEqual(world[1, 1].age, 0)

        self.assertEqual(len([c for c in world if c.alive]), 4)

        for trip in range(1, 10):
            world.step()
            alive_cells = [c for c in world if c.alive]
            self.assertEqual(len(alive_cells), 4)
            self.assertEqual(world.generation, trip)
            for cell in alive_cells:
                self.assertEqual(cell.age, trip)

        world.reset()

        world[0, 0].alive = True

        world.step()
        self.assertEqual(len([c for c in world if c.alive]), 0)

    def testAddMethod(self):

        # needs world bounds checking for world smaller than pattern

        for pattern in Patterns.values():

            world = World(width=100, height=100)

            nAlivePatternCells = len([c for c in pattern if not c.isspace()])

            world.add_pattern(pattern)

            self.assertEqual(
                len([cell for cell in world if cell.alive]),
                nAlivePatternCells,
                "pattern {pattern}".format(pattern=pattern),
            )

        for name, pattern in Patterns.items():

            world = World(width=100, height=100)

            nAlivePatternCells = len([c for c in pattern if not c.isspace()])

            world.add_named_pattern(name)

            self.assertEqual(
                len([cell for cell in world if cell.alive]),
                nAlivePatternCells,
                "{name} pattern {pattern}".format(name=name, pattern=pattern),
            )

        # XXX test x,y, rule, eol and resize


class OptimizedWorldTestCase(WorldTestCase):
    def testAliveProperty(self):
        pass

    def testResetMethod(self):
        pass

    def testAddMethod(self):
        pass

    def testStepMethod(self):
        pass


class NumpyWorldTestCase(unittest.TestCase):
    def assertIsNumpyWorld(self, obj, width=None, height=None):
        self.assertIsInstance(obj, NumpyWorld)

        self.assertIsInstance(obj.cells, numpy.ndarray)

        if width is not None and height is not None:
            self.assertSequenceEqual(obj.cells.shape, (width, height))

        if width is not None:
            self.assertEqual(obj.width, width)

        if height is not None:
            self.assertEqual(obj.height, height)


class OptimizedNumpyWorldTestCase(NumpyWorldTestCase):
    pass
