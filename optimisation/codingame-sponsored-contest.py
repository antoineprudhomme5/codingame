import sys

max_j = int(input())
max_i = int(input())
nb_coordinates_per_tour = int(input())

print("%d %d %d" % (max_j,
                    max_i,
                    nb_coordinates_per_tour), file=sys.stderr)

# game loop
while True:
    c1 = input()
    c2 = input()
    c3 = input()
    c4 = input()

    print("%s %s %s %s" % (c1, c2, c3, c4), file=sys.stderr)

    for i in range(nb_coordinates_per_tour):
        i, j = map(int, input().split())
        print("%d %d" % (i, j), file=sys.stderr)

    # print("A, B, C, D or E")
    print("A")
