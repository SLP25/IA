from algorithms.algorithm import Algorithm
from graph.graph import Graph
from graph.node import Node
import random
from graph.car import Car

class DFS(Algorithm):
    """
    Class implementing a depth-first-search algorithm
    """
    def search(self, graph:Graph,carN:int, cars:list[Car], end_nodes:list[tuple[int,int]], radius:int = 1e9):
        """Searches the graph startign on start_node until reaching one of the end_nodes using the dfs algorithm

        Args:
            graph (Graph): the graph to search the path in
            start_node (Node): the node to start the search in 
            end_nodes ([(Int,Int)]): the list of all position corresponding to end Nodes
            radius (int): the depth of the recursion allowed

        Returns:
            (int,[Node]): pair with the total distance travels and the path taken to reach the end
        """
        r=None
        itI=0
        car=cars[carNumber]
        while r==None:
            start_node=car.getLastNode()
            r=self.__search_aux__(graph,start_node, carNumber,cars, end_nodes, set(), radius,itI)
            itI+=1
            
        c,p=r
        for i in range(itI-1):
            c+=1
            p.insert(0,start_node)
        car.cost=c
        car.setPath(p)
            

    def __search_aux__(self, graph:Graph, start_node:Node,carN:int,cars:list[Car],end_nodes:list, visited:set, radius:int,it:int):
        """Auxiliary method for the main search method

        Args:
            graph (Graph): the graph to search on
            start_node (str): the starting/current node of the search
            end_nodes (list(str)): the list with all possible ending nodes
            visited (list(str)): the list of all nodes already visited
            radius (int): the depth of the recursion allowed

        Returns:
            A pair containing the cost and path taken in the found solution
        """
        visited.add(start_node)
        
        if (start_node.x, start_node.y) in end_nodes:
            return (0, [])
        
        if radius == 0:
            return None

        #for each node adjacent to current node
        for (node, cost) in graph.adjList[start_node]:
            # We don't visit a node twice
            if node not in visited and not any(c.colides(start_node.coords(),node.coords(),it) for c in cars[:carN]):
                res = self.__search_aux__(graph, node,carN,cars, end_nodes, visited, radius - 1,it+1)

                if res != None:
                    res[1].insert(0, node)
                    return (res[0] + cost, res[1])

        return None
