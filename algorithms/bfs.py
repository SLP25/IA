from graph.graph import Graph
from graph.node import Node
from queue import Queue
from algorithms.algorithm import Algorithm

class BFS(Algorithm):
    """
    Class implementing a breath-first-search algorithm
    """
    def search(self, graph, start_node, end_nodes):
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
                return (cost,self.__reconstruct_path__((node, cost, prev)))
            
            #didn't find it so will add the nodes connected to it
            for (n,c) in graph.adjList[node]:
                if n not in visited:
                    queue.put((n,cost + c,(node, cost,prev)))
                    visited.add(n)
        
    def __reconstruct_path__(self,data):
        path = []
        prev=True
        while prev != None:
            node,cost,prev=data
            path.insert(0, node)
            data = prev

        return path