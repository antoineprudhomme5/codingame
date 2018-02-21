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

    def on_segment(self, p, r):
        """
            Check if the Point is on segment 'pr'
        """
        return (self.x <= max(p.x, r.x) and self.x >= min(p.x, r.x) and
            self.y <= max(p.y, r.y) and self.y >= min(p.y, r.y))

    @staticmethod
    def orientation(p, q, r):
        """
            0: colinear
            1: clockwise
            2: counterclockwise
        """
        val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
        if val == 0: return 0
        return 1 if val > 0 else 2

class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dot(self, v):
        return (self.x*v.x)+(self.y*v.y)

    def magnitude(self):
        return math.sqrt((self.x)**2 + (self.y)**2)

    def angle(self, v):
        """ Return the angle in radian
        """
        return math.acos(self.dot(v) / (self.magnitude()*v.magnitude()))

class Unit(Point):
    def __init__(self, unit_id, x, y, vx, vy, radius):
        Point.__init__(self, x, y)
        self.unit_id = unit_id
        self.speed = Vector(vx, vy)
        self.radius = radius

    def intersect(self, unit):
        return self.distance(unit) < (self.radius + unit.radius)

    def is_in(self, target):
        """ Check if the center of this Unit is in the radius of the target
        """
        return self.distance(target) < target.radius

    def will_collide_unit(self, unit, target):
        unit_target = Point(0, 0)
        if unit.speed.x > 0:
            unit_target.x = math.floor((3000-unit.x)/unit.speed.x)
        elif unit.speed.x < 0:
            unit_target.x = math.floor((-3000-unit.x)/unit.speed.x)
        if unit.speed.y > 0:
            unit_target.y = math.floor((3000-unit.y)/unit.speed.y)
        elif unit.speed.y < 0:
            unit_target.y = math.floor((-3000-unit.y)/unit.speed.y)

        if unit_target.x == 0 or unit_target.y == 0:
            return False
        return self.do_intersect(target, unit, unit_target)

    def will_collide_units(self, units, target):
        for unit in units:
            if self.will_collide_unit(unit, target):
                return True
        return False

    def do_intersect(self, q1, p2, q2):
        # Find the four orientations needed for general and
        # special cases
        o1 = Point.orientation(self, q1, p2)
        o2 = Point.orientation(self, q1, q2)
        o3 = Point.orientation(p2, q2, self)
        o4 = Point.orientation(p2, q2, q1)
        # general case
        if o1 != o2 and o3 != o4:
            return True
        # Special Cases
        # self, q1 and p2 are colinear and p2 lies on segment p1q1
        if o1 == 0 and p2.on_segment(self, q1): return True
        # self, q1 and p2 are colinear and q2 lies on segment p1q1
        if o2 == 0 and q2.on_segment(self, q1): return True
        # p2, q2 and self are colinear and self lies on segment p2q2
        if o3 == 0 and self.on_segment(p2, q2): return True
        # p2, q2 and q1 are colinear and q1 lies on segment p2q2
        if o4 == 0 and q1.on_segment(p2, q2): return True
        # Doesn't fall in any of the above cases
        return False

    def calculate_next_point(self):
        return Point(self.x + self.speed.x, self.y + self.speed.y)

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
        self.max_throttle = 300

    def throttle(self, target, distance):
        thrust = 300
        if distance < 2000:
            thrust = 150
        elif distance < target.radius:
            thrust = 50
        return thrust

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

def wreck_heuristic(reapers, wreck, tankers, destroyers, doofs):
    # water quantity
    value = wreck.quantity * -1000
    # +5000 if an ennemy is closer, else -5000
    me_dist = reapers[0].distance(wreck)
    enemy_dist = min(reapers[1].distance(wreck), reapers[2].distance(wreck))
    value += 5000 if enemy_dist < me_dist else -5000
    value += me_dist
    # check if the path to this wreck is blocked
    if reapers[0].will_collide_units(reapers[1:] + tankers + destroyers + doofs, wreck):
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
    # find the closest tanker to
    DESTROYER = "WAIT"
    closest_tanker, closest_tanker_dist = closer(reapers[0], tankers)
    if closest_tanker_dist < 2000 and rages[0] >= 60:
        DESTROYER = "SKILL %d %d" % (closest_tanker.x+50, closest_tanker.y+50)
    elif closest_tanker:
        DESTROYER = "%d %d %d" % (closest_tanker.x, closest_tanker.y, destroyers[0].throttle(closest_tanker, closest_tanker_dist))

    # REAPER
    # if there is a wreck, go
    # else, follow the destroyer
    REAPER = "WAIT"
    closest_wreck, closest_wreck_dist  = wrecks_heuristic(reapers, wrecks, tankers, destroyers, doofs)
    if closest_wreck:
        throttle = reapers[0].throttle(closest_wreck, closest_wreck_dist)
        if throttle > 0:
            REAPER = "%d %d %d" % (closest_wreck.x, closest_wreck.y, throttle)
    elif DESTROYER != "WAIT":
        throttle = reapers[0].throttle(destroyers[0], destroyers[0].distance(reapers[0]))
        if throttle > 0:
            REAPER = "%d %d %d" % (destroyers[0].x, destroyers[0].y, throttle)

    # DOOF
    DOOF = "%d %d %d" % (reapers[1 if scores[1]>scores[2] else 2].x, reapers[1 if scores[1]>scores[2] else 2].y, 300)

    print(REAPER)
    print(DESTROYER)
    print(DOOF)
