import math

class Node:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.__estimate__ = None
        
    def getEstimate(self, finishes):
        if self.__estimate__ == None:
            self.__estimate__ = self.__gen_estimate__(finishes)
        return self.__estimate__

    def __str__(self):
        return f"Node: p=({self.x},{self.y}) v=({self.vx},{self.vy})"
    
    def __eq__(self, node):
        return isinstance(node,Node) and node.x == self.x and node.y == self.y and node.vx == self.vx and node.vy == self.vy
    
    def __hash__(self):
        return hash((self.x, self.y, self.vx, self.vy))
    
    def __gen_estimate__(self, finishes):
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
        return (self.x, self.y, self.vx, self.vy)

def __estimateAxis__(i, vi, f):
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