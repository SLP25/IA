import pygame
from utils import parseImage,GRAVEL_TRAP_COLOR,TRACK_COLOR,START_COLOR,FINISH_COLOR
from Exceptions import POP, QUIT

class PerCarView():
    
    def __init__(self,screen,cars,ImagePath='final.png'):
        self.finalImage=ImagePath
        
        self.screen=screen
        self.cars=cars
        
        self.maxCar=len(cars)-1
        self.currCar= -1 if self.maxCar==-1 else 0 #if non existing cars then -1 else 0
        
        self._drawInit_()
    
    def _drawInit_(self):
        backGroundImage = pygame.image.load(self.finalImage)
        
        self.trackmask=pygame.mask.from_threshold(backGroundImage, TRACK_COLOR,threshold=(1,1,1)).outline()
        self.startmask=pygame.mask.from_threshold(backGroundImage,START_COLOR,threshold=(1,1,1) ).outline()
        self.finishmask=pygame.mask.from_threshold(backGroundImage,FINISH_COLOR,threshold=(1,1,1)).outline()
        
        
        
        
    def _drawCarLines_(self,car,timelinePos):
        pygame.draw.line(self.screen,car.color,car.coords[timelinePos-1],car.coords[timelinePos],width=car.getCarLineWidthAtInstance(timelinePos))

    
    def _drawTrackComponent_(self,color,mask):
        pygame.draw.polygon(self.screen,color,mask,width=12)
        pygame.draw.polygon(self.screen,color,mask,width=0)
        
        
    def _eventHandler_(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.currCar>0: # so it can't go below the start
                        self.currCar-=1
                if event.key == pygame.K_RIGHT:
                    if self.currCar<self.maxCar: # so it can't go over the finish
                            self.currCar+=1
                if event.key == pygame.K_q:
                    raise QUIT()
                if event.key == pygame.K_ESCAPE:
                    raise POP()
        
    def draw(self):
        self.screen.fill(pygame.Color(GRAVEL_TRAP_COLOR))
        self._drawTrackComponent_(TRACK_COLOR,self.trackmask)
        self._drawTrackComponent_(FINISH_COLOR,self.finishmask)
        self._drawTrackComponent_(START_COLOR,self.startmask)
        
        self._eventHandler_()
        car=self.cars[self.currCar]
        pygame.draw.circle(self.screen,car.color,car.getCarPosAtInstance(-1), 5)
        for i in range(1,len(car.coords)):
            self._drawCarLines_(car,i)