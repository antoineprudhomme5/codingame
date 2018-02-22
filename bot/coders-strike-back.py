import sys
import math

boost_used = False

# game loop
while True:
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = map(int, input().split())
    opponent_x, opponent_y = map(int, input().split())

    if not boost_used and next_checkpoint_angle < 60 and next_checkpoint_dist > 500:
        boost_used = True
        print("%d %d BOOST" % (next_checkpoint_x, next_checkpoint_y))
    else:
        thrust = 100
        if abs(next_checkpoint_angle) > 90:
            thrust = 0
        print("%d %d %d" % (next_checkpoint_x, next_checkpoint_y, thrust))
