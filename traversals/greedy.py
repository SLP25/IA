from graph.graph import Graph
from graph.node import Node

def greedy(graph, start):
    current = Node(start[0], start[1], 0, 0)
    previous = {}
    previous[current] = None
    total = 0
    
    while (current.x,current.y) not in graph.finishes:
        (next, next_cost) = min(graph.adjList[current], key = lambda nc: nc[0].getEstimate(graph.finishes))
        previous[next] = current
        total += next_cost
        current = next

    return (__reconstruct_path__(previous, current), total)


def __reconstruct_path__(previous, end):
    path = []
    
    while end != None:
        path.insert(0, end)
        end = previous[end]
        
    return path