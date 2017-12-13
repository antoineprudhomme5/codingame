import sys
import math
from collections import deque

def find_direction(current, target):
    if target[0] > current[0]:
        return "DOWN"
    if target[1] > current[1]:
        return "RIGHT"
    if target[0] < current[0]:
        return "UP"
    if target[1] < current[1]:
        return "LEFT"

def find_cell(arr, target):
    for row in range(len(arr)):
        for col, val in enumerate(arr[row]):
            if val == target:
                return (row, col)
    return None

def BFS(grid, start, target):
    queue = deque()
    queue.append(start)
    parents = {start: None}

    def is_valid_cell(row, line):
        return (row < len(grid)
                and row >= 0
                and line < len(grid[0])
                and line >= 0
                and grid[row][line] != '#'
                and (row, line) not in parents)

    while len(queue):
        cell = queue.popleft()

        if grid[cell[0]][cell[1]] == target:
            path = []
            while cell:
                path.append(parents[cell])
                cell = parents[cell]
            return path[::-1]

        # queue each unvisited children
        if is_valid_cell(cell[0], cell[1]+1):
            queue.append((cell[0], cell[1]+1))
            parents[(cell[0], cell[1]+1)] = cell
        if is_valid_cell(cell[0], cell[1]-1):
            queue.append((cell[0], cell[1]-1))
            parents[(cell[0], cell[1]-1)] = cell
        if is_valid_cell(cell[0]+1, cell[1]):
            queue.append((cell[0]+1, cell[1]))
            parents[(cell[0]+1, cell[1])] = cell
        if is_valid_cell(cell[0]-1, cell[1]+1):
            queue.append((cell[0]-1, cell[1]))
            parents[(cell[0]-1, cell[1])] = cell

# rows:     number of rows.
# cols:     number of columns.
# alarm:    number of rounds between the time the alarm countdown is activated and
#           the time the alarm goes off.
rows, cols, alarm = [int(i) for i in input().split()]

# game loop
while True:
    # kirk_row: row where Kirk is located.
    # kirk_col: column where Kirk is located.
    kirk_row, kirk_col = [int(i) for i in input().split()]
    # read the grid
    grid = []
    for i in range(rows):
        grid.append(list(input()))
    # search if C has been discovered
    C_pos = find_cell(grid, 'C')
    # if C hasn't been discovered, continue to search
    # (use BFS to find the closest cell to discover)
    if not C_pos:
        next_cell = BFS(grid, (kirk_row, kirk_col), "?")[2]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # Kirk's next move (UP DOWN LEFT or RIGHT).
    print(find_direction((kirk_row, kirk_col), next_cell))
