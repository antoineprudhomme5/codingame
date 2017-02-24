class Node():
    def __init__(self, key=None, next=None):
        self.key = key
        self.next = next

def insert_node(head, data):
    if head is None:
        head = Node(key=data)
    else:
        head.next = insert_node(head.next, data)
    return head

d = {}
n = int(input())
stones = 0
# read the stones level
for i in input().split():
    i = int(i)
    if i in d:
        d[i] += 1
    else:
        d[i] = 1
# build a linked list from the dict
levels = sorted(d.keys())
levels_list = None
for i in range(0, len(levels)):
    levels_list = insert_node(levels_list, levels[i])
# go throught the list
while levels_list != None:
    # if we cant combine stones with this level
    if d[levels_list.key] < 2:
        # count the stones and remove this node from the linked list
        stones += d[levels_list.key]
        levels_list = levels_list.next
    else:
        # count how many stones we can combine
        to_combine = d[levels_list.key]
        if to_combine % 2 == 1:
            to_combine -= 1
            stones += 1
        # update the next level in dict
        if levels_list.key + 1 in d:
            d[levels_list.key + 1] += to_combine // 2
        else:
            d[levels_list.key + 1] = to_combine // 2
        # update the list to go to the next level
        if levels_list.next != None and levels_list.next.key == (levels_list.key + 1):
            levels_list = levels_list.next
        else:
            levels_list.key += 1

print(stones)
