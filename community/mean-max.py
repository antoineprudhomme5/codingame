import sys
import math

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, p):
        """ Return the eucliean distance between 2 Point
        """
        return math.sqrt((self.x-p.x)**2 + (self.y-p.y)**2)

class Unit(Point):
    def __init__(self, unit_id, x, y, vx, vy, radius):
        Point.__init__(self, x, y)
        self.unit_id = unit_id
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

def closer(origin, destinations):
    response = None
    response_distance = float('+Inf')
    for destination in destinations:
        dist = origin.distance(destination)
        if dist < response_distance:
            response = destination
            response_distance = dist
    return response, response_distance

def circle_collision(circle1, circle2):
    return circle2.distance(circle2) < (circle1.radius + circle2.radius)

def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    # colinear
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def on_segment(p, q, r):
    return (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and
        q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y))

def do_intersect(p1, q1, p2, q2):
    # Find the four orientations needed for general and
    # special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    # general case
    if o1 != o2 and o3 != o4:
        return True
    # Special Cases
    # p1, q1 and p2 are colinear and p2 lies on segment p1q1
    if o1 == 0 and on_segment(p1, p2, q1): return True
    # p1, q1 and p2 are colinear and q2 lies on segment p1q1
    if o2 == 0 and on_segment(p1, q2, q1): return True
    # p2, q2 and p1 are colinear and p1 lies on segment p2q2
    if o3 == 0 and on_segment(p2, p1, q2): return True
    # p2, q2 and q1 are colinear and q1 lies on segment p2q2
    if o4 == 0 and on_segment(p2, q1, q2): return True
    # Doesn't fall in any of the above cases
    return False

def collide(u1, u2, target):
    # draw path of u2 given his current position and speed
    end = Point(0, 0)
    if u2.vx != 0:
        if u2.vx > 0:
            end.x = math.floor((3000-u2.x)/u2.vx)
        else:
            end.x = math.floor((-3000-u2.x)/u2.vx)
    if u2.vy != 0:
        if u2.vy > 0:
            end.y = math.floor((3000-u2.y)/u2.vy)
        else:
            end.y = math.floor((-3000-u2.y)/u2.vy)

    return do_intersect(u1, target, u2, end)

def is_path_blocked(origin, units, target):
    for unit in units:
        if collide(origin, unit, target):
            return True
    return False

def wreck_heuristic(reapers, wreck, tankers, destroyers, doofs):
    # water quantity
    value = wreck.quantity * -1000
    # +5000 if an ennemy is closer, else -5000
    me_dist = reapers[0].distance(wreck)
    enemy_dist = min(reapers[1].distance(wreck), reapers[2].distance(wreck))
    value += 5000 if enemy_dist < me_dist else -5000
    value += me_dist
    # check if the path to this wreck is blocked
    if is_path_blocked(reapers[0], reapers[1:] + tankers + destroyers + doofs, wreck):
        value += 10000
    return value

def wrecks_heuristic(reapers, wrecks, tankers, destroyers, doofs):
    best_wreck = None
    best_heuristic = float('+Inf')
    for wreck in wrecks:
        heuristic = wreck_heuristic(reapers, wreck, tankers, destroyers, doofs)
        if heuristic < best_heuristic:
            best_heuristic = heuristic
            best_wreck = wreck
    return best_wreck, best_heuristic

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

    for _ in range(int(input())):
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

    # DESTROYER
    # if close enought, throw grenade to tanker
    # else, chase the closest tanker to my reaper ?
    DESTROYER = "WAIT"
    closest_wreck, closest_wreck_dist = wrecks_heuristic(reapers, wrecks, tankers, destroyers, doofs)
    closer_tanker, closer_tanker_dist = closer(destroyers[0], tankers)
    if closer_tanker_dist < 2000 and rages[0] >= 60:
        DESTROYER = "SKILL %d %d" % (closer_tanker.x+50, closer_tanker.y+50)
    elif closest_wreck_dist < closer_tanker_dist:
        DESTROYER = "%d %d %d" % (closest_wreck.x, closest_wreck.y, 300)
    elif closer_tanker:
        DESTROYER = "%d %d %d" % (closer_tanker.x, closer_tanker.y, 300)

    # REAPER
    # if there is a wreck, go
    # else, follow the destroyer
    REAPER = "WAIT"
    closest_wreck, _ = wrecks_heuristic(reapers, wrecks, tankers, destroyers, doofs)
    if closest_wreck:
        REAPER = "%d %d %d" % (closest_wreck.x, closest_wreck.y, 300)
    elif DESTROYER != "WAIT":
        REAPER = "%d %d %d" % (closer_tanker.x, closer_tanker.y, 250)

    # DOOF
    # block best ennemy reaper
    DOOF = "%d %d %d" % (reapers[0].x, reapers[1 if scores[1]>scores[2] else 2].y, 300)

    print(REAPER)
    print(DESTROYER)
    print(DOOF)
