from graph.graph import Graph
from graph.node import Node
from queue import PriorityQueue
from .algorithm import Algorithm

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
        """Searches the graph startign on start_node until reaching one of the end_nodes using th A* algorithm

        Args:
            graph (Graph): the graph to search the path in
            start_node (Node): the node to start the search in 
            end_nodes ([(Int,Int)]): the list of all position corresponding to end Nodes

        Returns:
            (int,[Node]): pair with the total distance travels and the path taken to reach the end
        """
        opened_queue = PriorityQueue()
        opened_queue.put((0 + start_node.getEstimate(end_nodes), start_node))

        closed_set = set([])

        parents = {}
        parents[start_node] = start_node

        g = {}
        g[start_node] = 0

        while not opened_queue.empty():
            (current_node_cost, current_node) = opened_queue.get()

            if (current_node.x,current_node.y) in end_nodes:
                return (current_node_cost + current_node.getEstimate(end_nodes),
                        self.__reconstruct_path__(start_node,
                        current_node,parents))

            for edge in graph.adjList[current_node]:
                neighbor_node = edge[0]
                edge_cost = edge[1]
                if not any(neighbor_node in node for node in opened_queue.queue) and neighbor_node \
                    not in closed_set:
                    parents[neighbor_node] = current_node
                    g[neighbor_node] = g[current_node] + edge_cost
                    opened_queue.put((g[neighbor_node]
                                   + neighbor_node.getEstimate(end_nodes),
                                   neighbor_node))
                else:
                    if g[neighbor_node] > g[current_node] + edge_cost:
                        g[neighbor_node] = g[current_node] + edge_cost
                        parents[neighbor_node] = current_node

                        if neighbor_node in closed_set:
                            closed_set.remove(neighbor_node)
                            opened_queue.put((g[neighbor_node]
                                    + neighbor_node.getEstimate(end_nodes),
                                    neighbor_node))

            opened_queue.get(current_node)
            closed_set.add(current_node)

        return None

    def __reconstruct_path__(
        self,
        start_node : Node,
        current_node : Node,
        parents : dict,
        ):
        """_summary_

        Args:
            start_node (Node): the starting node
            current_node (Node): the node it was searching for
            parents (dict): the dictionary containing the parent of each node

        Returns:
            list: the path taken from the start up to the end
        """

        path = []

        while parents[current_node] != current_node:
            path.append(current_node)
            current_node = parents[current_node]

        path.append(start_node)

        path.reverse()

        return path
