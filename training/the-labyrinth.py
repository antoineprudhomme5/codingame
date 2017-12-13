import sys
import math
from collections import deque

turn = 1

class Cell(object):
    def __init__(self, value):
        self.value = value
        self.score = 0

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_direction(current, target):
    if target[0] > current[0]:
        return "DOWN"
    if target[1] > current[1]:
        return "RIGHT"
    if target[0] < current[0]:
        return "UP"
    if target[1] < current[1]:
        return "LEFT"

def sort_insertion(arr, value):
    if len(arr) == 0:
        return [value]
    if arr[0] < value:
        return [value] + arr

    i = 0
    while i < len(arr):
        if arr[i] < value:
            i += 1
    return arr[::i] + [value] + arr[i::]

def find_cell(arr, target):
    for row in range(len(arr)):
        for col, cell in enumerate(arr[row]):
            if cell.value == target:
                return (row, col)
    return None

def is_cell_reachable(arr, cell):
    return (cell[0] >= 0
            and cell[0] < len(arr)
            and cell[1] >= 0
            and cell[1] < len(arr[0])
            and arr[cell[0]][cell[1]].value != '#')

def find_neighbours(arr, cell):
    neighbours = [
            (cell[0], cell[1]+1),
            (cell[0], cell[1]-1),
            (cell[0]+1, cell[1]),
            (cell[0]-1, cell[1])]

    return [neighbour for neighbour in neighbours if is_cell_reachable(arr, neighbour)]

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
        current = open_set.pop()
        if current == target:
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
                open_set = sort_insertion(open_set, neighbour)

                tempG = g_score[current] + 1
                if neighbour not in g_score or tempG < g_score[neighbour]:
                    # better path found
                    came_from[neighbour] = current
                    g_score[neighbour] = tempG
                    f_score[neighbour] = tempG + heuristic(neighbour, target)

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
        if turn == 6:
            print(neighbours)
        for neighbour in neighbours:
            if is_valid_cell(neighbour):
                queue.append(neighbour)

                parents[neighbour] = cell

# rows:     number of rows.
# cols:     number of columns.
# alarm:    number of rounds between the time the alarm countdown is activated and
#           the time the alarm goes off.
rows, cols, alarm = [int(i) for i in input().split()]
# True if krik reached the command room
CR_reached = False

# game loop
while True:
    # kirk_row: row where Kirk is located.
    # kirk_col: column where Kirk is located.
    kirk_row, kirk_col = [int(i) for i in input().split()]
    kirk_pos = (kirk_row, kirk_col)
    # read the grid
    grid = []
    for i in range(rows):
        grid.append([Cell(v) for v in list(input())])
    # search if C has been discovered
    C_pos = find_cell(grid, 'C')
    # check if kirk reached the command room
    if not CR_reached and C_pos == kirk_pos:
        CR_reached = True
    # if C hasn't been discovered, continue to search
    # (use BFS to find the closest cell to discover)
    if C_pos == None:
        next_cell = BFS(grid, kirk_pos, "?")[2]
    # else, if C has been discovered and kirk didn't reach it, go to C
    elif not CR_reached:
        next_cell = (kirk_row, kirk_col+1)
        #next_cell = a_star(grid, kirk_pos, C_pos)
    else:
        next_cell = (kirk_row, kirk_col-1)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # Kirk's next move (UP DOWN LEFT or RIGHT).
    print(find_direction((kirk_row, kirk_col), next_cell))
