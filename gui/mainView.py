import os
import pygame

from algorithms.iterative_dfs import ITERATIVE_DFS
from .exceptions import POP,QUIT,SIMULATIONVIEW
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.greedy import GREEDY
from algorithms.a_star import A_STAR

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
    """
        the view with the menus for selection to simulate
    """
    def __init__(self,screen):
        """creates a instance of mainView class

        Args:
            screen (Pygame Display): the display were to draw the menus
        """
        self.screen=screen
        self.__get_Tracks__()
        self.__set_alg__()
        self.menus=[
            Menu("track",self.tracks),
            Menu("algorithm",self.algorithms),
            Menu("Cars",options=[(str(i),i) for i in range(1,100)])
        ]
        self.currMenu=0
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.error=None
    
    def __eventHandler__(self):
        """Handler for keyboard events

        Raises:
            QUIT: quit the application
            POP: goes back to the previous 
            SIMULATIONVIEW: goes to the view of all cars simulation
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    self.error=None
                    self.menus[self.currMenu].prev()
                if event.key==pygame.K_RIGHT:
                    self.error=None
                    self.menus[self.currMenu].next()
                if event.key==pygame.K_UP:
                    self.error=None
                    self.prev()
                if event.key==pygame.K_DOWN:
                    self.error=None
                    self.next()
                if event.key==pygame.K_r:
                    self.__init__(self.screen)
                if event.key==pygame.K_q:
                    raise QUIT()
                if event.key==pygame.K_ESCAPE:
                    raise POP()
                if event.key==pygame.K_RETURN:
                    raise SIMULATIONVIEW()

    def setError(self,error:str):
        """sets the error to show

        Args:
            error (str): the error to show
        """
        self.error=str(error)
    
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
    
    
    
    def __get_Tracks__(self):
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
    
    def __set_alg__(self):
        """
           Defines the algorithm names and values
        """
        self.algorithms=[
            ("breath-first-search",BFS()),
            ("depth-first-search",DFS()),
            ("greedy",GREEDY()),
            ("a_star",A_STAR()),
            ("iterative-depth-first-search",ITERATIVE_DFS())
        ]
    def getTrackMenuValue(self):
        """Get the value in the current position of the track menu

        Returns:
            Any: the value of the current option of the track menu
        """
        return self.menus[0].value()
    def getAlgorithmMenuValue(self):
        """Get the value in the current position of the algorithm menu

        Returns:
            Any: the value of the current option of the algorithm menu
        """
        return self.menus[1].value()
    def getNCarsMenuValue(self):
        """Get the value in the current position of the number of cars menu

        Returns:
            Any: the value of the current option of the number of cars menu
        """
        return self.menus[2].value()
        
    def __showMenu__(self,menu,color,pos):
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
    
    
    def __showError__(self):
        """
            shows errors on screen
        """
        if self.error:
            text = self.font.render(self.error, True, (255,0,0))
            textRect = text.get_rect()
            textRect.center = (500, 250)
            self.screen.blit(text, textRect)
        
    
    def draw(self):
        """
           draws the Menus in the display
           handles keyboard events
        """
        self.screen.fill(pygame.Color(50,50,50))
        for pos,menu in enumerate(self.menus):
            self.__showMenu__(menu,SELECTED if pos==self.currMenu else UNSELECTED,pos)
        self.__showError__()
        
        self.__eventHandler__()
        