import os
import pygame
from Exceptions import POP,QUIT,SIMULATIONVIEW

UNSELECTED=(255,255,255)
SELECTED=(100,100,255)

class Menu():
    def __init__(self,title:str,options=[('None','None')]):
        self.title=title
        self.options=options
        self.curr=0
    def next(self):
        if self.curr==len(self.options)-1:
            self.curr=0
        else:
            self.curr+=1
    def prev(self):
        if self.curr==0:
            self.curr=len(self.options)-1
        else:
            self.curr-=1
    def __str__(self):
        return f"{self.title}: {self.options[self.curr][0]}"
    def value(self):
        return self.options[self.curr][1]
    
        





class MainView():
    def __init__(self,screen):
        self.screen=screen
        self._get_Tracks_()
        self._set_alg_()
        self.menus=[
            Menu("track",self.tracks),
            Menu("algorithm",self.algorithms),
            Menu("Cars",options=[(str(i),str(i)) for i in range(1,100)])
        ]
        self.currMenu=0
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        pass
    
    def _eventHandler_(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.menus[self.currMenu].prev()
                if event.key == pygame.K_RIGHT:
                    self.menus[self.currMenu].next()
                if event.key == pygame.K_UP:
                    self.prev()
                if event.key == pygame.K_DOWN:
                    self.next()
                if event.key == pygame.K_q:
                    raise QUIT()
                if event.key == pygame.K_ESCAPE:
                    raise POP()
                if event.key == pygame.K_RETURN:
                    raise SIMULATIONVIEW()

    
    def next(self):
        if self.currMenu==len(self.menus)-1:
            self.currMenu=0
        else:
            self.currMenu+=1
    
    def prev(self):
        if self.currMenu==0:
            self.currMenu=len(self.menus)-1
        else:
            self.currMenu-=1
    
    
    
    def _get_Tracks_(self):
        self.tracks=[]
        with os.scandir('gui/circuits/') as circuits:
            for circuit in circuits:
                print(circuit)
                name=circuit.name
                trackName=name.split('.')[0]
                self.tracks.append((trackName,f'gui/circuits/{name}'))
    def _set_alg_(self):
        self.algorithms=[
            ("bfs","algfunc"),
        ]
    def getTrackMenuValue(self):
        return self.menus[0].value()
        
    def _showMenu_(self,menu,color,pos):
        text = self.font.render(str(menu), True,color)
        textRect = text.get_rect()
        textRect.center = (500, 40*(pos+1))
        self.screen.blit(text, textRect)
    
    def draw(self):
        self.screen.fill(pygame.Color(50,50,50))
        for pos,menu in enumerate(self.menus):
            self._showMenu_(menu,SELECTED if pos==self.currMenu else UNSELECTED,pos)
        self._eventHandler_()
        