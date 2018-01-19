import unittest

from great_escape import Cell, Board

class TestGreatEscape(unittest.TestCase):

    def test_update_player(self):
        """ test the player's position
        """
        # create board
        width = 9
        height = 9
        nb_players = 3
        board = Board(width, height, nb_players)
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
