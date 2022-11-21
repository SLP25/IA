from graph.graph import Graph
from graph.node import Node
from .exceptions import InconsistenceSize,NoStartsFound,NoFinishesFound

wall = 'X'
start = 'P'
end = 'F'
track = '-'
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
            if __test_colision__(matrix, rows, cols, node.x, node.y, neightbour.x, neightbour.y):
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

def __sign__(x:int):
    """signoide function to apply to a given number

    Args:
        x (int): number to apply signoid to

    Returns:
        int: signoide representation of the number
    """
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0

def __test_colision__(matrix:list, rows:int, columns:int, xi:int, yi:int, xf:int, yf:int):
    """Verifies from given position and speed a colition will happen using a matrix representation of the circuit

    Args:
        matrix (list): the matrix representation of the circuit
        rows (int): the number of rows in the matrix
        columns (int): the number of columns in the matrix
        xi (int): x coordinate
        yi (int): y coordinate
        xf (int): x speed
        yf (int): y speed

    Returns:
        _type_: _description_
    """
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