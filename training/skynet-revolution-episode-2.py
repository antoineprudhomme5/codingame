from collections import deque
import sys
class Network(object):
    """ Graph that represent the skynet's network

        Attributes:
            nb_nodes:   the total number of nodes in the level, including the gateways
            nb_links:   the number of links
            nb_exits:   the number of exit gateways
            graph:      network nodes and links
            gateways:   store gateways in a dic (access in constant time)
            agent:      current agent's location (node index)
    """
    def __init__(self, nb_nodes, nb_links, nb_exits):
        self.nb_nodes = nb_nodes
        self.nb_links = nb_links
        self.nb_exits = nb_exits
        self.graph = {}
        self.gateways = {}
        self.agent = None

        for i in range(nb_nodes):
            self.graph[i] = []

    def add_link(self, a, b):
        self._add_child(a, b)
        self._add_child(b, a)

    def add_gateway(self, n):
        self.gateways[n] = True

    def gateway_children(self, node):
        return [n for n in self.graph[node] if (n in self.gateways)]

    def _add_child(self, parent, child):
        self.graph[parent].append(child)

    def next_link_to_cut(self):
        """ find the closest gateway to the agent node and cut the link
            last link of the path (from the last normal node to the gateway)

            use BFS to find the closest gateway

            they can be any gateways at the same level !!!
            => (test case 2). In this case, choose the "less protected" gateway
            (with the most path to it)
        """
        visited = {}
        parents = {}
        lonely_gateways = []
        depth = 1

        queue = deque()
        next_queue = deque()
        queue.append(self.agent)

        while len(queue):
            current = queue.pop()

            print("-----------", file=sys.stderr)
            print("current: %d" % (current), file=sys.stderr)
            print("depth: %d" % (depth), file=sys.stderr)

            gateways = []
            for child in self.graph[current]:
                if child not in visited:
                    if child not in parents:
                        parents[child] = current
                    if child in self.gateways:
                        gateways.append(child)
                    else:
                        visited[child] = True
                        next_queue.append(child)

            print("gateways: " + str(gateways), file=sys.stderr)

            if len(gateways):
                if (depth == 1) or (len(gateways) > 1):
                    print("priority : %d %d" % (gateways[0], current), file=sys.stderr)
                    self.graph[gateways[0]].remove(current)
                    self.graph[current].remove(gateways[0])
                    return "%d %d" % (current, gateways[0])
                else:
                    # there is only one gateway, but at depth > 1
                    lonely_gateways += gateways

            if len(queue) == 0:
                queue = next_queue
                next_queue = deque()
                depth += 1

        print("default : %d %d" % (lonely_gateways[0], parents[lonely_gateways[0]]), file=sys.stderr)
        self.graph[lonely_gateways[0]].remove(parents[lonely_gateways[0]])
        self.graph[parents[lonely_gateways[0]]].remove(lonely_gateways[0])
        return "%d %d" % (parents[lonely_gateways[0]], lonely_gateways[0])

nb_nodes, nb_links, nb_exits = [int(i) for i in input().split()]
network = Network(nb_nodes, nb_links, nb_exits)

# read links
for _ in range(nb_links):
    n1, n2 = [int(j) for j in input().split()]
    network.add_link(n1, n2)
# read gateways
for _ in range(nb_exits):
    network.add_gateway(int(input()))

# game loop
while True:
    network.agent = int(input())
    print(network.next_link_to_cut())
