import sys
import math

# game loop
while True:
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = map(int, input().split())
    opponent_x, opponent_y = map(int, input().split())
    thrust = 100
    if abs(next_checkpoint_angle) > 90:
        thrust = 0
    print("%d %d %d" % (next_checkpoint_x, next_checkpoint_y, thrust))
