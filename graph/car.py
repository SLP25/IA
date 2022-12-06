import itertools
from .node import Node
import math
import numpy as np
import random


class Car():
    newid = itertools.count()
    def __init__(self,start:Node):
        self.id = next(Car.newid)
        self.color = self.generateColor()
        self.fullPath=[start]
        self.cost=-1
    
    def getSpeeds(self):
        if not hasattr(self,'speed'):
            self.speed=[n.speed() for n in self.fullPath]
        return self.speed
    
    def getCoords(self):
        if not hasattr(self,'coords'):
            self.coords=[n.coords() for n in self.fullPath]
        return self.coords
    def getNpVspeed(self):
        if not hasattr(self,'npVspeed'):
            self.npVspeed=np.array(list(map(self.__vectorNorm__,self.getSpeeds())))
        return self.npVspeed

    
    def getCoordsAtInstance(self,inst):
        return self.fullPath[inst].coords()
    
    @staticmethod
    def on_segment(p, q, r):
        if r[0] <= max(p[0], q[0]) and r[0] >= min(p[0], q[0]) and r[1] <= max(p[1], q[1]) and r[1] >= min(p[1], q[1]):
            return True
        return False
    @staticmethod    
    def orientation(p, q, r):
        val = ((q[1] - p[1]) * (r[0] - q[0])) - ((q[0] - p[0]) * (r[1] - q[1]))
        if val == 0 : return 0
        return 1 if val > 0 else -1
    @staticmethod
    
    def intersects(p1, q1, p2, q2):
        o1 = Car.orientation(p1, q1, p2)
        o2 = Car.orientation(p1, q1, q2)
        o3 = Car.orientation(p2, q2, p1)
        o4 = Car.orientation(p2, q2, q1)
        
        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and Car.on_segment(p1, q1, p2) : return True
        if o2 == 0 and Car.on_segment(p1, q1, q2) : return True
        if o3 == 0 and Car.on_segment(p2, q2, p1) : return True
        if o4 == 0 and Car.on_segment(p2, q2, q1) : return True

        return False
    
    

    def colides(self,coordsI,coordsF,itI):
        if itI==0 or itI >= len(self.fullPath)-2 or coordsI==coordsF:#is in the start,finish or not moving
            return False
        A=coordsI
        B=coordsF
        C=self.getCoordsAtInstance(itI)
        D=self.getCoordsAtInstance(itI+1)
        if B==D: return True
        return Car.intersects(A,B,C,D)
        
        
     
    
    
    def addNodeToPath(self,cost:int,n:Node):
        self.fullPath.append(n)
        self.cost.append(cost)
        
    def setPath(self,l:list):
        self.fullPath=l.copy()
        
    def getLastNode(self):
        if self.fullPath:
            return self.fullPath[-1]
        return None
    
    #gui
    @staticmethod
    def toGuiSize(tup:tuple):
        return (16*tup[0],16*tup[1])
    
    @staticmethod
    def generateColor():
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        return (r,g,b)
    
    def getCarPosAtInstance(self,instance=0):
        """gets the coordenats the car is at in a given instance

        Args:
            instance (int, optional): timestamp to get position at. Defaults to 0.

        Returns:
            tuple: a tuple with the coordnats at that instance
        """
        if instance>len(self.getCoords())-1:
            instance=-1
        return self.toGuiSize(self.getCoords()[instance])
    
    def getCarSpeedAtInstance(self,instance=0):
        """gets the coordenats the car is at in a given instance

        Args:
            instance (int, optional): timestamp to get position at. Defaults to 0.

        Returns:
            tuple: a tuple with the coordnats at that instance
        """
        if instance>len(self.getSpeeds())-1:
            instance=-1
        return self.getSpeeds()[instance]
    
    def getTopSpeed(self):
        """Calculates the top Speed of the car

        Returns:
            float: top speed of the car
        """
        return np.amax(self.getNpVspeed())
    def getAverageSpeed(self):
        """Calculates the Average Speed of the car

        Returns:
            float: average speed of the car
        """
        return np.mean(self.getNpVspeed())
    def getMedian(self):
        """Calculates the Median Speed of the car

        Returns:
            float: median speed of the car
        """
        return np.median(self.getNpVspeed())
    def getStd(self):
        """Calculates the Standard deviation Speed of the car

        Returns:
            float: standard deviation speed of the car
        """
        return np.std(self.getNpVspeed())
    def getVar(self):
        """Calculates the variance Speed of the car

        Returns:
            float: variance speed of the car
        """
        return np.var(self.getNpVspeed())
    def get25Percentil(self):
        """Calculates the percentil 25 Speed of the car

        Returns:
            float: percentil 25 speed of the car
        """
        return np.percentile(self.getNpVspeed(),25)
    def get50Percentil(self):
        """Calculates the percentil 50 Speed of the car

        Returns:
            float: percentil 50 speed of the car
        """
        return np.percentile(self.getNpVspeed(),50)
    def get75Percentil(self):
        """Calculates the percentil 75 Speed of the car

        Returns:
            float: percentil 75 speed of the car
        """
        return np.percentile(self.getNpVspeed(),75)
        
    
        
    
    def __vectorNorm__(self,vector):
        """return the norm of a given vector

        Args:
            vector (tuple): vector

        Returns:
            float: the norm of the given vector
        """
        return math.sqrt(sum(map(lambda x: math.pow(x,2),vector)))
        
    
    def getCarSpeedNormAtInstance(self,instance=0):
        """Gets the norm speed of the car at a given instance

        Args:
            instance (int, optional): timestamp to get the speedNorm at. Defaults to 0.

        Returns:
            float: the Norm of the speed at the given position
        """
        if instance>len(self.getSpeeds()):
            instance=-1
        return self.__vectorNorm__(self.getSpeeds()[instance])
    
    def getCarLineWidthAtInstance(self,instance=0):
        """Gets the width the line representation of the path should have at a given instance

        Args:
            instance (int, optional): timestamp to calculate the width at. Defaults to 0.

        Returns:
            int: the width the line should have at the given intance
        """
        maxwidth=14
        minwidth=1
        speed=self.getCarSpeedNormAtInstance(instance)
        if speed==0:
            return minwidth
        width=max(minwidth,math.ceil(maxwidth/speed))
        return width
    

    
    
    
    
    

    