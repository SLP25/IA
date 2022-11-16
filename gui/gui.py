import pygame

from threading import Thread
from car import Car,generateRandomColor
from SimulationView import SimulationView
from perCarView import PerCarView
from mainView import MainView
from Exceptions import POP,QUIT,PERCARVIEW,SIMULATIONVIEW

        
            




class GUI:
    def __init__(self,cars=[]):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1000,500))
        self.views=[]
        self.cars=cars
        
        
        self.views.append(MainView(self.screen))               
        
    def __run__(self):
        """
           Main function to run the loop to show the graphics and the simulation
        """
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1000,500))
        pygame.mouse.set_visible(1)
        while self.running:
            self.clock.tick(60)
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
                p=PerCarView(self.screen,self.cars,self.views[-1].getExportedFile())
                self.views.append(p)
            except SIMULATIONVIEW:
                s=SimulationView(self.screen,self.cars,self.views[-1].getTrackMenuValue(),'final.png')
                self.views.append(s)
                
                
            pygame.display.update()
                                 
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

    


everything=[(24, 46, 0, 0), (23, 46, -1, 0), (21, 47, -2, 1), (18, 47, -3, 0), (14, 47, -4, 0), (11, 47, -3, 0), (9, 47, -2, 0), (8, 46, -1, -1), (8, 44, 0, -2), (9, 41, 1, -3), (9, 38, 0, -3), (8, 34, -1, -4), (8, 30, 0, -4), (9, 25, 1, -5), (10, 19, 1, -6), (11, 12, 1, -7), (13, 5, 2, -7), (13, 5, 0, 0), (14, 4, 1, -1), (16, 4, 2, 0), (18, 4, 2, 0), (19, 5, 1, 1), (20, 6, 1, 1), (22, 8, 2, 2), (25, 10, 3, 2), (28, 12, 3, 2), (30, 13, 2, 1), (32, 14, 2, 1), (34, 14, 2, 0), (35, 15, 1, 1), (36, 17, 1, 2), (36, 20, 0, 3), (36, 22, 0, 2), (37, 23, 1, 1), (39, 24, 2, 1), (41, 25, 2, 1), (41, 25, 0, 0), (41, 26, 0, 1), (42, 26, 1, 0), (43, 26, 1, 0), (43, 27, 0, 1), (44, 27, 1, 0), (46, 28, 2, 1), (48, 29, 2, 1), (50, 31, 2, 2), (50, 31, 0, 0), (49, 32, -1, 1), (47, 32, -2, 0), (45, 32, -2, 0), (42, 32, -3, 0), (38, 31, -4, -1), (33, 31, -5, 0), (29, 30, -4, -1), (25, 30, -4, 0), (21, 31, -4, 1), (18, 33, -3, 2), (18, 33, 0, 0), (19, 34, 1, 1), (21, 35, 2, 1), (24, 35, 3, 0), (28, 36, 4, 1), (33, 36, 5, 0), (39, 36, 6, 0), (46, 35, 7, -1), (54, 35, 8, 0), (63, 36, 9, 1), (72, 36, 9, 0), (72, 36, 0, 0), (72, 35, 0, -1), (72, 33, 0, -2), (72, 30, 0, -3), (71, 28, -1, -2), (69, 27, -2, -1), (66, 26, -3, -1), (63, 25, -3, -1), (60, 24, -3, -1), (58, 23, -2, -1), (57, 21, -1, -2), (56, 19, -1, -2), (56, 16, 0, -3), (56, 14, 0, -2), (57, 12, 1, -2), (59, 9, 2, -3), (59, 9, 0, 0), (60, 9, 1, 0), (60, 8, 0, -1), (61, 8, 1, 0), (63, 7, 2, -1), (66, 7, 3, 0), (66, 7, 0, 0), (66, 8, 0, 1), (67, 8, 1, 0), (67, 9, 0, 1), (68, 10, 1, 1), (70, 12, 2, 2), (72, 15, 2, 3), (75, 18, 3, 3), (78, 22, 3, 4), (81, 26, 3, 4), (85, 31, 4, 5), (85, 31, 0, 0), (86, 31, 1, 0), (86, 32, 0, 1), (87, 33, 1, 1), (89, 35, 2, 2), (90, 37, 1, 2), (92, 39, 2, 2), (94, 42, 2, 3), (96, 44, 2, 2), (96, 44, 0, 0), (95, 45, -1, 1), (93, 45, -2, 0), (90, 46, -3, 1), (86, 46, -4, 0), (81, 47, -5, 1), (75, 47, -6, 0), (68, 47, -7, 0), (61, 46, -7, -1), (53, 46, -8, 0), (44, 46, -9, 0), (34, 46, -10, 0)]

pos=list(map(lambda x:(x[0]*10,x[1]*10) ,everything))
speeds=list(map(lambda x:(x[2],x[3]) ,everything))
pos2=list(map(lambda x:(x[0]*10+1,x[1]*10) ,everything))

c1=Car(0,color=generateRandomColor(),pos=pos,speeds=speeds,tlen=336)#[(0,0),(1,0),(2,0),(4,0),(8,0)],speeds=[])
c2=Car(0,color=generateRandomColor(),pos=pos2,speeds=speeds,tlen=336)#[(0,0),(1,0),(2,0),(4,0),(8,0)],speeds=[])

g=GUI(cars=[c1,c2])

g.run()