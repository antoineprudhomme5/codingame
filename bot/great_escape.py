import sys
from collections import deque

# TODO: when more than 2 players, don't use all the walls at the beginning

class Cell(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.players = []
        # directions avaibles from this cell
        self.up = True
        self.down = True
        self.right = True
        self.left = True

    def compare(self, cell):
        """ Compare this instance with the Cell passed in parameters

            Args:
                cell -- Cell -- the cell to reach

            return a string, describing the direction to take to reach this cell
        """
        if cell.x > self.x:
            return "RIGHT"
        if cell.x < self.x:
            return "LEFT"
        if cell.y > self.y:
            return "DOWN"
        if cell.y < self.y:
            return "UP"
        return None

class Player(object):
    def __init__(self, id, x_goal, y_goal):
        self.id = id
        self.in_game = True
        self.x = 0
        self.y = 0
        self.walls_left = 0
        self.x_goal = x_goal
        self.y_goal = y_goal

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
        # init the players's goals
        self.goals = [
                (width-1, None),
                (0, None),
                (None, height-1),
                (None, 0)
            ]
        # init the players
        self.players = []
        for i in range(nb_player):
            self.players.append(Player(i, self.goals[i][0], self.goals[i][1]))
        # init the map with empty cells
        self.map = [[Cell(x, y) for x in range(width)] for y in range(height)]
        for i in range(width):
            self.map[0][i].up = False
            self.map[height-1][i].down = False
        for i in range(height):
            self.map[i][0].left = False
            self.map[i][width-1].right = False

    def update_player(self, id, x, y, walls_left=0):
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
        # check if this player is still in the game
        if x != -1 and y != -1:
            # set the new player's cell
            self.players[id].update(x, y, walls_left)
            self.map[y][x].players.append(self.players[id])
        else:
            self.players[id].in_game = False

    def set_wall(self, x, y, orientation, value=False):
        """ create or remove a wall

            Args:
                x -- int -- x coordinate
                y -- int -- y coordinate
                orientation -- string -- V for vertical, H for horizontal
                value -- boolean -- if False, build a wall. If True, remove the wall
        """
        if orientation == "V":
            self.map[y][x].left = value
            self.map[y+1][x].left = value
            if x > 0:
                self.map[y][x-1].right = value
                self.map[y+1][x-1].right = value
        if orientation == "H":
            self.map[y][x].up = value
            self.map[y][x+1].up = value
            if y > 0:
                self.map[y-1][x].down = value
                self.map[y-1][x+1].down = value

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

    def _valid_wall(self, x, y, direction, enemy):
        """ Check if the given wall can be placed on the map

            Args:
                x -- int -- x coordinate of the first wall's cell
                y -- int -- y coordinate of the first wall's cell
                direction -- string -- wall's direction: V or H
                enemy -- int -- the id of the enemy to block

            return True if the wall can be placed
        """
        if x < 0 or y < 0:
            return False

        is_valid = False

        if direction == "V" and y < self.height-1:
            # if top/bottom neighbours, check that they don't have a wall to the left
            if (y-1 < 0 or self.map[y-1][x].left) and (y+1 > self.height-1 or self.map[y+1][x].left):
                # check if the wall will not cut another wall
                if self.map[y][x].down or (x-1 < 0 or self.map[y][x-1].down):
                    is_valid = True
        elif direction == "H" and x < self.width-1:
            # if right/left neighbours, check that they don't have a wall to the top
            if (x-1 < 0 or self.map[y][x-1].up) and (x+1 > self.width-1 or self.map[y][x+1].up):
                # check if the wall will not cut another wall
                if self.map[y][x].right or (y-1 < 0 or self.map[y-1][x].right):
                    is_valid = True

        if is_valid:
            # check if the enemy can steal reach his goal
            self.set_wall(x, y, direction)
            is_valid = bool(self.find_shortest_path(enemy))
            self.set_wall(x, y, direction, True)

        return is_valid

    def _cell_neighbours(self, cell):
        """ Find the reachable neighbours of the cell given his coordinates

            Args:
                cell -- Cell -- the current cell

            return a list of Cell
        """
        neighbours = []

        # try each direction
        if cell.up: neighbours.append(self.map[cell.y-1][cell.x])
        if cell.down: neighbours.append(self.map[cell.y+1][cell.x])
        if cell.right: neighbours.append(self.map[cell.y][cell.x+1])
        if cell.left: neighbours.append(self.map[cell.y][cell.x-1])

        return neighbours

    def try_to_block_enemy(self, enemy, enemy_path, my_path):
        """ Try to put a wall on the map to block the enemy
            If it's possible, return the wall position and orientation
            If not, return None

            Args:
                enemy -- int -- id of the enemy to block
                enemy_path -- list of Cell -- the path of the enemy
                my_path -- list of Cell -- my path

            return None or a tuple (x -- int, y -- int, orientation -- string)
        """
        # create a dic with the cells on my path
        my_path_dic = {}
        for i in range(1, len(my_path)):
            my_path_dic[my_path[i]] = True
        # check if a cell is not on my path
        for i in range(1, len(enemy_path)):
            if enemy_path[i] not in my_path_dic:
                # compare the cells to know the enemy direction at this point
                direction = enemy_path[i-1].compare(enemy_path[i])

                x = enemy_path[i].x
                y = enemy_path[i].y

                if direction == "UP" or direction == "DOWN":
                    # check if empty cell at the left or right
                    if self._valid_wall(x-1, y, "H", enemy):
                        return (x-1, y, "H")
                    if self._valid_wall(x, y, "H", enemy):
                        return (x, y, "H")
                else:
                    # check if empty cell at the left or right
                    if self._valid_wall(x, y-1, "V", enemy):
                        return (x, y-1, "V")
                    if self._valid_wall(x, y, "V", enemy):
                        return (x, y, "V")
        return None

    def find_shortest_path(self, id):
        """ Find the path the player should take to reach his goal
            using BFS

            Args:
                id -- int -- the player's id

            return the next path to his goal (a list of Cell)
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
            if current_cell.x == player.x_goal or current_cell.y == player.y_goal:
                path = [current_cell]
                while current_cell in found_cells and found_cells[current_cell]:
                    current_cell = found_cells[current_cell]
                    path.append(current_cell)
                return list(reversed(path))

            # add his unvisited neighbours to the next level
            for neighbour in self._cell_neighbours(current_cell):
                if neighbour not in found_cells:
                    found_cells[neighbour] = current_cell
                    next_level.append(neighbour)

            # if the current level is empty, switch to the next level
            if len(current_level) == 0:
                current_level = next_level
                next_level = deque()

        return None

    def __str__(self):
        """ Build and return a string describing the map
        """
        s = " _ " * self.width + "\n"
        for j in range(self.height):
            t = ""
            for i in range(self.width):
                t += " " if self.map[j][i].left else "|"
                t += str(self.map[j][i].players[0].id) if len(self.map[j][i].players) else "."
                t += " " if self.map[j][i].right else "|"
            t += "\n"
            for i in range(self.width):
                t += " " if self.map[j][i].down else " _ "
            t += "\n"
            s += t
        return s

if __name__ == '__main__':
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
            board.set_wall(wall_x, wall_y, wall_orientation)

        nb_players_in_game = 0
        paths = [None] * player_count
        # calculate the shortest path for all players
        for i in range(player_count):
            if board.players[i].in_game:
                paths[i] = board.find_shortest_path(i)
                nb_players_in_game += 1
            else:
                paths[i] = None

        # find the enemy with the shortest path
        enemy_number_one = None
        for i in range(player_count):
            if i != my_id and paths[i] and (not enemy_number_one or len(paths[i] < len(paths[enemy_number_one]))):
                enemy_number_one = i

        me_remaining = len(paths[my_id])-1
        enemy_remaining = len(paths[enemy_number_one])-1

        wall = None
        # check if I still have walls
        if board.players[my_id].walls_left > 0:
            if nb_players_in_game == 2:
                # 1V1
                if enemy_remaining < me_remaining:
                    # if the enemy is closer than me, block him
                    wall = board.try_to_block_enemy(enemy_number_one, paths[enemy_number_one], paths[my_id])
            else:
                # 1v2
                if enemy_remaining < (me_remaining - enemy_remaining):
                    print("BLOOOCK", file=sys.stderr)
                    wall = board.try_to_block_enemy(enemy_number_one, paths[enemy_number_one], paths[my_id])
                    print(wall, file=sys.stderr)

        if wall:
            print("%d %d %s" % wall)
        else:
            next_cell = paths[my_id][1]
            direction = board.player_cell(my_id).compare(next_cell)
            print(direction)
