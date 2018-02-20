import sys
import math

class Unit(object):
    def __init__(self, unit_id, x, y, vx, vy, radius, mass):
        self.unit_id = unit_id
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.mass = mass

class Reaper(Unit):
    def __init__(self, unit_id, x, y, vx, vy, radius, mass, player_id, score):
        Unit.__init__(self, unit_id, x, y, vx, vy, radius, mass)
        self.player_id = player_id
        self.score = score

class Wreck(Unit):
    def __init__(self, unit_id, x, y, vx, vy, radius, mass, extra):
        Unit.__init__(self, unit_id, x, y, vx, vy, radius, mass)
        self.extra = extra

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def heuristic(reapers, wreck):
    """ simple heuristic: distance
    """
    d1 = distance(reapers[1].x, reapers[1].y, wreck.x, wreck.y)
    d2 = distance(reapers[2].x, reapers[2].y, wreck.x, wreck.y)
    return (-1)*d1*d2

NB_REAPERS = 3

# game loop
while True:
    scores = [int(input()) for _ in range(NB_REAPERS)]
    rages = [int(input()) for _ in range(NB_REAPERS)]
    reapers = [None for _ in range(NB_REAPERS)]
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
            reapers[player_id] = Reaper(unit_id, x, y, vx, vy, radius, mass, player_id, scores[player_id])
        else:
            wrecks.append(Wreck(unit_id, x, y, vx, vy, radius, mass, extra))

    for wreck in wrecks:
        wreck_heuristic = heuristic(reapers, wreck)
        if wreck_heuristic < next_wreck_heuristic:
            next_wreck_heuristic = wreck_heuristic
            next_wreck = wreck

    if next_wreck.x == reapers[0].x and next_wreck.y == reapers[0].y:
        print("WAIT")
    else:
        print("%d %d %d" % (wreck.x, wreck.y, 300))
    print("WAIT")
    print("WAIT")
