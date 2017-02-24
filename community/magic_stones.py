d = {}
n = int(input())
# read the stones level
for i in input().split():
    i = int(i)
    if i in d:
        d[i] += 1
    else:
        d[i] = 1

stones = 0
print(d)
# store levels here, because new levels can be added dynamically
levels = sorted(d)
nb_levels = len(levels)
level_index = 0
# while there are levels to checks
while level_index < nb_levels:
    level = levels[level_index]
    # how many stones of this level can we combine ?
    to_combine = d[level]
    if to_combine % 2 == 1:
        to_combine -= 1
        stones += 1
    # search the level of the final stone
    final_level = level
    while to_combine > 1:
        to_combine /= 2
        final_level += 1
    # increment or create the final level in the dict
    if final_level in d:
        d[final_level] += 1
    else:
        d[final_level] = 1
        levels = sorted(d)
        nb_levels += 1
    level_index += 1

print(stones)
