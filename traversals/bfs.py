from graph.graph import Graph
from graph.node import Node

def bfs(graph, start):
    first = Node(start[0], start[1], 0, 0)
    queue = [(first,0)]
    visited = set([first])
    previous = {first: None}
    
    while len(queue) != 0:
        (node, cost) = queue.pop(0)
        
        if (node.x,node.y) in graph.finishes:
            return (__reconstruct_path__(previous, node), cost)
        
        for (n,c) in graph.adjList[node]:
            if n not in visited:
                queue.append((n,cost + c))
                visited.add(n)
                previous[n] = node
        
def __reconstruct_path__(previous, end):
    path = []
    
    while end != None:
        path.insert(0, end)
        end = previous[end]
        
    return path