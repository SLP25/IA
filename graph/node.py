import math

class Node:
    """
        the representation of a position with a speed vector
    """
    def __init__(self, x:int, y:int, vx:int, vy:int):
        """Creates a new Node instance with the given values

        Args:
            x (int): The x componet of the position
            y (int): The y componet of the position
            vx (int): The x componet of the speed vector
            vy (int): The y componet of the speed vector
        """        
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.__estimate__ = None
        
    def getEstimate(self, finishes:list):
        """calculates the estimate of the nodes to the finishes if not stored yet

        Args:
            finishes (list): the list of all position representing a finish

        Returns:
            float: the distance between the node and the closest finish
        """
        if self.__estimate__ == None:
            self.__estimate__ = self.__gen_estimate__(finishes)
        return self.__estimate__

    def __str__(self):
        """the string representation of the node

        Returns:
            string: the string representation of the node
        """
        return f"Node: p=({self.x},{self.y}) v=({self.vx},{self.vy})"
    
    def __eq__(self, node:object):
        """compares if an object is equal to the node

        Args:
            node (object): the object to compare to the node

        Returns:
            bool: wether they are equal or not
        """
        return isinstance(node,Node) and node.x == self.x and node.y == self.y and node.vx == self.vx and node.vy == self.vy
    
    def __hash__(self):
        """generates the hash of the node

        Returns:
            int: the hash of the node
        """
        return hash((self.x, self.y, self.vx, self.vy))
    
    def __gen_estimate__(self, finishes:list):
        """calculates the estimate of the nodes to the finishes

        Args:
            finishes (list): the list of all position representing a finish

        Returns:
            float: the distance between the node and the closest finish
        """
        return min(map(lambda f: max(__estimateAxis__(self.x,self.vx,f[0]),
                                     __estimateAxis__(self.y,self.vy,f[1])), finishes))
    def __gt__(self, other):
        selfSpeedNorm=self.vx**2+self.vy**2
        otherSpeedNorm=other.vx**2+other.vy**2
        if selfSpeedNorm > otherSpeedNorm:
            return True
        elif selfSpeedNorm < otherSpeedNorm:
            return False
        else:
            selfPosNorm  = self.x**2+self.y**2
            otherPosNorm = other.x**2+other.y**2
            if selfPosNorm > otherPosNorm:
                return True
            else: 
                return False
        
    def deserialize(self):
        """gets the node as a tuple of its vectors xy positions

        Returns:
            tuple: the x position,y position ,x speed vector component,y speed vector component
        """
        return (self.x, self.y, self.vx, self.vy)

def __estimateAxis__(i:int, vi:int, f:int):
    """generates the estimate for one axis

    Args:
        i (int): starting position of the axis
        vi (int): starting velocity of the axis
        f (int): final position of the axis

    Returns:
        float: the distance in the axis between one position and another
    """
    if i == f:
        return 0
    elif i < f:
        a = 0.5
        b = vi + 0.5
        c = i - f
    else:
        a = -0.5
        b = vi - 0.5
        c = i - f

    S = [(-b - math.sqrt(b * b - 4 * a * c)) / (2 * a),
            (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)]

    return math.ceil(min(filter(lambda t: t >= 0, S)))