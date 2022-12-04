import pygame
from .utils import GRAVEL_TRAP_COLOR,TRACK_COLOR,START_COLOR,FINISH_COLOR
from .exceptions import POP, QUIT,PERCARVIEW
from graph.car import Car
import random
import time

from graph.node import Node
import graph.graph_parser as gp

class SimulationView():
    """
       the view to show the simulation ocuring
    """
    def __init__(self,screen,algorithm,nCars,inputImagePath):
        self.mapSize=(100,50)
        self.desiredSize=(1000,500)
        self.inputImage=inputImagePath
        self.screen=screen
        self._drawInit_()
        self.graph=gp.circuit_from_matrix(self.matrix)
        self.nCars=nCars
        

        self.algorithm=algorithm
        self.__simulate__(nCars)
        

        
    def __simulate__(self,nCars):
        """
           Uses the algorithm in the track to simulate the car
        """
        self.timelineCurrPos=0
        self.maxTimelinePos=0
        self.cars=[]
        startingNodes=random.choices(self.graph.starts,k=nCars)
        for i in range(nCars):
            self.cars.append(Car(Node(startingNodes[i][0],startingNodes[i][1],0,0)))
            
        self.algorithm.search(self.graph,self.cars, self.graph.finishes)
        self.maxTimelinePos=max(map(lambda c:len(c.fullPath),self.cars))

            
    def __draw_speed_arrow_(self,car):
        """Draws in the screen a arrow representing the speed vector of a given car at the current timeline moment

        Args:
            car (Car): the car to get the speed from
        """

        body_width=4
        head_width=8
        
        start=pygame.math.Vector2(car.getCarPosAtInstance(self.timelineCurrPos))
        speed=pygame.math.Vector2(car.getCarSpeedAtInstance(self.timelineCurrPos))*10#sinse the speeds are in the 50*100 representation not upscaled
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
        pygame.draw.polygon(self.screen, car.color, head_verts)
    
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
            pygame.draw.polygon(self.screen, car.color, body_verts)
        
        
        
    def getTrackComponents(self):
        """Gets the surface of the track

        Returns:
            Pygame.Surface: the surface of the track
        """
        return self.trackComponents
    
    def _drawInit_(self):
        """
           creates surfaces for the track components and defines max timeline position
        """
        image =  pygame.image.load(self.inputImage)
        resized_image=pygame.transform.scale(image,self.mapSize)
        greens=pygame.mask.from_threshold(resized_image,(0,255,0),threshold=(30, 50, 30, 255))
        reds=pygame.mask.from_threshold(resized_image,(255,0,0),threshold=(50, 30, 30, 255))
        blacks=pygame.mask.from_threshold(resized_image,(0,0,0),threshold=(100, 100, 100, 255))
        
        self.trackComponents=pygame.Surface(self.mapSize)
        self.matrix=[]
        for r in range(self.mapSize[1]):
            f=''
            for c in range(self.mapSize[0]):
                if greens.get_at((c,r)):
                    f+='P'
                    self.trackComponents.set_at((c, r), START_COLOR)
                elif reds.get_at((c,r)):
                    f+='F'
                    self.trackComponents.set_at((c, r), FINISH_COLOR)
                elif blacks.get_at((c,r)):
                    f+='-'
                    self.trackComponents.set_at((c, r), TRACK_COLOR)
                else:
                    f+='X'
                    self.trackComponents.set_at((c, r), GRAVEL_TRAP_COLOR)
            self.matrix.append(f)
        self.trackComponents=pygame.transform.scale(self.trackComponents,self.desiredSize)
        
        
        
        
    def _drawCarLines_(self,car:Car,timelinePos):
        """Draws the path lines for a car at a given timestamp

        Args:
            car (Car): the car whose path should be drawn
            timelinePos (int): the timestamp of the line to draw
        """
        if timelinePos<len(car.coords):
            pygame.draw.line(self.screen,car.color,car.getCarPosAtInstance(timelinePos-1),car.getCarPosAtInstance(timelinePos),width=car.getCarLineWidthAtInstance(timelinePos))


    def _eventHandler_(self):
        """Handles keyboard event within the view

        Raises:
            PERCARVIEW: Goes to the percar view
            QUIT: quits the application
            POP: goes to the previous view
        """
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.timelineCurrPos>0: # so it can't go below the start
                self.timelineCurrPos-=1
        if keys[pygame.K_RIGHT]:
            if self.timelineCurrPos<self.maxTimelinePos: # so it can't go over the finish
                    self.timelineCurrPos+=1

            
        if keys[pygame.K_r]:
            self.__init__(self.screen,self.algorithm,self.nCars,self.inputImage)
        if keys[pygame.K_p]:
            raise PERCARVIEW()
        if keys[pygame.K_q]:
            raise QUIT()
        if keys[pygame.K_ESCAPE]:
            raise POP()
        
    def draw(self):
        """
           Draws the view filling with the background color,the components,handles events and shows the cars up to the current isntance
        """        
        self.screen.blit(self.trackComponents,(0,0))
        self._eventHandler_()
        
        for car in self.cars:
            pygame.draw.circle(self.screen,car.color,car.getCarPosAtInstance(self.timelineCurrPos), 5)
            self.__draw_speed_arrow_(car)
            if self.timelineCurrPos!=0:
                for i in range(1,self.timelineCurrPos+1):
                    self._drawCarLines_(car,i)