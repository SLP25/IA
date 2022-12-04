import pygame
from .exceptions import POP, QUIT
from graph.car import Car

class PerCarView():
    """
        The view class to show individual cars on track and their statistics
    """
    def __init__(self,screen,cars,trackComponents):
        """creates an instance of the PerCarView class

        Args:
            screen (Pygame display): the screen were to draw
            cars (list): a list of all cars to be drawn
            trackComponents (surface): the background surface of the track
        """
        self.font = pygame.font.SysFont('Comic Sans MS', 12)
        self.trackComponents=trackComponents
        
        self.screen=screen
        self.cars=cars
        
        self.maxCar=len(cars)-1
        self.currCar= -1 if self.maxCar==-1 else 0 #if non existing cars then -1 else 0
        

        
    def _drawCarLines_(self,car:Car,timelinePos):
        """Draws the line of the car moving in a given timestamp

        Args:
            car (Car): the car being drawn
            timelinePos (int): the timestamp of the current line to draw
        """
        pygame.draw.line(self.screen,car.color,car.getCarPosAtInstance(timelinePos-1),car.getCarPosAtInstance(timelinePos),width=car.getCarLineWidthAtInstance(timelinePos))
        
        
    def _eventHandler_(self):
        """Handler for keyboard events

        Raises:
            QUIT: exists the aplication
            POP: exists the given view
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    if self.currCar>0: # so it can't go below the start
                        self.currCar-=1
                if event.key==pygame.K_RIGHT:
                    if self.currCar<self.maxCar: # so it can't go over the finish
                            self.currCar+=1
                if event.key==pygame.K_r:                    
                    self.__init__(self.screen, self.cars, self.trackComponents)
                if event.key==pygame.K_q:
                    raise QUIT()
                if event.key==pygame.K_ESCAPE:
                    raise POP()
                
    def _drawStat_(self,text,pos):
        """Shows a text on the left at the given y pos with the currCar color

        Args:
            text (string): the text to show
            pos (int): the Y coord to show the stat in
        """
        text = self.font.render(text, True,self.cars[self.currCar].color)
        textRect = text.get_rect()
        textRect.center = (40,pos)
        self.screen.blit(text, textRect)
        
    def _drawStats_(self):
        """
           Draws in the image all the statistics about the car
        """
        car=self.cars[self.currCar]
        self._drawStat_(f"Distance:{car.cost:.2f}",10)
        self._drawStat_(f"TopSpeed:{car.getTopSpeed():.2f}",25)
        self._drawStat_(f"AvgSpeed:{car.getAverageSpeed():.2f}",40)
        self._drawStat_(f"MedSpeed:{car.getMedian():.2f}",55)
        self._drawStat_(f"StdSpeed:{car.getStd():.2f}",70)
        self._drawStat_(f"VarSpeed:{car.getVar():.2f}",85)
        self._drawStat_(f"P25Speed:{car.get25Percentil():.2f}",100)
        self._drawStat_(f"P50Speed:{car.get50Percentil():.2f}",115)
        self._drawStat_(f"P75Speed:{car.get75Percentil():.2f}",130)
        
    def draw(self):
        """
           Draws the background,components,track
           Handles keyboard events given and draws the car with its path
        """
        self.screen.blit(self.trackComponents, (0,0))
        self._drawStats_()
        
        self._eventHandler_()
        car=self.cars[self.currCar]
        pygame.draw.circle(self.screen,car.color,car.getCarPosAtInstance(-1), 5)
        for i in range(1,len(car.coords)):
            self._drawCarLines_(car,i)