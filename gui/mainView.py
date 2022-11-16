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
        """
           moves to the next option
        """
        if self.curr==len(self.options)-1:
            self.curr=0
        else:
            self.curr+=1
    def prev(self):
        """
           moves to the previous option
        """
        if self.curr==0:
            self.curr=len(self.options)-1
        else:
            self.curr-=1
    def __str__(self):
        """
           convert the menu into a string
        """
        return f"{self.title}: {self.options[self.curr][0]}"
    def value(self):
        """gets the value of the current selected option in the menu

        Returns:
            Any: the value of the current selected option
        """
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
        """Handler for keyboard events

        Raises:
            QUIT: quit the application
            POP: goes back to the previous 
            SIMULATIONVIEW: goes to the view of all cars simulation
        """
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
                if event.key == pygame.K_r:
                    self.__init__(self.screen)
                if event.key == pygame.K_q:
                    raise QUIT()
                if event.key == pygame.K_ESCAPE:
                    raise POP()
                if event.key == pygame.K_RETURN:
                    raise SIMULATIONVIEW()

    
    def next(self):
        """
           Set the next menu as selected
        """
        if self.currMenu==len(self.menus)-1:
            self.currMenu=0
        else:
            self.currMenu+=1
    
    def prev(self):
        """
           Set the previous menu as selected
        """
        if self.currMenu==0:
            self.currMenu=len(self.menus)-1
        else:
            self.currMenu-=1
    
    
    
    def _get_Tracks_(self):
        """
           Scans the circuits folder for tracks to simulate in
           Defines the track names and values
        """
        self.tracks=[]
        with os.scandir('gui/circuits/') as circuits:
            for circuit in circuits:
                name=circuit.name
                trackName=name.split('.')[0]
                self.tracks.append((trackName,f'gui/circuits/{name}'))
    
    def _set_alg_(self):
        """
           Defines the algorithm names and values
        """
        self.algorithms=[
            ("bfs","algfunc"),
        ]
    def getTrackMenuValue(self):
        """Get the value in the current position of the track menu

        Returns:
            Any: the value of the current option of the track menu
        """
        return self.menus[0].value()
        
    def _showMenu_(self,menu,color,pos):
        """Displays a Menu in a given color and position

        Args:
            menu (Menu): the menu to display
            color (Pygame Color): the color to show the menu in
            pos (int): the Y position to show the menu in
        """
        text = self.font.render(str(menu), True,color)
        textRect = text.get_rect()
        textRect.center = (500, 40*(pos+1))
        self.screen.blit(text, textRect)
    
    def draw(self):
        """
           draws the Menus in the display
           handles keyboard events
        """
        self.screen.fill(pygame.Color(50,50,50))
        for pos,menu in enumerate(self.menus):
            self._showMenu_(menu,SELECTED if pos==self.currMenu else UNSELECTED,pos)
        self._eventHandler_()
        