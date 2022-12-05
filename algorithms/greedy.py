from graph.graph import Graph
from graph.node import Node
from graph.car import Car
from .algorithm import Algorithm

class GREEDY(Algorithm):
    """
    Class implementing a breath-first-search algorithm
    """
    def search(self, graph:Graph,carN:int, cars:list[Car], end_nodes:list[tuple[int,int]]):
        """Searches the graph startign on start_node until reaching one of the end_nodes using the greedy algorithm

        Args:
            graph (Graph): the graph to search the path in
            start_node (Node): the node to start the search in 
            end_nodes ([(Int,Int)]): the list of all position corresponding to end Nodes

        Returns:
            (int,[Node]): pair with the total distance travels and the path taken to reach the end
        """
        car=cars[carN]
        start_node = car.getLastNode()
        current = start_node
        itI=0
        it = itI
        parents = {}
        parents[(current,it)] = None
        total = 0
        iteration=2**6
        while (current.x,current.y) not in end_nodes:
            valid=list(filter(lambda n: not any(c.colides(current.coords(),n[0].coords(),it) for c in cars[:carN]) ,graph.adjList[current]))
            if valid==[]:
                itI+=1
                it = itI
                parents[(start_node,it)]=(start_node,it-1)
                current=start_node
                total=it
            (next, next_cost) = min(valid, key = lambda nc: nc[0].getEstimate(end_nodes))
            parents[(next,it+1)] = (current,it)
            total += next_cost
            current = next
            it+=1
        cars[carN].setPath(self.__reconstruct_path__((current,it),parents))
        cars[carN].cost=total


    def __reconstruct_path__(self,node:tuple[Node,int],parents:dict):
        path = []
        prev=node
        while prev != None:
            path.insert(0, prev[0])
            prev=parents[prev]
        return path