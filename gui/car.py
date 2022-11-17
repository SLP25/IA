import random
import math
import numpy as np
def generateRandomColor():
    """generates a random color in rgb in the tuple form

    Returns:
        tuple[3]: the rgb values of a color
    """
    c1=random.randint(0,255)
    c2=random.randint(0,255)
    c3=random.randint(0,255)
    return (c1,c2,c3)


class Car:
    coords=[]
    color=None
    topSpeed=None
    averageSpeed=None
    id=-1
    
    def __init__(self,id,color,tlen=0):
        self.id=id
        self.color=color
        self.tlen=tlen
        self.coords=[]
        self.speedinCoords=[]
        
        
    def fromNodes(self,nodes):
        for node in nodes:
            x,y,vx,vy=node.deserialize()    
            self.coords.append((x*10,y*10))
            self.speedinCoords.append((vx,vy))
        self.npVspeed=np.array(list(map(self.__vectorNorm__,self.speedinCoords)))
    
    def getCarPosAtInstance(self,instance=0):
        """gets the coordenats the car is at in a given instance

        Args:
            instance (int, optional): timestamp to get position at. Defaults to 0.

        Returns:
            tuple: a tuple with the coordnats at that instance
        """
        if instance>len(self.coords)-1:
            instance=-1
        return self.coords[instance]
    
    def getTopSpeed(self):
        """Calculates the top Speed of the car

        Returns:
            float: top speed of the car
        """
        return np.amax(self.npVspeed)
    def getAverageSpeed(self):
        """Calculates the Average Speed of the car

        Returns:
            float: average speed of the car
        """
        return np.mean(self.npVspeed)
    def getMedian(self):
        """Calculates the Median Speed of the car

        Returns:
            float: median speed of the car
        """
        return np.median(self.npVspeed)
    def getStd(self):
        """Calculates the Standard deviation Speed of the car

        Returns:
            float: standard deviation speed of the car
        """
        return np.std(self.npVspeed)
    def getVar(self):
        """Calculates the variance Speed of the car

        Returns:
            float: variance speed of the car
        """
        return np.var(self.npVspeed)
    def get25Percentil(self):
        """Calculates the percentil 25 Speed of the car

        Returns:
            float: percentil 25 speed of the car
        """
        return np.percentile(self.npVspeed,25)
    def get50Percentil(self):
        """Calculates the percentil 50 Speed of the car

        Returns:
            float: percentil 50 speed of the car
        """
        return np.percentile(self.npVspeed,50)
    def get75Percentil(self):
        """Calculates the percentil 75 Speed of the car

        Returns:
            float: percentil 75 speed of the car
        """
        return np.percentile(self.npVspeed,75)
        
    
        
    
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
        if instance>len(self.speedinCoords):
            instance=-1
        return self.__vectorNorm__(self.speedinCoords[instance])
    
    def getCarLineWidthAtInstance(self,instance=0):
        """Gets the width the line representation of the path should have at a given instance

        Args:
            instance (int, optional): timestamp to calculate the width at. Defaults to 0.

        Returns:
            int: the width the line should have at the given intance
        """
        maxwidth=10
        minwidth=1
        #assumir isto
        speed=self.getCarSpeedNormAtInstance(instance)
        if speed==0:
            return minwidth
        width=max(minwidth,math.ceil(maxwidth/speed))
        return width