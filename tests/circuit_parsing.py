import graph_parser as gp

graph = gp.circuit_from_file("circuits/teste.txt")

print("==============Nodes==============")
print(len(graph.nodes))