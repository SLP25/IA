import pygame
from .utils import GRAVEL_TRAP_COLOR,TRACK_COLOR,START_COLOR,FINISH_COLOR,GRAVEL_IMG,TRACK_IMG,START_IMG,FINISH_IMG
from .exceptions import POP, QUIT,PERCARVIEW
from graph.car import Car
import random
import time

from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.greedy import GREEDY
from algorithms.a_star import A_STAR
from algorithms.iterative_dfs import ITERATIVE_DFS
from algorithms.dijkstra import DIJKSTRA

from graph.node import Node
import graph.graph_parser as gp

class SimulationView():
    """
       the view to show the simulation ocuring
    """
    def __init__(self,screen,algorithm,nCars,inputImagePath):
        self.mapSize=(100,50)
        self.progress=0
        self.desiredSize=(100*16,50*16)
        self.xCenter=100*0.5*16
        self.yCenter=50*0.5*16
        if algorithm=='all':
            self.nCars=6
        elif algorithm=='allG':
            self.nCars=5
        else:self.nCars=nCars
        self.algorithm=algorithm
        self.inputImage=inputImagePath
        self.screen=screen
        self.updateProgressBar(0)
        self._drawInit_()        
        self.graph=gp.circuit_from_matrix(self.matrix)
        self.updateProgressBar(0.1)
        self.__simulate__(self.nCars)
        
    def updateProgressBar(self,inc:int):
        """increases the progress bar by a given ammount

        Args:
            inc (int): the percentage to increase the progress bar
        """
        self.progress+=inc
        pygame.draw.lines(self.screen, (129, 126, 123),closed=True,points=[
            (38,self.yCenter-20),
            (100*16-38,self.yCenter-20),
            (100*16-38,self.yCenter+20),
            (38,self.yCenter+20)
            ],width=2)
    
        pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(40,self.yCenter-20,(100*16*self.progress)-80,40))
        pygame.display.update()
        
    def __simulate__(self,nCars):
        """
           Uses the algorithm in the track to simulate the car
        """
        
        avaiableProg=0.9
        
        self.timelineCurrPos=0
        self.maxTimelinePos=0
        self.cars=[]
        startingNodes=random.choices(self.graph.starts,k=nCars)
        if self.algorithm=='all' or self.algorithm=='allG':
            algorithms=[(BFS(),(255, 127, 14)),(DFS(),(31, 119, 180)),(A_STAR(),(44, 160, 44)),(ITERATIVE_DFS(),(148, 103, 189)),(DIJKSTRA(),(140, 86, 75))]
            if self.algorithm=='all': algorithms.append((GREEDY(),(214, 39, 40)))
            random.shuffle(algorithms)
            for i in range(nCars):
                alg,color=algorithms.pop(0)
                self.cars.append(Car(Node(startingNodes[i][0],startingNodes[i][1],0,0)))
                self.cars[-1].color=color
                alg.search(self.graph,i,self.cars, self.graph.finishes)
                self.updateProgressBar(avaiableProg/nCars)
        else:
            for i in range(nCars):
                self.cars.append(Car(Node(startingNodes[i][0],startingNodes[i][1],0,0)))
                self.algorithm.search(self.graph,i,self.cars, self.graph.finishes)
                self.updateProgressBar(avaiableProg/nCars)
            
        self.maxTimelinePos=max(map(lambda c:len(c.fullPath),self.cars))

            
    def __draw_speed_arrow_(self,car):
        """Draws in the screen a arrow representing the speed vector of a given car at the current timeline moment

        Args:
            car (Car): the car to get the speed from
        """

        body_width=4
        head_width=8
        
        start=pygame.math.Vector2(car.getCarPosAtInstance(self.timelineCurrPos))
        speed=pygame.math.Vector2(car.getCarSpeedAtInstance(self.timelineCurrPos))*16#sinse the speeds are in the 50*100 representation not upscaled
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
        
        self.trackComponents=pygame.Surface(self.desiredSize)
        trackImg = pygame.image.load(TRACK_IMG).convert()
        startImg = pygame.image.load(START_IMG).convert()
        finishImg = pygame.image.load(FINISH_IMG).convert()
        gravelImg = pygame.image.load(GRAVEL_IMG).convert()
        self.matrix=[]
        for r in range(self.mapSize[1]):
            f=''
            for c in range(self.mapSize[0]):
                if greens.get_at((c,r)):
                    f+='P'
                    img=startImg
                elif reds.get_at((c,r)):
                    f+='F'
                    img=finishImg
                elif blacks.get_at((c,r)):
                    f+='-'
                    img=trackImg
                else:
                    f+='X'
                    img = gravelImg 
                self.trackComponents.blit(img,(c*16,r*16))
            self.matrix.append(f)
        
        
        
        
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

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_r:
                    self.__init__(self.screen,self.algorithm,self.nCars,self.inputImage)
                if event.key==pygame.K_p:
                    raise PERCARVIEW()
                if event.key==pygame.K_q:
                    raise QUIT()
                if event.key==pygame.K_ESCAPE:
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