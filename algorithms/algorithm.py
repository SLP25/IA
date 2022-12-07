from abc import ABC, abstractmethod
from graph.graph import Graph
from graph.car import Car
from graph.node import Node
class Algorithm(ABC):
    """
    An abstract class representing a search algorithm.

    The point of this class is to provide a common API
    that all algorithms must adhere to

    """
    @abstractmethod
    def search(self, graph:Graph,carN:int, cars:list[Car], end_nodes:list[tuple[int,int]]):
        """searches the path in a graph from a car postion to one of the end_nodes 
           this method is supposted to be implemented acording to the algorithm being defined
           this method must take into cosideration the path taken by the other cars(one with a number smaller than the current)
           The cars should ot be able to be in the same place simultaneous (except for the start and finish)

        Args:
            graph (Graph): the graph to search the path on
            carN (int): the position of the car to search a path to
            cars (list[Car]): the list of all cars
            end_nodes (list[tuple[int,int]]): the list of the positions of the coordenates a car needs to reach
        """
        pass

        
    def __reconstruct_path__(self,node:tuple[Node,int],parents:dict)->list[Node]:
        """reconstruct te path taken by a car given the last node,iteration and a dictionary with the parent of each node iteration pair

        Args:
            node (tuple[Node,int]): a pair of Node iteration
            parents (dict): the dictionary with the parent of each node iteration pair

        Returns:
            list[Node]: a list with all nodes the car traveled throw
        """
        path = []
        prev=node
        while prev != None:
            path.insert(0, prev[0])
            prev=parents[prev]
        return path