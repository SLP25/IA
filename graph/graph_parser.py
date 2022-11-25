from graph.graph import Graph
from graph.node import Node
from .exceptions import InconsistenceSize,NoStartsFound,NoFinishesFound
from .collision import test_colision

start = 'P'
end = 'F'
wall_cost = 25
normal_cost = 1

def get_matrix_dimensions(matrix:list):
    """gets the size of the matrix given and validates its a valid map

    Args:
        matrix (list): the matrix to get dimensions from
        
    Raises:
        InconsistenceSize: if the size of all collums is not the same

    Returns:
        tuple: the number of rows and number of columns
    """

    
    if matrix == []:
        return (0,0)

    rows = len(matrix)
    cols = len(matrix[0])

    for row in matrix:
        if len(row) != cols:
            raise InconsistenceSize()


    return (rows,cols)

def circuit_from_matrix(matrix:list):
    """converts the matrix representation of a circuit into the graph representation

    Args:
        matrix (list): the matrix representing a circuit

    Returns:
        Graph: the graph representation of the matrix
    """
    (rows, cols) = get_matrix_dimensions(matrix)
    g = Graph()
    __set_start_and_finish__(g, matrix, rows, cols)
    __transverse_circuit__(g, matrix, rows, cols)
    return g

def __set_start_and_finish__(g:Graph, matrix:list, rows:int, cols:int):
    """adds the start and end position from a matrix representation of a circuit to the graph representation

    Args:
        g (Graph): the graph representation of the circuit
        matrix (list): the matrix representation of the circuit
        rows (int): the number of rows in the matrix representation of the circuit
        cols (int):  the number of cols in the matrix representation of the circuit
    Raises:
        NoStartsFound: if no starts are found in the matrix
        NoFinishesFound: if no finishes are found in the matrix
    """
    for y in range(0,rows):
        for x in range(0, cols):
            if matrix[y][x] == start:
                g.add_start(x, y)
            if matrix[y][x] == end:
                g.add_finish(x, y)
                
    if g.starts == []:
        raise NoStartsFound()
    if g.finishes == []:
        raise NoFinishesFound()


def __transverse_circuit__(g:Graph, matrix:list, rows:int, cols:int):
    """genererates Nodes into the graph from the matrix representation

    Args:
        g (Graph): the graph representation of the circuit
        matrix (list): the matrix representation of the circuit
        rows (int): the number of rows in the matrix representation of the circuit
        cols (int):  the number of cols in the matrix representation of the circuit
    """
    accelerations = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]
    visited = set(map(lambda xy: Node(xy[0], xy[1], 0, 0), g.starts))
    to_visit = set(visited)
    
    while len(to_visit) != 0:
        node = to_visit.pop()
        for a in accelerations:
            neightbour = __apply_acceleration__(node, a)
            cost = normal_cost
            if test_colision(matrix, rows, cols, node.x, node.y, neightbour.x, neightbour.y):
                neightbour = Node(node.x, node.y, 0, 0)
                cost = wall_cost
            g.add_edge(node, neightbour, cost)
            if neightbour not in visited:
                visited.add(neightbour)
                to_visit.add(neightbour)

def __apply_acceleration__(node:Node, a:tuple):
    """applies an acceleration vector a node

    Args:
        node (Node): the node to apply the acceleration in
        a (tuple): the accelaration to apply to the node

    Returns:
        Node: return a new node resulting from applying the acceleration to the given vector
    """
    (ax, ay) = a
    return Node(node.x + node.vx + ax, node.y + node.vy + ay, node.vx + ax, node.vy + ay)