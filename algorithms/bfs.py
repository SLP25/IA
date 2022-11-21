from graph.graph import Graph
from graph.node import Node
from queue import Queue
from algorithms.algorithm import Algorithm

class BFS(Algorithm):
    """
    Class implementing a breath-first-search algorithm
    """
    def search(self, graph:Graph, start_node:Node, end_nodes:list):
        """Searches the graph startign on start_node until reaching one of the end_nodes using the bfs algorithm

        Args:
            graph (Graph): the graph to search the path in
            start_node (Node): the node to start the search in 
            end_nodes ([(Int,Int)]): the list of all position corresponding to end Nodes

        Returns:
            (int,[Node]): pair with the total distance travels and the path taken to reach the end
        """
        #the queue to store unprocessed Nodes
        queue = Queue()
        # queue will store a tuple with the node to process,cost up to that node,previous nodes information
        queue.put((start_node,0,None))
        visited = set()
        visited.add(start_node)

        while not queue.empty():
            node, cost,prev = queue.get(0)

            #found the finish
            if (node.x,node.y) in end_nodes:
                return (cost, self.__reconstruct_path__((node, cost, prev)))
            
            #didn't find it so will add the nodes connected to it
            for (n,c) in graph.adjList[node]:
                if n not in visited:
                    queue.put((n,cost + c,(node, cost,prev)))
                    visited.add(n)
        
    def __reconstruct_path__(self,data):
        """_summary_

        Args:
            data (tuple): a tuple with a node the cust up to that node and a tuple containing the previou node

        Returns:
            list: the path taken from the start up to the end
        """
        path = []
        prev=True
        while prev != None:
            node,cost,prev=data
            path.insert(0, node)
            data = prev

        return path