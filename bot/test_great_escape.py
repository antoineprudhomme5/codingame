import unittest

from great_escape import Cell

class TestGreatEscape(unittest.TestCase):

    def test_cell_compare(self):
        x = 2
        y = 2
        main = Cell(x, y)
        up = Cell(x, y-1)
        down = Cell(x, y+1)
        right = Cell(x+1, y)
        left = Cell(x-1, y)

        # adjacent cells
        self.assertEqual(main.compare(up), "UP")
        self.assertEqual(up.compare(main), "DOWN")
        self.assertEqual(main.compare(down), "DOWN")
        self.assertEqual(down.compare(main), "UP")
        self.assertEqual(main.compare(right), "RIGHT")
        self.assertEqual(right.compare(main), "LEFT")
        self.assertEqual(main.compare(left), "LEFT")
        self.assertEqual(left.compare(main), "RIGHT")
        # same cell
        self.assertEqual(main.compare(main), None)

    def test_is_free(self):

if __name__ == '__main__':
    unittest.main()
