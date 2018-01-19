import unittest

from great_escape import Cell, Board

class TestGreatEscape(unittest.TestCase):

    def test_add_wall_vertical(self):
        # create board
        board = Board(9, 9, 3)
        # create a horizontal wall
        h_wall_x = 5
        h_wall_y = 2
        board.add_wall(h_wall_x, h_wall_y, "H")
        # check that the wall has been created
        self.assertFalse(board.map[h_wall_y][h_wall_x].up)
        self.assertFalse(board.map[h_wall_y][h_wall_x+1].up)
        self.assertFalse(board.map[h_wall_y-1][h_wall_x].down)
        self.assertFalse(board.map[h_wall_y-1][h_wall_x+1].down)
        # create a vertical wall
        v_wall_x = 5
        v_wall_y = 5
        board.add_wall(v_wall_x, v_wall_y, "V")
        # check that the wall has been created
        self.assertFalse(board.map[v_wall_y][v_wall_x].left)
        self.assertFalse(board.map[v_wall_y+1][v_wall_x].left)
        self.assertFalse(board.map[v_wall_y][v_wall_x-1].right)
        self.assertFalse(board.map[v_wall_y+1][v_wall_x-1].right)

    def test_update_player(self):
        """ test the player's position
        """
        # create board
        board = Board(9, 9, 3)
        # player info
        player_id = 0
        player_x = 5
        player_y = 3
        # get the player instance
        player = board.players[player_id]
        # put the player on the board
        board.update_player(player_id, player_x, player_y)
        # assert that the player instance is updated
        self.assertEqual(player.x, player_x)
        self.assertEqual(player.y, player_y)
        # assert that the cell contains the player
        player_cell = board.player_cell(player_id)
        self.assertTrue(player in player_cell.players)
        # update the player's position
        new_player_x = 6
        board.update_player(player_id, new_player_x, player_y)
        # assert that the player instance has been updated
        self.assertEqual(player.x, new_player_x)
        self.assertEqual(player.y, player_y)
        # assert that the player has been removed from the previous cell
        self.assertFalse(player in player_cell.players)
        # assert that the new cell contains the player
        player_cell = board.player_cell(player_id)
        self.assertTrue(player in player_cell.players)

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

if __name__ == '__main__':
    unittest.main()
