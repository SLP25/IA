import random
import math
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
    
    def getCarPosAtInstance(self,instance=0):
        return self.coords[instance]
    
    def getTopSpeed(self):
        if self.topSpeed==None:
            self.topSpeed=max(map(self.__vectorNorm__,self.speedinCoords))
        return self.topSpeed
    def getAverageSpeed(self):
        if self.averageSpeed==None:
            self.averageSpeed=sum(map(self.__vectorNorm__,self.speedinCoords))/len(self.speedinCoords)
        return self.averageSpeed
        
    
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