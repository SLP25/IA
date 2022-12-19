import itertools
from .node import Node
import math
import pygame
import numpy as np
import random



class Car():
    """
        The class representing a car

    """
    newid = itertools.count()
    
    def __init__(self,start:Node,name=""):
        """
           Creates a new Car object generating a new random color and a autoincreasing id

        Args:
            start (Node): the Node the car will start on
        """
        self.id = next(Car.newid)
        self.color = self.__generateColor__()
        self.name = name
        self.fullPath=[start]
        self.graphPath=[start]
        self.cost=-1
    
    def getSpeeds(self)->list[tuple[int,int]]:
        """gets a list of the speed vectors in each position of the path

        Returns:
            list[tuple[int,int]]: a list of the speed vectors in each position of the path
        """
        if not hasattr(self,'speed'):
            self.speed=[n.speed() for n in self.fullPath]
        return self.speed
    
    def getCoords(self)->list[tuple[int,int]]:
        """gets a list of the coordenates in each position of the path

        Returns:
            list[tuple[int,int]]: a list of the coordenates in each position of the path
        """
        if not hasattr(self,'coords'):
            self.coords=[n.coords() for n in self.fullPath]
        return self.coords
    def getGraphCoords(self)->list[tuple[int,int]]:
        """gets a list of the coordenates in each position of the graph

        Returns:
            list[tuple[int,int]]: a list of the coordenates in each position of the path
        """
        if not hasattr(self,'graphCoords'):
            self.graphCoords=[n.coords() for n in self.graphPath]
        return self.graphCoords
    def getNpVspeed(self):
        """
            Gets a np array of the speed vector norm in each position of the path

        Returns:
            list[tuple[int,int]]: a list of the speed vector norm in each position of the path
        """
        if not hasattr(self,'npVspeed'):
            self.npVspeed=np.array(list(map(self.__vectorNorm__,self.getSpeeds())))
        return self.npVspeed

    
    
    def getCoordsAtInstance(self,inst:int):
        """
            Gets the coordenates in a position of the path

        Args:
            inst (int): the position of the path to get the coordenates in

        Returns:
            tuple[int,int]: the coordenates pair the intance
        """
        return self.fullPath[inst].coords()
    
    @staticmethod
    def on_segment(p:tuple[int,int], q:tuple[int,int], r:tuple[int,int]):
        """
            Return if a point is contained in a line segment defined by 2 points

        Args:
            p (tuple[int,int]): segment first point
            q (tuple[int,int]): segment second point
            r (tuple[int,int]): the point to check if is contained

        Returns:
            bool: if a point is contained in a line segmen
        """
        if r[0] <= max(p[0], q[0]) and r[0] >= min(p[0], q[0]) and r[1] <= max(p[1], q[1]) and r[1] >= min(p[1], q[1]):
            return True
        return False
    
    @staticmethod    
    def orientation(p:tuple[int,int], q:tuple[int,int], r:tuple[int,int]):
        """
            Returns the orientation of a point in a reference to a semi lines defined by 2 points

        Args:
            p (tuple[int,int]): segment first point
            q (tuple[int,int]): segment second point
            r (tuple[int,int]): the point to check the orientation

        Returns:
            int: -1 if is to the left, 0 if is in line and 1 to the right
        """
        val = ((q[1] - p[1]) * (r[0] - q[0])) - ((q[0] - p[0]) * (r[1] - q[1]))
        if val == 0 : return 0
        return 1 if val > 0 else -1
    @staticmethod
    
    def intersects(p1:tuple[int,int], q1:tuple[int,int], p2:tuple[int,int], q2:tuple[int,int]):
        """
            Checks if 2 line segments define by 2 points each intersect at some point

        Args:
            p1 (tuple[int,int]): the first point of the first line segment
            q1 (tuple[int,int]): the second point of the first line segment
            p2 (tuple[int,int]): the first point of the second line segment
            q2 (tuple[int,int]): the second point of the second line segment

        Returns:
            bool: True if they intersect, False if otherwise
        """
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
    
    

    def colides(self,coordsI:tuple[int,int],coordsF:tuple[int,int],itI:int):
        """
            Checks if the movement between 2 coordenates at a given moment would colide with the car

        Args:
            coordsI (tuple[int,int]): the starting position of the movement
            coordsF (tuple[int,int]): the desitation position of the movement
            itI (int): the moment at which the movement is being done

        Returns:
            bool: wheather a colision will occor
        """
        if itI==0 or itI >= len(self.fullPath)-2 or coordsI==coordsF:#is in the start,finish or not moving
            return False
        A=coordsI
        B=coordsF
        C=self.getCoordsAtInstance(itI)
        D=self.getCoordsAtInstance(itI+1)
        if B==D: return True
        return Car.intersects(A,B,C,D)
        
    def setPath(self,l:list):
        """
            Sets the list of nodes the car travels through

        Args:
            l (list): the list of nodes to store as the path of the car
        """
        self.fullPath=l.copy()
        
    def getLastNode(self):
        """
            Gets the last node in the list of the nodes the car traveld through

        Returns:
            Node: the last node in the list of the nodes the car traveld through
            None: if the list is empty
        """
        if self.fullPath:
            return self.fullPath[-1]
        return None
    
    #gui
    @staticmethod
    def toGuiSize(tup:tuple[int,int]):
        """
            Returns a tuple with the gui representation size (16*bigger)

        Args:
            tup (tuple[int,int]): the input tuple

        Returns:
            tuple[int,int]: the enlarged tuple
        """
        return (8+16*tup[0],8+16*tup[1])
    
    def __generateColor__(self):
        """
            Generates a random color under the rgb format

        Returns:
            tuple[int,int,int]: tuple with the rgb values
        """
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
    
    def getGraphPosAtInstance(self,instance=0):
        """gets the coordenats the car is at in a given instance

        Args:
            instance (int, optional): timestamp to get position at. Defaults to 0.

        Returns:
            tuple: a tuple with the coordnats at that instance
        """
        if instance>len(self.getGraphCoords())-1:
            instance=-1
        return self.toGuiSize(self.getGraphCoords()[instance])
    
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
    
    def __draw_speed_arrow__(self,screen,position):
        
        body_width=4
        head_width=8
        
        start=pygame.math.Vector2(self.getCarPosAtInstance(position))
        speed=pygame.math.Vector2(self.getCarSpeedAtInstance(position))*16#sinse the speeds are in the 50*100 representation not upscaled
        end=start+speed
        
        arrow = start - end
        angle = arrow.angle_to(pygame.Vector2(0, -1))
        
        body_length = arrow.length() *0.8
        head_height = arrow.length() *0.2
        
        # Vector for the arrow head
        head_verts = [
            pygame.Vector2(0, head_height / 2),  # Center
            pygame.Vector2(head_width / 2, -head_height / 2),  # Bottomright
            pygame.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
        ]
        # rotation of the head to match the speed direction
        translation = pygame.Vector2(0, arrow.length() - (head_height / 2)).rotate(-angle)
        for i in range(len(head_verts)):
            head_verts[i].rotate_ip(-angle)
            head_verts[i] += translation
            head_verts[i] += start
    
        #draw head
        pygame.draw.polygon(screen, self.color, head_verts)
    
        # Stop weird shapes when the arrow is shorter than arrow head
        if arrow.length() >= head_height:
            # Vector for the arrow body
            body_verts = [
                pygame.Vector2(-body_width / 2, body_length / 2),  # Topleft
                pygame.Vector2(body_width / 2, body_length / 2),  # Topright
                pygame.Vector2(body_width / 2, -body_length / 2),  # Bottomright
                pygame.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
            ]
            # rotation of the body to match the speed direction
            translation = pygame.Vector2(0, body_length / 2).rotate(-angle)
            for i in range(len(body_verts)):
                body_verts[i].rotate_ip(-angle)
                body_verts[i] += translation
                body_verts[i] += start
            #draw body
            pygame.draw.polygon(screen, self.color, body_verts)

    def __draw_name__(self,screen,position):
        font = pygame.font.SysFont('Comic Sans MS', 12)
        text = font.render(self.name, True,self.color)
        
        x,y=self.getCarPosAtInstance(position)
        text_width, text_height = font.size(self.name)
        y+=10
        textRect = text.get_rect()
        textRect.center = (x, y)
        screen.blit(text, textRect)
        
    
    def __drawCarLines__(self,screen,timelinePos):
        """Draws the path lines for a car at a given timestamp
        Args:
            car (Car): the car whose path should be drawn
            timelinePos (int): the timestamp of the line to draw
        """
        if timelinePos<len(self.getCoords()):
            pygame.draw.line(screen,self.color,self.getCarPosAtInstance(timelinePos-1),self.getCarPosAtInstance(timelinePos),width=self.getCarLineWidthAtInstance(timelinePos))

    
    
    def drawPath(self,screen,position):
        pygame.draw.circle(screen,self.color,self.getCarPosAtInstance(position), 5)
        self.__draw_name__(screen,position)
        self.__draw_speed_arrow__(screen,position)
        if position!=0:
            for i in range(1,position+1):
                self.__drawCarLines__(screen, i)


    
    
    
    
    

    