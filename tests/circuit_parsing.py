import graph.graph_parser as gp
from tests.scuffed_gui import show_race
from traversals.bfs import bfs

print("generating circuit...")
matrix = gp.matrix_from_file("circuits/bahrain.txt")
graph = gp.circuit_from_matrix(matrix)

print("done! applying pathfinding...")
(path,cost) = bfs(graph, graph.starts[0])

print(f"done! cost: {cost}")
input("Press any key to start animation...")
show_race(graph, matrix, path)