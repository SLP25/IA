import itertools
from algorithms.dfs import DFS
from graph.graph import Graph
from graph.node import Node
from .algorithm import Algorithm


class ITERATIVE_DFS(Algorithm):
    """
    Class implementing an iterative depth-first-search algorithm
    """
    
    def search(self, graph:Graph, start_node:Node, end_nodes:list):
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
            aux = dfs.search(graph, start_node, end_nodes, i)
            
            if aux != None:
                return aux