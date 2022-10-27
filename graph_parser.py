from graph.graph import Graph

wall = 'X'
start = 'P'
end = 'F'
track = '-'
wall_cost = 25
normal_cost = 1

def circuit_from_file(filePath):
    matrix = []
    try:
        with open(filePath, "r") as f:
            matrix = f.readlines()
            #Remove '\n' from every line
            matrix = list(map(lambda s: s.strip('\n'), matrix))

    except IOError:
        print("Could not open " + filePath + " for reading")
        exit(1)

    (rows, cols) = __get_matrix_dimensions__(matrix)
    graph =  __transverse_circuit__(matrix, rows, cols)
    __validate_graph__(graph)
    return graph


def __get_matrix_dimensions__(matrix):
    if matrix == []:
        return (0,0)

    rows = len(matrix)
    cols = len(matrix[0])

    for row in matrix:
        if len(row) != cols:
            print("Invalid file. Circuit must be a square")
            exit(1)

    return (rows,cols)


def __transverse_circuit__(matrix, rows, cols):
    graph = Graph()

    for i in range(0,rows):
        for j in range(0, cols):
            if matrix[i][j] == start:
                graph.add_start(__coords_to_str__((i,j)))
            elif matrix[i][j] == end:
                graph.add_finish(__coords_to_str__((i,j)))

            if i + 1 < rows:
                __add_edge__(matrix, graph, (i,j), (i + 1, j))

            if j + 1 < cols:
                __add_edge__(matrix, graph, (i,j), (i, j + 1))

            if i - 1 >= 0:
                __add_edge__(matrix, graph, (i,j), (i - 1, j))

            if j - 1 >= 0:
                __add_edge__(matrix, graph, (i, j), (i, j - 1))
    return graph

def __add_edge__(matrix, graph, src, dest):
    cost = -1
    if matrix[dest[0]][dest[1]] == wall:
        cost = wall_cost
    elif matrix[dest[0]][dest[1]] in [track, start, end]:
        cost = normal_cost

    if cost == -1:
        print("Invalid character detected in position " + __coords_to_str__(dest)
              + ": " + matrix[dest[0]][dest[1]])
        exit(1)

    graph.add_edge(__coords_to_str__(src), __coords_to_str__(dest), cost)


def __coords_to_str__(coords):
    return "({x},{y}".format(x = coords[0], y = coords[1])

def __validate_graph__(graph):
    if graph.start == []:
        print("No starting position detected")
        exit(1)
    if graph.finish == []:
        print("No finish line detected")
        exit(1)