import sys
import math

boost_used = False
c_points = {}
max_dist = float("-Inf")

# game loop
while True:
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = map(int, input().split())
    opponent_x, opponent_y = map(int, input().split())

    thrust = 0 if next_checkpoint_angle > 90 or next_checkpoint_angle < -90 else 100

    # store all locations and store max distance
    key = "%d,%d" % (next_checkpoint_x, next_checkpoint_y)
    if key not in c_points:
        c_points[key] = True
        max_dist = max(max_dist, next_checkpoint_dist)
    elif not boost_used and next_checkpoint_dist >= max_dist and thrust != 0:
        thrust = "BOOST"
        boost_used = True

    print("%d %d %s" % (next_checkpoint_x, next_checkpoint_y, str(thrust)))
