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
           Searches the graph startign on start_node until reaching one of the end_nodes using th A* algorithm

        Args:
            graph (Graph): the graph to search the path in
            start_node (Node): the node to start the search in 
            end_nodes ([(Int,Int)]): the list of all position corresponding to end Nodes

        Returns:
            (int,[Node]): pair with the total distance travels and the path taken to reach the end
        """
        car=cars[carN]
        itI=0
        start_node = car.getLastNode()
        
        
        getEstimate = lambda x: x.getEstimate(end_nodes)
        opened_queue = PriorityQueue()
        parents = {}
        parents[(start_node,itI)] = None
        opened_queue.put((0+getEstimate(start_node),start_node,-itI))
        
        visited = set()

        

        while not opened_queue.empty():
            current_node_cost, current_node,Nit = opened_queue.get() # current_node_cost edges from start + estimate from that node
            it=-Nit
            if (current_node.x,current_node.y) in end_nodes:
                car.setPath(self.__reconstruct_path__((current_node,it),parents))
                car.cost=current_node_cost
                break
            visited.add(current_node)
            for neighbor_node,edge_cost in graph.adjList[current_node]:
                if neighbor_node in visited or any(c.colides(current_node.coords(),neighbor_node.coords(),it) for c in cars[:carN]):
                    continue
                g = current_node_cost-getEstimate(current_node)+edge_cost+getEstimate(neighbor_node)
                
                update=[]
                continuing=False
                for p,(ga,node,itp) in enumerate(opened_queue.queue):
                    if node==neighbor_node:
                        if g<ga:
                            del opened_queue.queue[p]
                        else:    
                            continuing=True
                        break
                if continuing:
                    continue
                
                parents[(neighbor_node,it+1)]=(current_node,it)
                
                opened_queue.put((g,neighbor_node,-(it+1)))

            if opened_queue.empty():
                itI+=1
                opened_queue.put((itI+getEstimate(start_node),start_node,-itI))
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


          
                    
                    
                    
                
                
                    