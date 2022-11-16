import numpy as np
from PIL import Image,ImageFilter


GRAVEL_TRAP_COLOR = [ 235, 203, 139]
TRACK_COLOR = [52, 58, 64]
START_COLOR = [ 0,255,0]
FINISH_COLOR =[ 255,0,0]


def npArrayToImage(img):
    """Converts an npArray to a PIL image

    Args:
        img (np.array): the np array to convert to PIL Image

    Returns:
        PIL Image : the image representation of the np array
    """
    return Image.fromarray(img)

def imageFromTrackStr(string):
    """Converts the string representation of the track into a 50*100 PIL Image

    Args:
        string (string): the track to convert to an PIL Image

    Returns:
        PIL Image: the image generated
    """
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
    """doubles the brightness of all collors in an rgb image

    Args:
        image (PIL Image): image to increase brightness

    Returns:
        PIL Image: the image with the increased brightness
    """
    hsv = image.convert('HSV')
    H, S, V = hsv.split()
    V=V.point(lambda p: p*2)
    HSVr = Image.merge('HSV', (H,S,V))
    return HSVr.convert('RGB')

def getImageAsBW(image):
    """ Create a String of the Track and the walls from a PIL Image

    Args:
        image (PIL Image): The Pil image to turn into a track

    Returns:
        List[List[String]]: List with the rows (List of each square)
    """
    image=image.convert("1")
    image=image.resize((100,50),Image.Resampling.NEAREST)
    f=[]
    for j in np.array(image):
        f.append(['X' if i else '-' for i in j])
    return f

def reduceToScale(n):
    """Reduzes the scale of a number to the integer division of 10

    Args:
        n (Number): The number to reduce

    Returns:
        Int: The reduced number
    """
    return n//10

def findStartEnd(image,track):
    """Finds the pixeis with Red and Green Coloring and Adds those pixels as starting and ending positions in the track
       Red   -> End
       Green -> Start

    Args:
        image (PIL Image): The PIL Image from where to extract the 
        track (List[List[String]]): The list of lists of characters of the track

    Returns:
        List[List[String]] : The list of lists of characters of the track with the start and end position
    """
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
    """Convert a List of Lists of characters into a \n separated string 

    Args:
        track (List[List[String]]): The List of List Of Characters to convert to a unified string

    Returns:
        String : track representation in \n separated string
    """
    f=''
    for row in track:
        for c in row:
            f+=c
        f+='\n'
    return f


def parseImage(path,output):
    """Parses image into string Track and creates a shPowable map with the default colorScheme

    Args:
        path (string): The file of the image input
        output (stirng): the file path to store the output track 

    Returns:
        string: The track in a string representation
    """
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