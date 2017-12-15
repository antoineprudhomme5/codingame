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
        parents = {}
        visited = {}
        gateways = []

        queue = deque()
        next_queue = deque()
        queue.append(self.agent)

        while len(queue):
            current = queue.pop()

            if current in self.gateways:
                gateways.append(current)

            for child in self.graph[current]:
                if child not in visited:
                    visited[child] = True
                    next_queue.append(child)
                    parents[child] = current

            # if the current node level is empty and still not found
            # gateways, children nodes becomes parent nodes and continue to search
            if len(gateways) == 0 and len(queue) == 0:
                queue = next_queue
                next_queue = deque()

        to_protect = gateways[0]
        for i in range(1, len(gateways)):
            if len(self.gateway_children(parents[gateways[i]])) > len(self.gateway_children(parents[to_protect])):
                to_protect = gateways[i]

        self.graph[to_protect].remove(parents[to_protect])
        self.graph[parents[to_protect]].remove(to_protect)
        return "%d %d" % (parents[to_protect], to_protect)

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
