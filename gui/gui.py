import pygame

from threading import Thread
from .car import Car,generateRandomColor
from .simulationView import SimulationView
from .perCarView import PerCarView
from .mainView import MainView
from .exceptions import POP,QUIT,PERCARVIEW,SIMULATIONVIEW
import sys
        
            

sys.setrecursionlimit(10**6)


class GUI:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1000,500))
        self.views=[]
        
        
        self.views.append(MainView(self.screen))               
        
    def __run__(self):
        """
           Main function to run the loop to show the graphics and the simulation
        """
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1000,500))
        pygame.mouse.set_visible(1)
        while self.running:
            self.clock.tick(20)
            if len(self.views)==0:
                pygame.QUIT()
                self.running=False
            try:
                self.views[-1].draw()
            except POP:
                self.views.pop()
            except QUIT:
                pygame.QUIT()
                self.running=False
            except PERCARVIEW:
                p=PerCarView(self.screen,self.views[-1].cars,self.views[-1].getTrackComponents())
                self.views.append(p)
            except SIMULATIONVIEW:
                self.views.append(SimulationView(self.screen,self.views[-1].getAlgorithmMenuValue(),self.views[-1].getNCarsMenuValue(),self.views[-1].getTrackMenuValue()))
                
            pygame.display.update()
            pygame.event.clear()
                                 
    def run(self):
        """
           Creates a thread to run the application in
        """
        self.running=True
        self.thread = Thread(target=self.__run__,args=())
        self.thread.start()
        
    def stop(self):
        """
           Stops the thread running the application
        """
        self.running=False
        self.thread.join()

    


g=GUI()

g.run()