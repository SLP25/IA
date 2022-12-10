import itertools
from algorithms.dfs import DFS
from graph.graph import Graph
from graph.node import Node
from graph.car import Car
from .algorithm import Algorithm


class ITERATIVE_DFS(Algorithm):
    """
    Class implementing an iterative depth-first-search algorithm
    """
    
    def search(self, graph:Graph,carN:int, cars:list[Car], end_nodes:list[tuple[int,int]]):
        """
            Searches the graph startig in the car in position carN last node until reaching one of the end_nodes using the iterative dfs algorithm

        Args:
            graph (Graph): the graph to search the path on
            carN (int): the position of the car to search a path to
            cars (list[Car]): the list of all cars
            end_nodes (list[tuple[int,int]]): the list of the positions of the coordenates a car needs to reach
            
        """
        dfs = DFS()
        
        for i in itertools.count(1,1):
            dfs.search(graph,carN,cars,end_nodes, i)
            if cars[carN].cost!=-1:
                break
