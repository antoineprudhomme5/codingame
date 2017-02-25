# number of floors
n = int(input())
# find x, where x*(x+1) / 2 == n and round it up
x = 0
while x*(x+1) / 2 < n:
    x += 1
print(x)
