from node import Node

class Graph:
    def __init__(self, adjList = {}, nodes = [], estimates = {}, directed = False):
        self.adjList = adjList
        self.nodes = nodes
        self.directed = directed
        self.estimates = estimates

    def add_edge(self, src_node, dest_node, cost):
        n1 = Node(src_node)
        n2 = Node(dest_node)

        if n1 not in self.nodes:
            n1.setId(len(self.nodes))
            self.nodes.append(n1)

        if n2 not in self.nodes:
            n2.setId(len(self.nodes))
            self.nodes.append(n2)

        if src_node not in self.adjList.keys():
            self.adjList[src_node] = set()

        if dest_node not in self.adjList.keys():
            self.adjList[dest_node] = set()

        self.adjList[src_node].add((dest_node, cost))

        if not self.directed:
            self.adjList[dest_node].add((src_node, cost))

    def add_estimate(self, node, value):
        self.estimates[node] = value