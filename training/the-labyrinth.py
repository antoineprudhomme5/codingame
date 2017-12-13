import sys
import math
from collections import deque, namedtuple

# define the Point namedtuple
Point = namedtuple('Point', ['r', 'c'])

def find_neighbours(arr, cell):
    neighbours = [
        Point(r=cell[0], c=cell[1]+1),
        Point(r=cell[0], c=cell[1]-1),
        Point(r=cell[0]+1, c=cell[1]),
        Point(r=cell[0]-1, c=cell[1])]

    return [neighbour for neighbour in neighbours if is_cell_reachable(arr, neighbour)]

def is_cell_reachable(arr, cell):
    return (cell[0] >= 0
            and cell[0] < len(arr)
            and cell[1] >= 0
            and cell[1] < len(arr[0])
            and arr[cell[0]][cell[1]].value != '#')

def heuristic(a, b):
    return abs(a.r - b.r) + abs(a.c - b.c)

def a_star(arr, start, target):
    # cells already evaluated
    closed_set = {}
    # cells discovered by not evaluated yet
    open_set = [start]
    # most efficient previous steps
    came_from = {}
    # for each node, the coast from start to this cell
    g_score = {}
    g_score[start] = 0
    # for each cell, the coast from the start to the end, passing throught this cell
    f_score = {}
    f_score[start] = heuristic(start, target)

    while len(open_set):

        # find the cell with the lowest f score
        lowestIndex = 0
        for i in range(1, len(open_set)):
            if f_score[open_set[i]] < f_score[open_set[lowestIndex]]:
                lowestIndex = i

        current = open_set.pop(lowestIndex)

        if current.r == target.r and current.c == target.c:
            # build and return the path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path

        closed_set[current] = True

        for neighbour in find_neighbours(arr, current):
            # check if already evaluated
            if neighbour in closed_set:
                continue
            # check if not discovered
            if neighbour not in open_set:
                open_set.append(neighbour)

            tempG = g_score[current] + 1
            if neighbour not in g_score or tempG < g_score[neighbour]:
                # better path found
                came_from[neighbour] = current
                g_score[neighbour] = tempG
                f_score[neighbour] = g_score[neighbour] + heuristic(neighbour, target)

    return False


def BFS(grid, start, target):
    queue = deque()
    queue.append(start)
    parents = {start: None}

    def is_valid_cell(cell):
        return (is_cell_reachable(grid, cell) and cell not in parents)

    while len(queue):
        cell = queue.popleft()

        if grid[cell[0]][cell[1]].value == target:
            path = []
            while cell:
                path.append(parents[cell])
                cell = parents[cell]
            return path[::-1]

        # queue each unvisited neighbours
        neighbours = find_neighbours(grid, cell)
        for neighbour in neighbours:
            if is_valid_cell(neighbour):
                queue.append(neighbour)

                parents[neighbour] = cell

class Cell(object):
    def __init__(self, value):
        self.value = value
        self.score = 0

class Grid(object):
    def __init__(self, nb_rows, nb_cols, alarm):
        self.nb_rows = nb_rows
        self.nb_cols = nb_cols
        self.alarm = alarm
        self.grid = [None] * nb_rows
        self.CR_pos = None
        self.kirk_pos = None
        self.CR_reached = False

    def update_row(self, row_index, row):
        self.grid[row_index] = row
        if not self.CR_pos:
            for col, cell in enumerate(self.grid[row_index]):
                if cell.value == 'C':
                    self.CR_pos = Point(r=row_index, c=col)
                    break

    def find_cell(self, arr, target):
        for row in range(self.nb_rows):
            for col, cell in enumerate(self.grid[row]):
                if cell.value == target:
                    return (row, col)
        return None

    def find_direction(self, target):
        if target.r > self.kirk_pos.r:
            return "DOWN"
        if target.c > self.kirk_pos.c:
            return "RIGHT"
        if target.r < self.kirk_pos.r:
            return "UP"
        if target.c < self.kirk_pos.c:
            return "LEFT"

# rows:     number of rows.
# cols:     number of columns.
# alarm:    number of rounds between the time the alarm countdown is activated and
#           the time the alarm goes off.
nb_rows, nb_cols, alarm = [int(i) for i in input().split()]

grid = Grid(nb_rows, nb_cols, alarm)

# game loop
while True:
    # update kirk pos
    kirk_row, kirk_col = [int(i) for i in input().split()]
    grid.kirk_pos = Point(r=kirk_row, c=kirk_col)
    # update the grid
    for i in range(nb_rows):
        grid.update_row(i, [Cell(v) for v in list(input())])

    # if kirk is in the command room, update CR_reached
    if grid.kirk_pos and grid.CR_pos and grid.kirk_pos.r == grid.CR_pos.r and grid.kirk_pos.c == grid.CR_pos.c:
        grid.CR_reached = True

    if grid.CR_reached:
        # run out
        next_cell = Point(r=kirk_row, c=kirk_col-1)
    else:
        if grid.CR_pos:
            # go to the command room
            path = a_star(grid.grid, grid.kirk_pos, grid.CR_pos)
            next_cell = path[len(path) - 2]
        else:
            # keep exploring the grid to find the command room
            next_cell = BFS(grid.grid, grid.kirk_pos, "?")[2]

    # Kirk's next move (UP DOWN LEFT or RIGHT).
    print(grid.find_direction(next_cell))
