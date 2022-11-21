from .node import Node

class Graph:
    """
        The graph to represent a circuit
    """
    def __init__(self, adjList:dict = {}, nodes:set = set(),
                 starts:list = [], finishes:list = [], directed:bool = True):
        """create a new graph instance

        Args:
            adjList (dict, optional): the list of adjacent node to each node. Defaults to {}.
            nodes (set, optional): a set of all nodes in the graph. Defaults to set().
            starts (list, optional): a list of all position that are starts of the circuit. Defaults to [].
            finishes (list, optional): a list of all position that are finishes of the circuit. Defaults to [].
            directed (bool, optional): wether the graph is directed. Defaults to True.
        """
        self.adjList = {}
        self.nodes = set()
        self.directed = True
        self.starts = []
        self.finishes =  []

    def add_edge(self, src_node:Node, dest_node:Node, cost:int):
        """creates a new connection between 2 nodes with a given weight

        Args:
            src_node (Node): the starting node to add the edge to
            dest_node (Node): the destination node to add the edge to
            cost (int): the weight of the edge between those nodes
        """
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

    def add_start(self, x:int, y:int):
        """adds a new position as a starrting point of the circuit

        Args:
            x (int): the x position of the start
            y (int): the y position of the start
        """
        self.starts.append((x,y))

    def add_finish(self, x:int, y:int):
        """adds a new position as a finishing point of the circuit

        Args:
            x (int): the x position of the finish
            y (int): the y position of the finish
        """
        self.finishes.append((x,y))