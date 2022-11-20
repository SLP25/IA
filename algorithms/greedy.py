from graph.graph import Graph
from graph.node import Node
from .algorithm import Algorithm

class GREDDY(Algorithm):
    """
    Class implementing a breath-first-search algorithm
    """
    def search(self, graph, start_node, end_nodes):
        current = start_node
        previous = {}
        previous[current] = None
        total = 0    
        while (current.x,current.y) not in end_nodes:
            (next, next_cost) = min(graph.adjList[current], key = lambda nc: nc[0].getEstimate(end_nodes))
            previous[next] = current
            total += next_cost
            current = next
        return (total,self.__reconstruct_path__(previous, current))


    def __reconstruct_path__(self,previous, end):
        path = []

        while end != None:
            path.insert(0, end)
            end = previous[end]

        return path