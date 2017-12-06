#!/usr/bin/env python3

""" Solution for the Blender (episode 1) problem
"""

class Ground(object):
    """ Represent a 2D map
    """

    def __init__(self, nb_lines, nb_columns):
        self.nb_lines = nb_lines
        self.nb_columns = nb_columns
        self.ground = []

    def init_ground(self, lines):
        """ Fill the ground

            Args:
                lines -- list of strings -- the ground's lines
        """
        self.ground = []
        for i in range(self.nb_lines):
            lines[i] = list(lines[i])
            for j in range(self.nb_columns):
                lines[i][j] = [lines[i][j], None]
            self.ground.append(lines[i])

    def get_cell(self, line, column):
        """ Get the content of a cell

            Args:
                line -- int -- the line index
                column -- int -- the column index

            return 2 values:
                a string, the value of the cell
                a direction, int, if visited. Else, None

        """
        return self.ground[line][column][0], self.ground[line][column][1]

    def set_cell(self, line, column, value=None, visited=None):
        """ Update a cell of the ground

            Args:
                line -- int -- the line index
                column -- int -- the column index
                value -- string -- the new cell's value
                visited -- boolean -- the direction of Blender when visiting the cell
        """
        if value:
            self.ground[line][column][0] = value
        if visited:
            self.ground[line][column][1] = visited

    def find_cells(self, value):
        """ Return the coordinates of all the cells that matches the given value

            Args:
                value -- string -- the value to match

            return a list of lists (line -- int, column -- int)
        """
        matches = []
        for i in range(self.nb_lines):
            for j in range(self.nb_columns):
                if self.ground[i][j][0] == value:
                    matches.append([i, j])
        return matches


class Bender(object):
    """ Represent the robot Bender

        Attributes:
            line -- int -- his current line (position)
            column -- int -- his current column (position)
            direction -- int -- his current direction
            drunk -- boolean
    """

    def __init__(self, line, column, direction):
        self.line = line
        self.column = column
        self.direction = direction
        self.drunk = False

    def toggle_drunk(self):
        """ Toggle the drunk attribute
        """
        self.drunk = not self.drunk


class Solution(object):
    """ Main class
    """

    DIRECTIONS = ['SOUTH', 'EAST', 'NORTH', 'WEST']

    def __init__(self, ground):
        self.ground = ground
        # find teleporters
        teleporters = ground.find_cells('T')
        self.teleporter_a = teleporters[0] if teleporters else None
        self.teleporter_b = teleporters[1] if teleporters else None
        # find blender initial position
        bender = ground.find_cells('@')
        self.bender = Bender(bender[0][0], bender[0][1], 0)
        # direction attribute
        self.inverse_direction = False
        # movements history
        self.history = []

    def toggle_inverse_direction(self):
        """ Toggle the inverse_direction attribute
        """
        self.inverse_direction = not self.inverse_direction

    def is_cell_reachable(self, line, column):
        """ Check if Bender can go on the cell

            Args:
                line -- int
                column -- int

            return True if Bender can go on the cell, else False
        """
        value = self.ground.get_cell(line, column)[0]
        if value == '#':
            return False
        if value == 'X' and not self.bender.drunk:
            return False
        elif value == 'X' and self.bender.drunk:
            # empty this cell
            self.ground.set_cell(line, column, '')
        return True

    def run(self):
        # continue while Bender is not dead
        while self.ground.get_cell(self.bender.line, self.bender.column)[0] != '$':
            # move to the next cell
            old_line = self.bender.line
            old_column = self.bender.column
            # first, start with the current blender's direction. If if doesn't work,
            # search for new direction
            search_new_direction = False
            # continue while can't move in the current direction
            while self.bender.line == old_line and self.bender.column == old_column:
                if self.DIRECTIONS[self.bender.direction] == 'SOUTH' \
                        and self.is_cell_reachable(self.bender.line+1, self.bender.column):
                    self.bender.line += 1
                elif self.DIRECTIONS[self.bender.direction] == 'EAST' \
                        and self.is_cell_reachable(self.bender.line, self.bender.column+1):
                    self.bender.column += 1
                elif self.DIRECTIONS[self.bender.direction] == 'NORTH' \
                        and self.is_cell_reachable(self.bender.line-1, self.bender.column):
                    self.bender.line -= 1
                elif self.DIRECTIONS[self.bender.direction] == 'WEST' \
                        and self.is_cell_reachable(self.bender.line, self.bender.column-1):
                    self.bender.column -= 1
                else:
                    # if it was the previous direction of Bender, reset direction
                    if not search_new_direction:
                        search_new_direction = True
                        self.bender.direction = 3 if self.inverse_direction else 0
                    else:
                        # check another direction
                        if self.inverse_direction:
                            self.bender.direction = (self.bender.direction - 1) % 4
                        else:
                            self.bender.direction = (self.bender.direction + 1) % 4

            # if cell has already been visited, with the same direction => LOOP
            if self.ground.get_cell(self.bender.line, self.bender.column) == self.bender.direction:
                print("LOOP")
                return
            # else, set the cell to visited
            self.ground.set_cell(self.bender.line, self.bender.column, visited=self.bender.direction)

            # push direction in history
            self.history.append(self.DIRECTIONS[self.bender.direction])

            # handle new cell
            cell_value = self.ground.get_cell(self.bender.line, self.bender.column)[0]
            if cell_value == 'B':
                self.bender.toggle_drunk()
            elif cell_value == 'I':
                self.toggle_inverse_direction()
            elif cell_value == 'T':
                # move to the other teleporter
                if self.bender.line == self.teleporter_a[0] and self.bender.column == self.teleporter_a[1]:
                    self.bender.line = self.teleporter_b[0]
                    self.bender.column = self.teleporter_b[1]
                else:
                    self.bender.line = self.teleporter_a[0]
                    self.bender.column = self.teleporter_a[1]
            elif cell_value == 'E':
                self.bender.direction = self.DIRECTIONS.index('EAST')
            elif cell_value == 'N':
                self.bender.direction = self.DIRECTIONS.index('NORTH')
            elif cell_value == 'S':
                self.bender.direction = self.DIRECTIONS.index('SOUTH')
            elif cell_value == 'W':
                self.bender.direction = self.DIRECTIONS.index('WEST')

        # print the path
        for direction in self.history:
            print(direction)



###
# MAIN CODE
###

# init the map with the inputs
nb_lines, nb_columns = map(int, input().split())
ground = Ground(nb_lines, nb_columns)
ground.init_ground([input() for _ in range(nb_lines)])

# init solution
solution = Solution(ground)
# run code
solution.run()
