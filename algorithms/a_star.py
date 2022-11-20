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
        graph,
        start_node,
        end_nodes,
        ):

        open_queue = PriorityQueue()
        open_queue.put((0 + start_node.__estimate__, start_node))

        close_set = set([])

        parents = {}
        parents[start_node] = start_node

        g = {}
        g[start_node] = 0

        while not open_queue.empty():
            (current_node, current_node_cost) = open_queue.delete()

            if (current_node.x, current_node.y) in graph.finishes:
                return (current_node_cost + current_node.__estimate__,
                        self.__reconstruct_path__((start_node,
                        current_node, current_node_cost, parents)))

            for edge in graph.adjList[current_node]:
                neighbor_node = list(edge)[0]
                edge_cost = list(edge)[1]

                if neighbor_node not in open_queue and neighbor_node \
                    not in closed_set:
                    parents[neighbor_node] = current_node
                    g[neighbor_node] = g[current_node] + edge_cost
                    open_queue.put(g[neighbor_node]
                                   + neighbor_node.__estimate__,
                                   neighbor_node)
                else:

                    if g[neighbor_node] > g[current_node] + edge_cost:
                        g[neighbor_node] = g[current_node] + edge_cost
                        parents[neighbor_node] = current_node

                        if neighbor_node in closed_set:
                            closed_set.remove(neighbor_node)
                            open_queue.put(g[neighbor_node]
                                    + neighbor_node.__estimate__,
                                    neighbor_node)

            open_queue.delete(current_node)
            closed_set.add(current_node)

        return None

    def __reconstruct_path__(
        start_node,
        current_node,
        current_node_cost,
        parents,
        ):
        path = []

        while parents[current_node] != current_node:
            path.append(current_node)
            current_node = parents[current_node]

        path.append(start_node)

        path.reverse()

        return path