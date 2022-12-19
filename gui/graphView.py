import pygame
from .exceptions import POP,QUIT
class GraphView():
    """
        The view class to show individual cars on track and their statistics
    """
    def __init__(self,screen,car,trackComponents):
        """creates an instance of the GraphView class

        Args:
            screen (Pygame display): the screen were to draw
            car (Car): the car to be drawn
            trackComponents (surface): the background surface of the track
        """
        self.trackComponents=trackComponents
        
        self.screen=screen
        self.car=car
        self.pos=0
    
    def _eventHandler_(self):
        """Handles keyboard event within the view

        Raises:
            QUIT: quits the application
            POP: goes to the previous view
        """
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.pos>0: # so it can't go below the start
                self.pos-=1
        if keys[pygame.K_RIGHT]:
            if self.pos<len(self.car.getGraphCoords()): # so it can't go over the finish
                    self.pos+=1

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_r:
                    self.__init__(self.screen,self.car,self.trackComponents)
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
        pygame.draw.circle(self.screen, self.car.color, self.car.getGraphPosAtInstance(self.pos), 5)
        
                
                