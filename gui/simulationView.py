import pygame
from .utils import parseImage,GRAVEL_TRAP_COLOR,TRACK_COLOR,START_COLOR,FINISH_COLOR
from .exceptions import POP, QUIT,PERCARVIEW
from .car import Car,generateRandomColor
import random

from graph.node import Node
import graph.graph_parser as gp

class SimulationView():
    def __init__(self,screen,algorithm,nCars,inputImagePath,outputImagePath='final.png'):

        self.inputImage=inputImagePath
        self.finalImage=outputImagePath
        self.__generateGraph__()
        
        self.screen=screen
        self.algorithm=algorithm
        self.__simulate__(nCars)
        
        self._drawInit_()
        
    def __simulate__(self,nCars):
        """
           Uses the algorithm in the track to simulate the car
        """
        self.cars=[]
        for i in range(nCars):
            startingNode=random.choice(self.graph.starts)
            cost,nodes = self.algorithm.search(self.graph, Node(startingNode[0], startingNode[1], 0, 0), self.graph.finishes)
            c=Car(0,color=generateRandomColor(),tlen=cost)
            c.fromNodes(nodes)
            self.cars.append(c)
            
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


        
    def __generateGraph__(self):
        """
        generates the graph from the input image
        """
        matrix = parseImage(self.inputImage,self.finalImage)
        self.graph=gp.circuit_from_matrix(matrix)
        
        
        
    def getExportedFile(self):
        """Gets the path to the background image

        Returns:
            string: the path to the 
        """
        return self.finalImage
    
    def _drawInit_(self):
        """
           creates mask for the track components and defines max timeline position
        """
        backGroundImage = pygame.image.load(self.finalImage)
        
        self.trackmask=pygame.mask.from_threshold(backGroundImage, TRACK_COLOR,threshold=(1,1,1)).outline()
        self.startmask=pygame.mask.from_threshold(backGroundImage,START_COLOR,threshold=(1,1,1) ).outline()
        self.finishmask=pygame.mask.from_threshold(backGroundImage,FINISH_COLOR,threshold=(1,1,1)).outline()
        
        self.timelineCurrPos=0
        self.maxTimelinePos=0
        if self.cars:
            self.maxTimelinePos = max(map(lambda car: len(car.coords)-1,self.cars))
        
        
        
        
    def _drawCarLines_(self,car,timelinePos):
        """Draws the path lines for a car at a given timestamp

        Args:
            car (Car): the car whose path should be drawn
            timelinePos (int): the timestamp of the line to draw
        """
        if timelinePos<len(car.coords):
            pygame.draw.line(self.screen,car.color,car.coords[timelinePos-1],car.coords[timelinePos],width=car.getCarLineWidthAtInstance(timelinePos))

    
    def _drawTrackComponent_(self,color,mask):
        """Draws a track component from a mask and color

        Args:
            color (Pygame Color): color of the track component
            mask (Pygame Masks): the mask to fill with the color
        """
        pygame.draw.polygon(self.screen,color,mask,width=6)
        pygame.draw.polygon(self.screen,color,mask,width=0)
        
        
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
            self.__init__(self.screen,self.cars,self.inputImage,self.finalImage)
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
        self.screen.fill(pygame.Color(GRAVEL_TRAP_COLOR))
        self._drawTrackComponent_(TRACK_COLOR,self.trackmask)
        self._drawTrackComponent_(FINISH_COLOR,self.finishmask)
        self._drawTrackComponent_(START_COLOR,self.startmask)
        
        self._eventHandler_()
        
        for car in self.cars:
            pygame.draw.circle(self.screen,car.color,car.getCarPosAtInstance(self.timelineCurrPos), 5)
            self.__draw_speed_arrow_(car)
            if self.timelineCurrPos!=0:
                for i in range(1,self.timelineCurrPos+1):
                    self._drawCarLines_(car,i)