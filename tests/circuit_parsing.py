import graph.graph_parser as gp
from graph.node import Node
from tests.scuffed_gui import show_race
from traversals.bfs import bfs
from algorithms.dfs import DFS
import sys

sys.setrecursionlimit(10**6)

print("generating circuit...")
matrix = gp.matrix_from_file("circuits/bahrain.txt")
graph = gp.circuit_from_matrix(matrix)
print(len(graph.nodes))
dfs = DFS()

print("done! applying pathfinding...")
(cost, path) = dfs.search(graph, Node(graph.starts[0][0], graph.starts[0][1], 0, 0), graph.finishes)

print(f"done! cost: {cost}")
input("Press any key to start animation...")
show_race(graph, matrix, path)
