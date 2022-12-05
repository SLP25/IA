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
        Searches the graph startign on start_node until reaching
        one of the end_nodes using the iterative dfs algorithm
        
        Args:
            graph (Graph): the graph to search the path in
            start_node (Node): the node to start the search in 
            end_nodes ([(Int,Int)]): the list of all position corresponding to end Nodes
        """
        dfs = DFS()
        
        for i in itertools.count():
            aux = dfs.search(graph,carN,cars,end_nodes, i)
            
            if cars[carN].cost!=-1:
                return aux