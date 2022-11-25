import itertools
from math import floor, ceil


def uniquefy(generator):
    aux = set()
    
    for i in generator:
        if i not in aux:
            yield i
        aux.add(i)

wall = 'X'
track = '-'

def __intersect_vertical__(xi:int, xf:int, a:float, b:float, c:float):
    """
    Fills the ans set with the coordinates of intersection points of vertical lines with
    x coordinates between xi and xf (inclusive) with the line ax + by + c = 0
    """
    for x in range(xi, xf + 1):
        yield (float(x), -(a * x + c) / b)
    
def __intersect_horizontal__(yi:int, yf:int, a:float, b:float, c:float):
    """
    Fills the ans set with the coordinates of intersection points of horizontal lines with
    y coordinates between yi and yf (inclusive) with the line ax + by + c = 0
    """
    for y in range(yi, yf + 1):
        yield (-(c + b * y) / a, float(y))

def __intersected_squares__(xi:float, yi:float, xf:float, yf:float):
    """
    Fills the ans set with the grid squares that the line segment that
    connects (xi,yi) to (xf,yf) intersects the interior of.
    The coordinates given centered on the top left corner of the square they refer to
    (ex: coordinate (0,0) is the top left corner of square (0,0))
    """
    #these constants define the line by the equation ax + by + c = 0
    a = yi - yf
    b = xf - xi
    c = -(a * xi + b * yi)
    
    vert = __intersect_vertical__(floor(min(xi, xf)) + 1, ceil(max(xi, xf)) - 1, a, b, c)
    hor = __intersect_horizontal__(floor(min(yi, yf)) + 1, ceil(max(yi, yf)) - 1, a, b, c)
    
    for x,y in uniquefy(itertools.chain(vert, hor)):
        int_x = int(x)
        int_y = int(y)
        
        if int_x < 0 or int_y < 0:
            print((x, y), (xi, yi), (xf, yf), a, b, c)
        
        if not x.is_integer():      #horizontal line intersection
            yield (int_x, int_y - 1)
            yield (int_x, int_y)
        elif not y.is_integer():    #vertical line intersection
            yield (int_x - 1, int_y)
            yield (int_x, int_y)
        else:                       #corner
            orientation = (xf-xi)*(yf-yi) #positive direction means \, negative means /
            if orientation > 0:
                yield (int_x - 1, int_y - 1)
                yield (int_x, int_y)
            elif orientation < 0: 
                yield (int_x - 1, int_y)
                yield (int_x, int_y - 1)
    

def test_colision(matrix:list, rows:int, columns:int, xi:int, yi:int, xf:int, yf:int):
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
    
    orientation = (xf-xi)*(yf-yi) #positive direction means \, negative means /
    squares = [[(xi, yi), (xf, yf)]]
    squares.append(__intersected_squares__(xi + 0.5, yi + 0.5, xf + 0.5, yf + 0.5))
    
    if orientation > 0:
        squares.append(__intersected_squares__(xi + 1, yi, xf + 1, yf))
        squares.append(__intersected_squares__(xi, yi + 1, xf, yf + 1))
    elif orientation < 0:
        squares.append(__intersected_squares__(xi, yi, xf, yf))
        squares.append(__intersected_squares__(xi + 1, yi + 1, xf + 1, yf + 1))

    for x,y in uniquefy(itertools.chain(*squares)):
        if matrix[y][x] == wall:
            return True

    return False