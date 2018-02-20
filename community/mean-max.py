import sys
import math

class Unit(object):
    def __init__(self, unit_id, x, y, vx, vy, radius):
        self.unit_id = unit_id
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius

class WaterCarrier(object):
    def __init__(self, quantity):
        self.quantity = quantity

class Wreck(Unit, WaterCarrier):
    def __init__(self, unit_id, x, y, vx, vy, radius, extra):
        Unit.__init__(self, unit_id, x, y, vx, vy, radius)
        WaterCarrier.__init__(self, extra)

class Vehicule(Unit):
    def __init__(self, unit_id, x, y, vx, vy, radius, mass):
        Unit.__init__(self, unit_id, x, y, vx, vy, radius)
        self.mass = mass

class Looter(Vehicule):
    def __init__(self, unit_id, x, y, vx, vy, radius, mass):
        Vehicule.__init__(self, unit_id, x, y, vx, vy, radius, mass)

class Tanker(Vehicule, WaterCarrier):
    def __init__(self, unit_id, x, y, vx, vy, radius, mass, extra, extra_2):
        Vehicule.__init__(self, unit_id, x, y, vx, vy, radius, mass)
        WaterCarrier.__init__(self, extra)
        self.water_capacity = extra_2

class Reaper(Looter):
    def __init__(self, unit_id, x, y, vx, vy, radius, mass):
        Looter.__init__(self, unit_id, x, y, vx, vy, radius, mass)

class Destroyer(Looter):
    def __init__(self, unit_id, x, y, vx, vy, radius, mass):
        Looter.__init__(self, unit_id, x, y, vx, vy, radius, mass)

class Doof(Looter):
    def __init__(self, unit_id, x, y, vx, vy, radius, mass):
        Looter.__init__(self, unit_id, x, y, vx, vy, radius, mass)


def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def heuristic(reapers, wreck):
    """ simple heuristic: distance
    """
    d1 = distance(reapers[1].x, reapers[1].y, wreck.x, wreck.y)
    d2 = distance(reapers[2].x, reapers[2].y, wreck.x, wreck.y)
    return (-1)*d1*d2

NB_PLAYERS = 3

# game loop
while True:
    scores = [int(input()) for _ in range(NB_PLAYERS)]
    rages = [int(input()) for _ in range(NB_PLAYERS)]

    reapers = [None for _ in range(NB_PLAYERS)]
    doofs = [None for _ in range(NB_PLAYERS)]
    destroyers = [None for _ in range(NB_PLAYERS)]
    tankers = []
    wrecks = []

    next_wreck_heuristic = float('+Inf')
    next_wreck = None

    unit_count = int(input())
    for _ in range(unit_count):
        unit_id, unit_type, player_id, mass, radius, x, y, vx, vy, extra, extra_2 = input().split()
        unit_id = int(unit_id)
        unit_type = int(unit_type)
        player_id = int(player_id)
        mass = float(mass)
        radius = int(radius)
        x = int(x)
        y = int(y)
        vx = int(vx)
        vy = int(vy)
        extra = int(extra)
        extra_2 = int(extra_2)

        if unit_type == 0:
            reapers[player_id] = Reaper(unit_id, x, y, vx, vy, radius, mass)
        elif unit_type == 1:
            destroyers[player_id] = Destroyer(unit_id, x, y, vx, vy, radius, mass)
        elif unit_type == 2:
            doofs[player_id] = Doof(unit_id, x, y, vx, vy, radius, mass)
        elif unit_type == 3:
            tankers.append(Tanker(unit_id, x, y, vx, vy, radius, mass, extra, extra_2))
        else:
            wrecks.append(Wreck(unit_id, x, y, vx, vy, radius, extra))

    for wreck in wrecks:
        wreck_heuristic = heuristic(reapers, wreck)
        if wreck_heuristic < next_wreck_heuristic:
            next_wreck_heuristic = wreck_heuristic
            next_wreck = wreck

    print("%d %d %d" % (next_wreck.x, next_wreck.y, 300) if next_wreck else "WAIT")
    print("%d %d %d" % (next_wreck.x, next_wreck.y, 300) if next_wreck else "WAIT")
    print("%d %d %d" % (next_wreck.x, next_wreck.y, 300) if next_wreck else "WAIT")
