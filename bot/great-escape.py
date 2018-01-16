import sys
from collections import deque

class Cell(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_wall = False
        self.players = []

    def compare(self, cell):
        """ Compare this instance with the Cell passed in parameters

            Args:
                cell -- Cell -- the cell to reach

            return a string, describing the direction to take to reach this cell
        """
        print("%d %d - %d %d" % (self.x, self.y, cell.x, cell.y), file=sys.stderr)
        if cell.x > self.x:
            return "RIGHT"
        if cell.x < self.x:
            return "LEFT"
        if cell.y > self.y:
            return "UP"
        return "DOWN"

    def __str__(self):
        if self.is_wall:
            return "x"
        if self.players:
            return ''.join(str(player.id) for player in self.players)
        return "."

class Player(object):
    def __init__(self, id, board_width):
        self.id = id
        self.x = 0
        self.y = 0
        self.walls_left = 0
        self.x_goal = (board_width-1) if id == 0 else 0

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
        self.players = [Player(i, width) for i in range(nb_player)]
        # init the map with empty cells
        self.map = [[Cell(x, y) for x in range(width)] for y in range(height)]

    def update_player(self, id, x, y, walls_left):
        """ update a player in the board

            Args:
                id -- int -- player id
                x -- int -- new x coordinate
                y -- int -- new y coordinate
                walls_left -- int -- number of walls this player can still place
        """
        # remove the player from his current cell
        if self.players[id] in self.map[self.players[id].y][self.players[id].x].players:
            self.map[self.players[id].y][self.players[id].x].players.remove(self.players[id])
        # set the new player's cell
        self.players[id].update(x, y, walls_left)
        self.map[y][x].players.append(self.players[id])

    def add_wall(self, x, y, orientation):
        """ create a new wall
            if it already exists, nothing will change
            else, a new wall will be created

            Args:
                x -- int -- x coordinate
                y -- int -- y coordinate
                orientation -- string -- V for vertical, H for horizontal
        """
        self.map[y][x].is_wall = True
        if orientation == "V" and y+1 < self.height:
            self.map[y+1][x].is_wall = True
        if orientation == "H" and x+1 < self.width:
            self.map[y][x+1].is_wall = True

    def player_cell(self, player_id):
        """ Given the id of a player, return his Cell

            Args:
                player_id -- int -- the id of the player

            return a Cell
        """
        player = self.players[player_id]
        return self.map[player.y][player.x]

    def _cell_exist(self, cell_x, cell_y):
        """ Check if a cell exists in the map

            Args:
                cell_x -- int -- x coordinate of the cell
                cell_y -- int -- y coordinate of the cell

            return True if the Cell exists
        """
        return (cell_x >= 0 and cell_x < self.width) and (cell_y >= 0 and cell_y < self.height)

    def _cell_neighbours(self, cell, wall=False):
        """ Find the reachable neighbours of the cell given his coordinates

            Args:
                cell -- Cell -- the current cell
                wall -- boolean -- if False, don't return the neighbours cell that are walls

            return a list of Cell
        """
        neighbours = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        # try each direction
        for d in directions:
            # check if the cell exists
            if self._cell_exist(cell.x + d[0], cell.y + d[1]):
                temp_cell = self.map[cell.y + d[1]][cell.x + d[0]]
                # if we don't want walls, check that the Cell is not a wall
                if not wall and not temp_cell.is_wall:
                    neighbours.append(temp_cell)

        return neighbours

    def find_shortest_path(self, id):
        """ Find the path the player should take to reach his goal
            using BFS

            Args:
                id -- int -- the player's id

            return the next Cell he has to reach
        """
        player = self.players[id]
        current_level = deque([self.map[player.y][player.x]])
        next_level = deque()
        found_cells = {self.map[player.y][player.x]: None}

        # continue while there are cells to visit
        while len(current_level):
            # pop the next cell to analyse
            current_cell = current_level.popleft()

            # if the cell is where we want to go,
            # reup the path and get the next cell to reach
            if current_cell.x == player.x_goal:
                previous = current_cell
                current_cell = found_cells[current_cell]
                while current_cell in found_cells and found_cells[current_cell]:
                    previous = current_cell
                    current_cell = found_cells[current_cell]
                return previous

            # add his unvisited neighbours to the next level
            for neighbour in self._cell_neighbours(current_cell):
                if neighbour not in found_cells:
                    found_cells[neighbour] = current_cell
                    next_level.append(neighbour)

            # if the current level is empty, switch to the next level
            if len(current_level) == 0:
                current_level = next_level
                next_level = deque()

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
    next_cell = board.find_shortest_path(my_id)
    direction = board.player_cell(my_id).compare(next_cell)
    print(direction)
