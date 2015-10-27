
import unittest

from GameOfLife import Cell

class CellTestCase(unittest.TestCase):

    def assertIsCell(self,obj,x=None,y=None,alive=None,markers=None):
        self.assertIsInstance(obj,Cell)
        if x is not None:
            self.assertEqual(obj.location[0],x)
        if y is not None:
            self.assertEqual(obj.location[1],y)
        if alive is not None:
            self.assertEqual(obj.alive,alive)
        if markers is not None:
            self.assertEqual(obj.markers,markers)

    def testCellCreation(self):

        with self.assertRaises(TypeError):
            cell = Cell()

        with self.assertRaises(TypeError):            
            cell = Cell(0)

        self.assertIsCell(Cell(0,0),x=0,y=0,alive=False,markers=' .')

        alive = True
        self.assertIsCell(Cell(0,0,alive=alive),alive=alive)

        markers = 'ox'
        cell = Cell(0,0,markers=markers)
        self.assertIsCell(cell,markers=markers)

        self.assertTrue(str(cell) == markers[0])
        cell.alive = True
        self.assertTrue(str(cell) == markers[1])


    def testCellAliveProperty(self):
        cell = Cell(0,0)

        cell.alive = True
        cell.age = 1
        self.assertTrue(cell.alive)

        cell.alive = False
        self.assertFalse(cell.alive)
        self.assertEqual(cell.age,0)

    def testCellNeighborsProperty(self):
        x,y = 3,3
        cell = Cell(x,y)

        self.assertEqual(len(cell.neighbors),8)

    def testCellUpdateMethod(self):

        cell = Cell(0,0)

        for n in range(9):
            cell.update(n)
            self.assertEqual(cell.aliveNeighbors,n)
            self.assertFalse(cell.alive)
            self.assertEqual(cell.age,0)

        cell.alive = True

        for n in range(9):
            cell.update(n)
            self.assertEqual(cell.aliveNeighbors,n)
            self.assertTrue(cell.alive)
            self.assertEqual(cell.age,n+1)

    def testCellCommitMethod(self):

        cell = Cell(0,0)

        for n in range(9):
            cell.alive = False
            cell.update(n)
            cell.commit()
            if n == 3:
                self.assertTrue(cell.alive)
            else:
                self.assertFalse(cell.alive)

        for n in range(9):
            cell.alive = True
            cell.update(n)
            cell.commit()

            if n in [2,3]:
                self.assertTrue(cell.alive)
            else:
                self.assertFalse(cell.alive)
                self.assertEqual(cell.age,0)

    def testCellAddMethod(self):
        a = Cell(0,0)
        b = Cell(0,1)

        self.assertEqual(a+b,0) # false false

        a.alive = True

        self.assertEqual(a+b,1) # true false

        b.alive = True

        self.assertEqual(a+b,2) # true true

        a.alive = False

        self.assertEqual(a+b,1) # false true

    def testCellRaddMethod(self):
        a = Cell(0,0)
        
        self.assertEqual(a+0,0)
        self.assertEqual(a+0.0,0)

        a.alive = True

        self.assertEqual(a+0,1)
        self.assertEqual(a+0.0,1)

        a.alive = False

        self.assertEqual(a+1,1)
        self.assertEqual(a+1.0,1)

        a.alive = True
        
        self.assertEqual(a+1,2)
        self.assertEqual(a+1.0,2)

        for n in range(0,8):
            cells = [Cell(x,0) for x in range(n)]
            self.assertEqual(sum(cells),0)
            cells = [Cell(x,0,alive=True) for x in range(n)]
            self.assertEqual(sum(cells),n)
        
