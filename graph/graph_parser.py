from graph.graph import Graph
from graph.node import Node

wall = 'X'
start = 'P'
end = 'F'
track = '-'
wall_cost = 25
normal_cost = 1

def circuit_from_file(filePath):
    matrix = matrix_from_file(filePath)
    graph = Graph()
    (rows, cols) = get_matrix_dimensions(matrix)
    __set_start_and_finish__(graph, matrix, rows, cols)
    __transverse_circuit__(graph, matrix, rows, cols)
    return graph

def matrix_from_file(filePath):
    matrix = []
    try:
        with open(filePath, "r") as f:
            matrix = f.readlines()
            #Remove '\n' from every line
            matrix = list(map(lambda s: s.strip('\n'), matrix))

    except IOError:
        print("Could not open " + filePath + " for reading")
        exit(1)
        
    return matrix

def get_matrix_dimensions(matrix):
    if matrix == []:
        return (0,0)

    rows = len(matrix)
    cols = len(matrix[0])

    for row in matrix:
        if len(row) != cols:
            print("Invalid file. Circuit must be a rectangle")
            exit(1)

    return (rows,cols)

def circuit_from_matrix(matrix):
    (rows, cols) = get_matrix_dimensions(matrix)
    graph = Graph()
    (rows, cols) = get_matrix_dimensions(matrix)
    __set_start_and_finish__(graph, matrix, rows, cols)
    __transverse_circuit__(graph, matrix, rows, cols)
    return graph

def __set_start_and_finish__(graph, matrix, rows, cols):
    for y in range(0,rows):
        for x in range(0, cols):
            if matrix[y][x] == start:
                graph.add_start(x, y)
            if matrix[y][x] == end:
                graph.add_finish(x, y)
                
    if graph.starts == []:
        print("Starting position not found")
        exit(1)
    if graph.finishes == []:
        print("No finish line detected")
        exit(1)


def __transverse_circuit__(graph, matrix, rows, cols):
    accelerations = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]
    visited = set(map(lambda xy: Node(xy[0], xy[1], 0, 0), graph.starts))
    to_visit = set(visited)
    
    while len(to_visit) != 0:
        node = to_visit.pop()
        for a in accelerations:
            neightbour = __apply_acceleration__(node, a)
            cost = normal_cost
            if __test_colision__(matrix, rows, cols, node.x, node.y, neightbour.x, neightbour.y):
                neightbour = Node(node.x, node.y, 0, 0)
                cost = wall_cost
            graph.add_edge(node, neightbour, cost)
            if neightbour not in visited:
                visited.add(neightbour)
                to_visit.add(neightbour)

def __apply_acceleration__(node, a):
    (ax, ay) = a
    return Node(node.x + node.vx + ax, node.y + node.vy + ay, node.vx + ax, node.vy + ay)

def __sign__(x):
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0

def __test_colision__(matrix, rows, columns, xi, yi, xf, yf):
    if xf < 0 or xf >= columns or yf < 0 or yf >= rows:
        return True
    
    #TEMPORARIO!!!
    (x,y) = (xi,yi)
    while (x,y) != (xf,yf):
        step_x = __sign__(xf-x) 
        step_y = __sign__(yf-y)
        
        if matrix[y][x + step_x] == wall or matrix[y + step_y][x] == wall or matrix[y + step_y][x + step_x] == wall:
            return True
        
        x += step_x
        y += step_y
    
    return False