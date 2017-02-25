# http://oeis.org/A000002
# http://mathworld.wolfram.com/KolakoskiSequence.html

n = int(input())
a, b = input().split()
v_a, v_b = int(a), int(b)

blocks = a * v_a

if v_a == 1:
    i = 2
    blocks += b * v_b
else:
    i = 1

len_blocks = len(blocks)

while len_blocks < n:
    m = int(blocks[i])
    # turn of A
    if i % 2 == 0:
        blocks += m * a
    # turn of B
    else:
        blocks += m * b

    len_blocks += m
    i += 1

print(blocks[:n])
