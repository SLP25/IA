from .node import Node

class Graph:
    def __init__(self, adjList = {}, nodes = set(),
                 starts = [], finishes = [], directed = True):
        self.adjList = {}
        self.nodes = set()
        self.directed = True
        self.starts = []
        self.finishes =  []

    def add_edge(self, src_node, dest_node, cost):
        if src_node not in self.nodes:
            self.nodes.add(src_node)

        if dest_node not in self.nodes:
            self.nodes.add(dest_node)

        if src_node not in self.adjList.keys():
            self.adjList[src_node] = set()

        if dest_node not in self.adjList.keys():
            self.adjList[dest_node] = set()

        self.adjList[src_node].add((dest_node, cost))

        if not self.directed:
            self.adjList[dest_node].add((src_node, cost))

    def add_start(self, x, y):
        self.starts.append((x,y))

    def add_finish(self, x, y):
        self.finishes.append((x,y))