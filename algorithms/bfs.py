from graph.graph import Graph
from graph.node import Node
from queue import Queue
import random
from algorithms.algorithm import Algorithm
from graph.car import Car

class BFS(Algorithm):    
    """
    Class implementing a breadth-first-search algorithm
    """
    def search(self, graph:Graph, cars:list[Car], end_nodes:list):
        """Searches the graph startign on start_node until reaching one of the end_nodes using the bfs algorithm

        Args:
            graph (Graph): the graph to search the path in
            start_node (Node): the node to start the search in 
            end_nodes ([(Int,Int)]): the list of all position corresponding to end Nodes

        Returns:
            (int,[Node]): pair with the total distance travels and the path taken to reach the end
        """
        random.shuffle(cars)
        for carN,car in enumerate(cars):
            itI=0
            #the queue to store unprocessed Nodes
            start_node=car.getLastNode()
            queue = Queue()
            parents={}
            # queue will store a tuple with the node to process,cost up to that node,depth
            parents[(start_node,itI)]=None
            queue.put((start_node,0,itI)) 
            visited = set()
            visited.add(start_node)

            while not queue.empty():
                node, cost,it = queue.get(0)

                #found the finish
                if (node.x,node.y) in end_nodes:
                    car.setPath(self.__reconstruct_path__((node,it),parents))
                    car.cost=cost
                    break

                #didn't find it so will add the nodes connected to it
                for (n,c) in graph.adjList[node]:
                    if ((n not in visited) and not any(c.colides(node.coords(),n.coords(),it) for c in cars[:carN])):
                        parents[(n,it+1)]=(node,it)
                        queue.put((n,cost + c,it+1))
                        visited.add(n)

                #if no more ways restart, moving 1 iteration later
                if queue.empty():
                    itI+=1
                    queue.put((start_node,itI,itI))
                    visited = set()
                    visited.add(start_node)
                    parents[(start_node,itI)]=(start_node,itI-1)
                    
                    
            
                    
        
    def __reconstruct_path__(self,node:tuple[Node,int],parents:dict):
        path = []
        prev=node
        while prev != None:
            path.insert(0, prev[0])
            prev=parents[prev]
        return path