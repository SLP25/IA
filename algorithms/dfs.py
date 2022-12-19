from algorithms.algorithm import Algorithm
from collections import deque
from graph.graph import Graph
from graph.node import Node
import random
from graph.car import Car


class IterationLimitException(Exception):
    pass

class DFS(Algorithm):
    """
    Class implementing a depth-first-search algorithm
    """
    def search(self, graph:Graph,carN:int, cars:list[Car], end_nodes:list[tuple[int,int]],radius=1e9):
        """
            Searches the graph startig in the car in position carN last node until reaching one of the end_nodes using the bfs algorithm

        Args:
            graph (Graph): the graph to search the path on
            carN (int): the position of the car to search a path to
            cars (list[Car]): the list of all cars
            end_nodes (list[tuple[int,int]]): the list of the positions of the coordenates a car needs to reach

        """
        car=cars[carN]
        itI=0
        #the queue to store unprocessed Nodes
        start_node=car.getLastNode()
        queue = deque()
        parents={}
        # queue will store a tuple with the node to process,cost up to that node,depth
        parents[(start_node,itI)]=None
        queue.append((start_node,0,itI)) 
        visited = set()
        visited.add(start_node)
        maxitReched=False

        while queue:
            node, cost,it = queue.pop()
            car.graphPath.append(node)

            #found the finish
            if (node.x,node.y) in end_nodes:
                car.setPath(self.__reconstruct_path__((node,it),parents))
                car.cost=cost
                break
            if it<radius:
                #didn't find it so will add the nodes connected to it
                for (n,c) in graph.adjList[node]:
                    if ((n not in visited) and not any(c.colides(node.coords(),n.coords(),it) for c in cars[:carN])):
                        parents[(n,it+1)]=(node,it)
                        queue.append((n,cost + c,it+1))
                        visited.add(n)
            else:
                maxitReched=True
            #if no more ways restart, moving 1 iteration later
            if not queue and not maxitReched:
                itI+=1
                queue.append((start_node,itI,itI))
                visited = set()
                visited.add(start_node)
                parents[(start_node,itI)]=(start_node,itI-1)
