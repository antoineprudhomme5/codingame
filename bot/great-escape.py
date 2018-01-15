import sys

class Cell(object):
    def __init__(self):
        self.wall = False
        self.player = None

    def __str__(self):
        if self.wall:
            return "x"
        if self.player:
            return str(self.player.id)
        return "."

class Player(object):
    def __init__(self, id):
        self.id = id
        self.x = 0
        self.y = 0
        self.walls_left = 0

    def update(self, x, y, walls_left):
        """ update the coordinates and number of walls left
            of the player
        """
        self.x = x
        self.y = y
        self.walls_left = walls_left

class Board(object):
    def __init__(self, width, height, nb_player):
        self.width = width
        self.height = height
        # init the players
        self.players = [Player(i) for i in range(nb_player)]
        # init the map with empty cells
        self.map = [[Cell() for _ in range(width)] for _ in range(height)]

    def update_player(self, id, x, y, walls_left):
        """ update a player in the board

            Args:
                id -- int -- player id
                x -- int -- new x coordinate
                y -- int -- new y coordinate
                walls_left -- int -- number of walls this player can still place
        """
        #
        current_cell = self.map[self.players[id].y][self.players[id].x]
        if current_cell.player and current_cell.player.id == id:
            self.map[self.players[id].y][self.players[id].x].player = None
        # set the new player's cell
        self.players[id].update(x, y, walls_left)
        self.map[y][x].player = self.players[id]

    def add_wall(self, x, y, orientation):
        """ create a new wall
            if it already exists, nothing will change
            else, a new wall will be created

            Args:
                x -- int -- x coordinate
                y -- int -- y coordinate
                orientation -- string -- V for vertical, H for horizontal
        """
        self.map[y][x].wall = True
        if orientation == "V" and y+1 < self.height:
            self.map[y+1][x].wall = True
        if orientation == "H" and x+1 < self.width:
            self.map[y][x+1].wall = True

    def __str__(self):
        """ Build and return a string describing the map
            The content of each cell is represented by a character

            return a multilines string (the game's map)
        """
        return '\n'.join(''.join(str(cell) for cell in self.map[i]) for i in range(self.height))

# player_count: number of players (2 or 3)
# my_id: id of my player (0 = 1st player, 1 = 2nd player, ...)
board_width, board_height, player_count, my_id = map(int, input().split())

board = Board(board_width, board_height, player_count)
# game loop
while True:
    for i in range(player_count):
        # walls_left: number of walls available for the player
        x, y, walls_left = map(int, input().split())
        board.update_player(i, x, y, walls_left)
    wall_count = int(input())  # number of walls on the board
    for i in range(wall_count):
        # wall_orientation: wall orientation ('H' or 'V')
        wall_x, wall_y, wall_orientation = input().split()
        wall_x = int(wall_x)
        wall_y = int(wall_y)
        board.add_wall(wall_x, wall_y, wall_orientation)

    print(board, file=sys.stderr)
    # action: LEFT, RIGHT, UP, DOWN or "putX putY putOrientation" to place a wall
    print("RIGHT")
