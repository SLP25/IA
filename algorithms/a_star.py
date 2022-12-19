from graph.graph import Graph
from graph.node import Node
from graph.car import Car
from queue import PriorityQueue,Queue
from .algorithm import Algorithm
import time

class A_STAR(Algorithm):
    """
    Class implementing a a*-search algorithm
    """
    def search(self, graph:Graph,carN:int, cars:list[Car], end_nodes:list[tuple[int,int]]):
        """
           Searches the graph startig in the car in position carN last node until reaching one of the end_nodes using the A* algorithm

        Args:
            graph (Graph): the graph to search the path on
            carN (int): the position of the car to search a path to
            cars (list[Car]): the list of all cars
            end_nodes (list[tuple[int,int]]): the list of the positions of the coordenates a car needs to reach

        """
        car=cars[carN]
        itI=0
        start_node = car.getLastNode()
        
        
        getEstimate = lambda x: x.getEstimate(end_nodes)
        opened_queue = PriorityQueue()
        parents = {}
        costs={(start_node,itI):itI}
        parents[(start_node,itI)] = None
        opened_queue.put((0+getEstimate(start_node),start_node,-itI))
        
        visited = set()

        

        while not opened_queue.empty():
            current_node_cost, current_node,it = opened_queue.get() # current_node_cost edges from start + estimate from that node
            car.graphPath.append(current_node)
            if (current_node.x,current_node.y) in end_nodes:
                car.setPath(self.__reconstruct_path__((current_node,it),parents))
                car.cost=current_node_cost
                break
            visited.add(current_node)
            for neighbor_node,edge_cost in graph.adjList[current_node]:
                if neighbor_node in visited or any(c.colides(current_node.coords(),neighbor_node.coords(),it) for c in cars[:carN]):
                    continue
                g = current_node_cost-getEstimate(current_node)+edge_cost+getEstimate(neighbor_node)
                
                if (neighbor_node,it+1) in costs:
                        if g>=costs[(neighbor_node,it+1)]:
                            continue
                
                parents[(neighbor_node,it+1)]=(current_node,it)
                costs[(neighbor_node,it+1)]=g
                opened_queue.put((g,neighbor_node,it+1))

            if opened_queue.empty():
                itI+=1
                opened_queue.put((itI+getEstimate(start_node),start_node,itI))
                visited = set()
                costs[(start_node,itI)]=itI
                visited.add(start_node)
                parents[(start_node,itI)]=(start_node,itI-1)


          
                    
                    
                    
                
                
                    