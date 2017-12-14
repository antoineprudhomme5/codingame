from collections import deque

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

    def add_link(self, a, b):
        self._add_child(a, b)
        self._add_child(b, a)

    def add_gateway(self, n):
        self.gateways[n] = True

    def _add_child(self, parent, child):
        if parent in self.graph:
            self.graph[parent].append(child)
        else:
            self.graph[parent] = [child]

    def next_link_to_cut(self):
        """ find the closest gateway to the agent node and cut the link
            last link of the path (from the last normal node to the gateway)

            use BFS to find the closest gateway

            they can be any gateways at the same level !!!
            => (test case 2). In this case, choose the "less protected" gateway
            (with the most path to it)
        """
        queue = deque()
        queue.append(self.agent)
        parents = {}
        visited = {}

        while len(queue):
            current = queue.pop()
            # if it's a gateway, remove and return the link to this gateway
            if current in self.gateways:
                self.graph[current].remove(parents[current])
                self.graph[parents[current]].remove(current)
                return "%d %d" % (parents[current], current)
            # else, add unvisited children
            for child in self.graph[current]:
                if child not in visited:
                    visited[child] = True
                    queue.append(child)
                    parents[child] = current

        return None

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
