# registers
a, b, c, d = [int(v) for v in input().split()]
# nb instructions
n = int(input())
# read the instructions
instructions = [''] * n
for i in range(n):
    instructions[i] = input().split()
# execute instructions
p = 0
while p < n:
    go_next = True
    if instructions[p][0] == "MOV":
        exec("%s = %s" % (instructions[p][1], instructions[p][2]))
    elif instructions[p][0] == "ADD":
        exec("%s = %s + %s" % (instructions[p][1], instructions[p][2], instructions[p][3]))
    elif instructions[p][0] == "SUB":
        exec("%s = %s - %s" % (instructions[p][1], instructions[p][2], instructions[p][3]))
    elif instructions[p][0] == "JNE":
        if eval("%s != %s" % (instructions[p][2], instructions[p][3])):
            p = int(instructions[p][1])
            go_next = False
    if go_next == True:
        # go next instruction
        p += 1
# print the registers values
print("%d %d %d %d" % (a, b, c, d))
