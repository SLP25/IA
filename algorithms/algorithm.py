from abc import ABC, abstractmethod


class Algorithm(ABC):
    """
    An abstract class representing a search algorithm.

    The point of this class is to provide a common API
    that all algorithms must adhere to

    """
    @abstractmethod
    def search(self, graph, start_node, end_nodes):
        """ Performs the search on the given graph

        Args:
            graph (Graph): the graph to search on
            start_node (str): the starting node of the search
            end_nodes (list(str)): the list of all possible ending nodes

        Returns:
            A pair containing the cost of the solution and the path taken
        """
        pass