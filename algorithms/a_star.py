from graph.graph import Graph
from graph.node import Node
from queue import PriorityQueue,Queue
from .algorithm import Algorithm
import time

class A_STAR(Algorithm):
    """
    Class implementing a a*-search algorithm
    """
    def search(
        
        self,
        graph:Graph,
        start_node:Node,
        end_nodes:list,
        ):
        """
           Searches the graph startign on start_node until reaching one of the end_nodes using th A* algorithm

        Args:
            graph (Graph): the graph to search the path in
            start_node (Node): the node to start the search in 
            end_nodes ([(Int,Int)]): the list of all position corresponding to end Nodes

        Returns:
            (int,[Node]): pair with the total distance travels and the path taken to reach the end
        """
        getEstimate = lambda x: x.getEstimate(end_nodes)
        
        opened_queue = PriorityQueue()
        
        parents = {}
        
        opened_queue.put((0+getEstimate(start_node),start_node))
        
        closed_set = set()

        

        while not opened_queue.empty():
            (current_node_cost, current_node) = opened_queue.get() # current_node_cost edges from start + estimate from that node
            if (current_node.x,current_node.y) in end_nodes:
                return (current_node_cost,self.__reconstruct_path__(current_node, parents))
            
            closed_set.add(current_node)
            
            for neighbor_node,edge_cost in graph.adjList[current_node]:
                if neighbor_node in closed_set:
                    continue
                g = current_node_cost-getEstimate(current_node)+edge_cost+getEstimate(neighbor_node)
                
                update=[]
                continuing=False
                for p,(ga,node) in enumerate(opened_queue.queue):
                    if node==neighbor_node:
                        if g<ga:
                            del opened_queue.queue[p]
                        else:    
                            continuing=True
                        break
                if continuing:
                    continue
                
                parents[neighbor_node]=current_node
                
                opened_queue.put((g,neighbor_node))
                
                
            
     
              
    
    

    def __reconstruct_path__(
        self,
        current_node : Node,
        parents : dict,
        ):
        """_summary_

        Args:
            current_node (Node): the node it was searching for
            parents (dict): the dictionary containing the parent of each node

        Returns:
            list: the path taken from the start up to the end
        """

        path = [current_node]

        while current_node in parents:
            current_node = parents[current_node]          
            path.insert(0,current_node)
            
        return path


          
                    
                    
                    
                
                
                    