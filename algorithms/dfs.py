from algorithms.algorithm import Algorithm

class DFS(Algorithm):
    """
    Class implementing a depth-first-search algorithm
    """
    def search(self, graph, start_node, end_nodes):
        return self.__search_aux__(graph, start_node, end_nodes, set())

    def __search_aux__(self, graph, start_node, end_nodes, visited):
        """Auxiliary method for the main search method

        Args:
            graph (Graph): the graph to search on
            start_node (str): the starting/current node of the search
            end_nodes (list(str)): the list with all possible ending nodes
            visited (list(str)): the list of all nodes already visited

        Returns:
            A pair containing the cost and path taken in the found solution
        """
        if (start_node.x, start_node.y) in end_nodes:
            return (0, [])

        visited.add(start_node)

        #Initialize ans as infinite, as this is a minimization
        #problem
        ans = (1e9, [])

        #print(start_node)
        #for each node adjacent to current node
        for (node, cost) in graph.adjList[start_node]:
            # We don't visit a node twice
            if node not in visited:
                res = self.__search_aux__(graph, node, end_nodes, visited)

                if ans is None or res[0] + cost < ans[0]:
                    res[1].insert(0, node)
                    ans = (res[0] + cost, res[1])

        return ans