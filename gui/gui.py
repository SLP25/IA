import pygame

from threading import Thread
from .simulationView import SimulationView
from .perCarView import PerCarView
from .mainView import MainView
from .graphView import GraphView
from .exceptions import POP,QUIT,PERCARVIEW,SIMULATIONVIEW,GRAPHVIEW
from graph.exceptions import InvalidCircuit
import sys
        
audios={
    MainView:'gui/audios/main.mp3',
    SimulationView:'gui/audios/simulation.mp3',
    PerCarView:'gui/audios/perCar.mp3'
}
AUDIO=False

sys.setrecursionlimit(10**6)


class GUI:
    """
       Class for the handler of the multiple views
    """
    def __init__(self):
        """
           creates a new object of the GUI Class
        """
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((100*16,50*16))
        self.views=[]
        if AUDIO:
            pygame.mixer.init()
            pygame.mixer.music.set_volume(1)
            self.playing=""
        
        
        self.views.append(MainView(self.screen))               
        
    def __run__(self):
        """
           Main function to run the loop to show the graphics and the simulation
        """
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((100*16,50*16))
        pygame.mouse.set_visible(1)
        while self.running:
            self.clock.tick(20)
            if len(self.views)==0:
                break
            try:
                if AUDIO:
                    if self.playing!=audios[type(self.views[-1])]:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(audios[type(self.views[-1])])
                        self.playing=audios[type(self.views[-1])]
                        pygame.mixer.music.play(-1)
                self.views[-1].draw()
            except POP:
                self.views.pop()
            except QUIT:
                break
            except PERCARVIEW:
                p=PerCarView(self.screen,self.views[-1].cars,self.views[-1].getTrackComponents())
                self.views.append(p)
            except GRAPHVIEW:
                g=GraphView(self.screen,self.views[-1].cars[self.views[-1].currCar],self.views[-1].trackComponents)
                self.views.append(g)
            except SIMULATIONVIEW:
                try:
                    self.views.append(SimulationView(self.screen,self.views[-1].getAlgorithmMenuValue(),self.views[-1].getNCarsMenuValue(),self.views[-1].getTrackMenuValue()))
                except Exception as e:
                    self.views[-1].setError(e)
            pygame.display.update()
            pygame.event.clear()
        sys.exit()
                                 
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