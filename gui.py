import pygame
import numpy as np
from PIL import Image,ImageEnhance,ImageFilter
from threading import Thread
import time
from car import Car,generateRandomColor



GRAVEL_TRAP_COLOR = [ 235, 203, 139]
TRACK_COLOR = [52, 58, 64]
START_COLOR = [ 0,255,0]
FINISH_COLOR =[ 255,0,0]


def npArrayToImage(img):
    return Image.fromarray(img)

def imageFromTrackStr(string):
    img=[]
    lines=string.split('\n')
    for line in lines:
        for c in line:
            if c=='X':
                img.append(GRAVEL_TRAP_COLOR)
            elif c=='-':
                img.append(TRACK_COLOR)
            elif c=='P':
                img.append(START_COLOR)
            elif c=='F':
                img.append(FINISH_COLOR)
    npimg=np.uint8(np.array(img))
    newnpimg=npimg.reshape(50,100,3)
    return npArrayToImage(newnpimg)

def increaseColors(image):
    hsv = image.convert('HSV')
    H, S, V = hsv.split()
    V=V.point(lambda p: p*2)
    HSVr = Image.merge('HSV', (H,S,V))
    return HSVr.convert('RGB')

def getImageAsBW(image):
    image=image.convert("1")
    image=image.resize((100,50),Image.Resampling.NEAREST)
    f=[]
    for j in np.array(image):
        f.append(['X' if i else '-' for i in j])
    return f

def reduceToScale(n):
    return n//10

def findStartEnd(image,track):
    pix = np.array(image)
    reduce = np.vectorize(reduceToScale)
    #green
    indices = np.where(np.all(pix == np.array([ 0,255,0], dtype=np.uint8), axis=-1))
    indices=np.dstack(indices)[0]
    indices =reduce(np.round(indices,-1))
    indices = np.unique(indices,axis=0)
    for start in indices:
        track[start[0]][start[1]] = 'P'
    #red
    
    indices = np.where(np.all(pix == np.array([ 255,0,0], dtype=np.uint8), axis=-1))
    
    indices=np.dstack(indices)[0]
    indices =reduce(np.round(indices,-1))
    indices = np.unique(indices,axis=0)
    for finish in indices:
        track[finish[0]][finish[1]] = 'F'
    return track

def convertTrackToString(track):
    f=''
    for row in track:
        for c in row:
            f+=c
        f+='\n'
    return f


def parseImage(path,finalPath):
        image=Image.open(path)
        image=image.resize((1000,500),Image.Resampling.NEAREST)# normalize image to 1000,500
        image=increaseColors(image)# brighten ups to be easier to detect colors
        track = getImageAsBW(image)#black and white to be easier to separate track from walls
        findStartEnd(image,track)#finds red and green spots and generates a tack from it
        s=convertTrackToString(track)# converts the image to a normalized string
        img=imageFromTrackStr(s)#converts the string to a new track without blurred line
        img=img.resize((1000,500),Image.Resampling.NEAREST)#upsample to 1000,500 aka 10x curr size
        img=img.filter(ImageFilter.SHARPEN)#adds a separating line between track and walls
        img.save(finalPath)#saves the image in a file
        return s


class GUI:
    def __init__(self,inputImagePath,outputImagePath='final.png'):
        self.inputImage=inputImagePath
        self.finalImage=outputImagePath
        self.track=parseImage(self.inputImage,self.finalImage)
        self.cars=[]
                
        
    def __run__(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((1000,500))
        bg = pygame.image.load(self.finalImage)
        trackmask=pygame.mask.from_threshold(bg, TRACK_COLOR,threshold=(1,1,1)).outline()
        startmask=pygame.mask.from_threshold(bg,START_COLOR,threshold=(1,1,1) ).outline()
        finishmask=pygame.mask.from_threshold(bg,FINISH_COLOR,threshold=(1,1,1)).outline()
        pygame.mouse.set_visible(1)
        pos=0
        maxpos=0
        if self.cars:
            maxpos = len(self.cars[0].coordsMap)-1
        while self.running:
            clock.tick(60)
            screen.fill(pygame.Color(GRAVEL_TRAP_COLOR))
            
            pygame.draw.polygon(screen,TRACK_COLOR,trackmask,width=12)
            pygame.draw.polygon(screen,TRACK_COLOR,trackmask,width=0)
            
            pygame.draw.polygon(screen,FINISH_COLOR,finishmask,width=12)
            pygame.draw.polygon(screen,FINISH_COLOR,finishmask,width=0)
            
            pygame.draw.polygon(screen,START_COLOR,startmask,width=12)
            pygame.draw.polygon(screen,START_COLOR,startmask,width=0)
        
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        self.running=False
                    if event.key == pygame.K_LEFT:
                        if pos>0:
                            pos-=1
                    if event.key == pygame.K_RIGHT:
                        if pos<maxpos:
                                pos+=1
            for car in self.cars:
                pygame.draw.circle(screen,car.color,car.getCarPosAtInstance(pos), 5)
                if pos!=0:
                    for i in range(1,pos+1):
                        pygame.draw.line(screen,car.color,car.coordsMap[i-1],car.coordsMap[i],width=car.getCarLineWidthAtInstance(i))
            pygame.display.update()
                        
                        
                        
                        
    def run(self):
        self.running=True
        self.thread = Thread(target=self.__run__,args=())
        self.thread.start()
    def stop(self):
        self.running=False
        self.thread.join()
        
    def addCars(self,cars):
        for car in cars:
            car.coordsMap=list(map(lambda x: (x[0]*10,x[1]*10),car.coordsMap))
        self.cars=cars

    
g=GUI(inputImagePath='../bahrain.png')

everything=[(24, 46, 0, 0), (23, 46, -1, 0), (21, 47, -2, 1), (18, 47, -3, 0), (14, 47, -4, 0), (11, 47, -3, 0), (9, 47, -2, 0), (8, 46, -1, -1), (8, 44, 0, -2), (9, 41, 1, -3), (9, 38, 0, -3), (8, 34, -1, -4), (8, 30, 0, -4), (9, 25, 1, -5), (10, 19, 1, -6), (11, 12, 1, -7), (13, 5, 2, -7), (13, 5, 0, 0), (14, 4, 1, -1), (16, 4, 2, 0), (18, 4, 2, 0), (19, 5, 1, 1), (20, 6, 1, 1), (22, 8, 2, 2), (25, 10, 3, 2), (28, 12, 3, 2), (30, 13, 2, 1), (32, 14, 2, 1), (34, 14, 2, 0), (35, 15, 1, 1), (36, 17, 1, 2), (36, 20, 0, 3), (36, 22, 0, 2), (37, 23, 1, 1), (39, 24, 2, 1), (41, 25, 2, 1), (41, 25, 0, 0), (41, 26, 0, 1), (42, 26, 1, 0), (43, 26, 1, 0), (43, 27, 0, 1), (44, 27, 1, 0), (46, 28, 2, 1), (48, 29, 2, 1), (50, 31, 2, 2), (50, 31, 0, 0), (49, 32, -1, 1), (47, 32, -2, 0), (45, 32, -2, 0), (42, 32, -3, 0), (38, 31, -4, -1), (33, 31, -5, 0), (29, 30, -4, -1), (25, 30, -4, 0), (21, 31, -4, 1), (18, 33, -3, 2), (18, 33, 0, 0), (19, 34, 1, 1), (21, 35, 2, 1), (24, 35, 3, 0), (28, 36, 4, 1), (33, 36, 5, 0), (39, 36, 6, 0), (46, 35, 7, -1), (54, 35, 8, 0), (63, 36, 9, 1), (72, 36, 9, 0), (72, 36, 0, 0), (72, 35, 0, -1), (72, 33, 0, -2), (72, 30, 0, -3), (71, 28, -1, -2), (69, 27, -2, -1), (66, 26, -3, -1), (63, 25, -3, -1), (60, 24, -3, -1), (58, 23, -2, -1), (57, 21, -1, -2), (56, 19, -1, -2), (56, 16, 0, -3), (56, 14, 0, -2), (57, 12, 1, -2), (59, 9, 2, -3), (59, 9, 0, 0), (60, 9, 1, 0), (60, 8, 0, -1), (61, 8, 1, 0), (63, 7, 2, -1), (66, 7, 3, 0), (66, 7, 0, 0), (66, 8, 0, 1), (67, 8, 1, 0), (67, 9, 0, 1), (68, 10, 1, 1), (70, 12, 2, 2), (72, 15, 2, 3), (75, 18, 3, 3), (78, 22, 3, 4), (81, 26, 3, 4), (85, 31, 4, 5), (85, 31, 0, 0), (86, 31, 1, 0), (86, 32, 0, 1), (87, 33, 1, 1), (89, 35, 2, 2), (90, 37, 1, 2), (92, 39, 2, 2), (94, 42, 2, 3), (96, 44, 2, 2), (96, 44, 0, 0), (95, 45, -1, 1), (93, 45, -2, 0), (90, 46, -3, 1), (86, 46, -4, 0), (81, 47, -5, 1), (75, 47, -6, 0), (68, 47, -7, 0), (61, 46, -7, -1), (53, 46, -8, 0), (44, 46, -9, 0), (34, 46, -10, 0)]

pos=list(map(lambda x:(x[0],x[1]) ,everything))
speeds=list(map(lambda x:(x[2],x[3]) ,everything))

pos2=list(map(lambda x:(x[0]+1,x[1]) ,everything))


c1=Car(0,color=generateRandomColor(),pos=pos,speeds=speeds)#[(0,0),(1,0),(2,0),(4,0),(8,0)],speeds=[])
c2=Car(0,color=generateRandomColor(),pos=pos2,speeds=speeds)#[(0,0),(1,0),(2,0),(4,0),(8,0)],speeds=[])
g.addCars([c1,c2])
g.run()