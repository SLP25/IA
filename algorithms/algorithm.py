from abc import ABC, abstractmethod
from graph.graph import Graph
from graph.car import Car

class Algorithm(ABC):
    """
    An abstract class representing a search algorithm.

    The point of this class is to provide a common API
    that all algorithms must adhere to

    """
    @abstractmethod
    def search(self, graph:Graph,carN:int, cars:list[Car], end_nodes:list[tuple[int,int]]):
        """ Performs the search on the given graph

        Args:
            graph (Graph): the graph to search on
            cars (list): the list of cars to simulate
            end_nodes (list(str)): the list of all possible ending nodes

        Returns:
            A pair containing the cost of the solution and the path taken
        """
        pass