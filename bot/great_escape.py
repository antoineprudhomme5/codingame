import sys
from collections import deque

# TODO: LES MURS NE SONT PAS SUR LES CELLULES, MAIS ENTRE LES CELLULES ...
# refactoring à faire pour fix ça

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
        if orientation == "V":
            self.map[y][x].left = False
            self.map[y+1][x].left = False
            if x < 0:
                self.map[y][x-1].down = False
                self.map[y+1][x-1].down = False
        if orientation == "H":
            self.map[y][x].up = False
            self.map[y][x+1].up = False
            if y < 0:
                self.map[y-1][x].down = False
                self.map[y-1][x+1].down = False

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

    def _valid_wall(self, x1, y1, x2, y2, direction):
        """ Check if the given when can be placed on the map

            Args:
                x1 -- int -- x coordinate of the first wall's cell
                y1 -- int -- y coordinate of the first wall's cell
                x2 -- int -- x coordinate of the second wall's cell
                y3 -- int -- y coordinate of the second wall's cell

            return True if the wall can be placed
        """
        if x1 < 1 or x1 > self.width-1 or y1 < 1 or y1 > self.height-1:
            return False

        first_ngbr = (x1-1, y1) if direction == "V" else (x1, y1-1)
        second_ngbr = (x2+1, y2) if direction == "V" else (x2, y2+1)

        if self._cell_exist(first_ngbr[0], first_ngbr[1]) and self.map[first_ngbr[1]][first_ngbr[0]].is_wall:
            return False
        if self._cell_exist(second_ngbr[0], second_ngbr[1]) and self.map[second_ngbr[1]][second_ngbr[0]].is_wall:
            return False

        return True

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

    def try_to_block_enemy(self, enemy_path, my_path):
        """ Try to put a wall on the map to block the enemy
            If it's possible, return the wall position and orientation
            If not, return None

            Args:
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
                ###print("to block => %d %d" % (enemy_path[i].x, enemy_path[i].y), file=sys.stderr)
                # compare the cells to know the enemy direction at this point
                direction = enemy_path[i-1].compare(enemy_path[i])

                x = enemy_path[i].x
                y = enemy_path[i].y

                if direction == "UP" or direction == "DOWN":
                    # check if empty cell at the left or right
                    if self._valid_wall(x-1, y, x, y, "H"):
                        return (x-1, y, "H")
                    if self._valid_wall(x, y, x+1, y, "H"):
                        return (x, y, "H")
                else:
                    # check if empty cell at the left or right
                    if self._valid_wall(x, y-1, x, y, "V"):
                        return (x, y-1, "V")
                    if self._valid_wall(x, y, x, y+1, "V"):
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

    def __str__(self):
        """ Build and return a string describing the map
        """
        s = " _ " * self.width + "\n"
        for j in range(self.height):
            t = ""
            for i in range(self.width):
                t += " " if self.map[j][i].left else "|"
                t += "."
                t += " " if self.map[j][i].right else "|"
            t += "\n"
            for i in range(self.width):
                t += " _ " if self.map[j][i].down else "   "
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
            board.add_wall(wall_x, wall_y, wall_orientation)

        #print(board, file=sys.stderr)

        # calculate the shortest path for all players
        paths = [board.find_shortest_path(i) for i in range(player_count)]

        for cell in paths[my_id]:
            print("%d %d" % (cell.x, cell.y), file=sys.stderr)

        """
        # if an enemy's path is shorter than mine, I have to block him
        # if an enemy's path is same length than mine but he play before, I have to block him too
        enemy_to_block = None
        for i in range(player_count):
            if i != my_id and (len(paths[my_id]) > len(paths[i])) or (len(paths[my_id]) == len(paths[i]) and my_id > i):
                enemy_to_block = paths[i]

        # action: LEFT, RIGHT, UP, DOWN or "putX putY putOrientation" to place a wall
        can_block_enemy = None
        if enemy_to_block and board.players[my_id].walls_left > 0:
            can_block_enemy = board.try_to_block_enemy(enemy_to_block, paths[my_id])

        print(can_block_enemy, file=sys.stderr)
        """
        can_block_enemy = None
        if can_block_enemy:
            print("%d %d %s" % can_block_enemy)
        else:
            next_cell = paths[my_id][1]
            direction = board.player_cell(my_id).compare(next_cell)
            print(direction)
