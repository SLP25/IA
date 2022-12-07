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
        """
            Searches the graph startig in the car in position carN last node until reaching one of the end_nodes using the dfs algorithm

        Args:
            graph (Graph): the graph to search the path on
            carN (int): the position of the car to search a path to
            cars (list[Car]): the list of all cars
            end_nodes (list[tuple[int,int]]): the list of the positions of the coordenates a car needs to reach
            radius (int): the depth of the recursion allowed
        """
        r=None
        itI=0
        car=cars[carN]
        while r==None:
            start_node=car.getLastNode()
            r=self.__search_aux__(graph,start_node, carN,cars, end_nodes, set(), radius,itI)
            itI+=1
            
        c,p=r
        for i in range(itI-1):
            c+=1
            p.insert(0,start_node)
        car.cost=c
        car.setPath(p)
            

    def __search_aux__(self, graph:Graph, start_node:Node,carN:int,cars:list[Car],end_nodes:list, visited:set, radius:int,it:int)->tuple[int,list[Node]]:
        """Auxialiary method for the search method

        Args:
            graph (Graph): the graph to search the path on
            start_node (Node): the starting node
            carN (int): the position of the car to search a path to
            cars (list[Car]): the list of all cars
            end_nodes (list[tuple[int,int]]): the list of the positions of the coordenates a car needs to reach
            visited (set): the set containing all visited nodes
            radius (int): the depth of the recursion allowed
            it (int): the iteration number of the current call

        Returns:
            tuple[int,list[Node]]: a tuple with the cost and nodes path of the recursive search
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
