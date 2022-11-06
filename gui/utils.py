import numpy as np
from PIL import Image,ImageFilter


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


def parseImage(path,output):
        image=Image.open(path)
        image=image.resize((1000,500),Image.Resampling.NEAREST)# normalize image to 1000,500
        image=increaseColors(image)# brighten ups to be easier to detect colors
        track = getImageAsBW(image)#black and white to be easier to separate track from walls
        findStartEnd(image,track)#finds red and green spots and generates a tack from it
        s=convertTrackToString(track)# converts the image to a normalized string
        img=imageFromTrackStr(s)#converts the string to a new track without blurred line
        img=img.resize((1000,500),Image.Resampling.NEAREST)#upsample to 1000,500 aka 10x curr size
        img=img.filter(ImageFilter.SHARPEN)#adds a separating line between track and walls
        img.save(output)#saves the image in a file
        return s