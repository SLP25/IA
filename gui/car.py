import random
import math
import numpy as np
def generateRandomColor():
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
    
    def __init__(self,id,color,pos=[],speeds=[],tlen=0):
        self.id=id
        self.color=color
        self.tlen=tlen
        self.coords=pos
        self.speedinCoords=speeds
        self.npVspeed=np.array(list(map(self.__vectorNorm__,self.speedinCoords)))
    
    def getCarPosAtInstance(self,instance=0):
        return self.coords[instance]
    
    def getTopSpeed(self):
        return np.amax(self.npVspeed)
    def getAverageSpeed(self):
        return np.mean(self.npVspeed)
    def getMedian(self):
        return np.median(self.npVspeed)
    def getStd(self):
        return np.std(self.npVspeed)
    def getVar(self):
        return np.var(self.npVspeed)
    def get25Percentil(self):
        return np.percentile(self.npVspeed,25)
    def get50Percentil(self):
        return np.percentile(self.npVspeed,50)
    def get75Percentil(self):
        return np.percentile(self.npVspeed,75)
        
    
        
    
    def __vectorNorm__(self,vector):
        return math.sqrt(sum(map(lambda x: math.pow(x,2),vector)))
        
    
    def getCarSpeedNormAtInstance(self,instance=0):
        return self.__vectorNorm__(self.speedinCoords[instance])
    
    def getCarLineWidthAtInstance(self,instance=0):
        maxwidth=10
        minwidth=1
        #assumir isto
        speed=self.getCarSpeedNormAtInstance(instance)
        if speed==0:
            return minwidth
        width=max(minwidth,math.ceil(maxwidth/speed))
        return width