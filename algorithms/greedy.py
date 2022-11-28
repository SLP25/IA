from graph.graph import Graph
from graph.node import Node
from .algorithm import Algorithm

class GREEDY(Algorithm):
    """
    Class implementing a breath-first-search algorithm
    """
    def search(self, graph:Graph, start_node:Node, end_nodes:list):
        """Searches the graph startign on start_node until reaching one of the end_nodes using the greedy algorithm

        Args:
            graph (Graph): the graph to search the path in
            start_node (Node): the node to start the search in 
            end_nodes ([(Int,Int)]): the list of all position corresponding to end Nodes

        Returns:
            (int,[Node]): pair with the total distance travels and the path taken to reach the end
        """
        current = start_node
        previous = {}
        previous[current] = None
        total = 0
        iteration=2**6
        while (current.x,current.y) not in end_nodes:
            (next, next_cost) = min(graph.adjList[current], key = lambda nc: nc[0].getEstimate(end_nodes))
            previous[next] = current
            total += next_cost
            current = next
        return (total,self.__reconstruct_path__(previous, current))


    def __reconstruct_path__(self, previous:dict, end:Node):
        """reconstructs the path the algorithm took from the start up to the end

        Args:
            previous (dict): the dictionary of each node and the one it came from
            end (Node): the node it finished on

        Returns:
            list: the path the algorithm took from the start up to the end
        """
        path = []

        while end != None:
            path.insert(0, end)
            end = previous[end]

        return path