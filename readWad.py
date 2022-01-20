import struct
import sys
import random

wadPath = ""

def showHelp():
    print("Usage:")
    print("  python main.py C:\\path\\to\\doom.wad\n")
    print("https://github.com/Pedro-Beirao/pyopenglDoomRenderer")

noGL = False
if len(sys.argv) > 1:
    wadPath = sys.argv[1]
else:
    print("\nNo IWAD specified\n")
    showHelp()
    exit()
wadFile = open(wadPath, "rb")
try: gwaFile = open(wadPath[:-4] + ".gwa", "rb")
except: noGL = True

mapName = input("What level? (ex: e1m1)\n")

print()

wadType = wadFile.read(4)

def useGLnodes():
    if noGL:
        return False
    else:
        return True

def read1byte(offset = 0):
    wadFile.seek(offset)
    return struct.unpack("<B", wadFile.read(1))[0]

def read2bytes(offset = 0):
    wadFile.seek(offset)
    return struct.unpack("<H", wadFile.read(2))[0]

def read4bytes(offset = 0):
    wadFile.seek(offset)
    return struct.unpack("<I", wadFile.read(4))[0]

def read8bytes(offset = 0):
        wadFile.seek(offset)
        sss = ''
        c = ''
        for i in range(0, 8):
                c += str(struct.unpack('<c', wadFile.read(1))[0], "ascii")
        return c

def read2bytesGL(offset = 0):
    gwaFile.seek(offset)
    return struct.unpack("<H", gwaFile.read(2))[0]

def read4bytesGL(offset = 0):
    gwaFile.seek(offset)
    return struct.unpack("<I", gwaFile.read(4))[0]

def read8bytesGL(offset = 0):
        gwaFile.seek(offset)
        sss = ''
        c = ''
        for i in range(0, 8):
                c += str(struct.unpack('<c', gwaFile.read(1))[0], "ascii")
        return c


directoryCount = read4bytes(4)
directoryOffset = read4bytes(8)

if noGL:
    if input("\033[93m No GL nodes found on the provided wad file. \033[0m \nTo correctly render the map, you should generate GL nodes using glBSP\n( https://github.com/Pedro-Beirao/pyopenglDoomRenderer/blob/main/docs/glBSP-guide.md )\n\nDo you want to proceed without GL nodes? (y/n)").lower()=="y":
        pass
    else:
        exit()
else:
    directoryCountGL = read4bytesGL(4)
    directoryOffsetGL = read4bytesGL(8)


def readVertexData(offset):
    return [read2bytes(offset), #x
            read2bytes(offset + 2)] #y

def readLinedefData(offset):
    
    return [read2bytes(offset), #Start vertex
            read2bytes(offset + 2), #End vertex
            read2bytes(offset + 4), #Flags
            read2bytes(offset + 6), #LineType
            read2bytes(offset + 8), #Sector tag
            read2bytes(offset + 10), #Right sidedef
            read2bytes(offset + 12) #Left sidedef
    ]

def readSidedefData(offset):
    return [read2bytes(offset), #x
            read2bytes(offset + 2), #y
            read8bytes(offset + 4).rstrip('\x00'), #upper texture
            read8bytes(offset + 12).rstrip('\x00'), #lower texture
            read8bytes(offset + 20).rstrip('\x00'), #middle texture
            read2bytes(offset + 28) #sector
    ]

def readSegData(offset):
    return [read2bytes(offset), #x
            read2bytes(offset + 2), #y
            read2bytes(offset + 4), #angle
            read2bytes(offset + 6), #line
            read2bytes(offset + 8), #side
            read2bytes(offset + 10) #offset
    ]

def readSubsectorData(offset):
    return [read2bytes(offset), #seg count
            read2bytes(offset + 2) #first seg
    ]

def readNodeData(offset):
    return [read2bytes(offset), #x
            read2bytes(offset + 2), #y
            read2bytes(offset + 4), #dx
            read2bytes(offset + 6), #dy
            read2bytes(offset + 8), #right box top
            read2bytes(offset + 10), #right box bottom
            read2bytes(offset + 12), #right box left
            read2bytes(offset + 14), #right box right
            read2bytes(offset + 16), #left box top
            read2bytes(offset + 18), #left box bottom
            read2bytes(offset + 20), #left box left
            read2bytes(offset + 22), #left box right
            read2bytes(offset + 24), #right child
            read2bytes(offset + 26), #left child
    ]

def readSectorData(offset):
    return [read2bytes(offset), #floor height
            read2bytes(offset + 2), #ceiling height
            read8bytes(offset + 4).rstrip('\x00'), #floor texture
            read8bytes(offset + 12).rstrip('\x00'), #ceiling texture
            read2bytes(offset + 20), #light level
            read2bytes(offset + 22), #special
            read2bytes(offset + 24) #tag
    ]

def readThingData(offset):
    return [read2bytes(offset), #x
            read2bytes(offset + 2), #y
            read2bytes(offset + 4), #direction
            read2bytes(offset + 6), #type
            read2bytes(offset + 8) #flags
    ]

def readGLVertData(offset):
    return [read2bytesGL(offset), #no clue what this is, the documentation sucks
            read2bytesGL(offset + 2),#x
            read2bytesGL(offset + 4), #no clue
            read2bytesGL(offset + 6) #y
    ]
def readGLSegsData(offset):
    return [int(bin(read2bytesGL(offset))[2:].zfill(16)[1:],2), #start
            int(bin(read2bytesGL(offset))[2:].zfill(16)[0]),
            int(bin(read2bytesGL(offset+2))[2:].zfill(16)[1:],2), #end
            int(bin(read2bytesGL(offset+2))[2:].zfill(16)[0]),
            read2bytesGL(offset + 4), #linedef
            read2bytesGL(offset + 6), #side
            read2bytesGL(offset + 8) #partner seg
    ]

def readGLSubsectorData(offset):
    return [read2bytesGL(offset), #seg count
            read2bytesGL(offset + 2) #no clue what this is, the documentation sucks
    ]

def readGLNodeData(offset):
    return [read2bytesGL(offset), #x
            read2bytesGL(offset + 2), #y
            read2bytesGL(offset + 4), #dx
            read2bytesGL(offset + 6), #dy
            read2bytesGL(offset + 8), #right box top
            read2bytesGL(offset + 10), #right box bottom
            read2bytesGL(offset + 12), #right box left
            read2bytesGL(offset + 14), #right box right
            read2bytesGL(offset + 16), #left box top
            read2bytesGL(offset + 18), #left box bottom
            read2bytesGL(offset + 20), #left box left
            read2bytesGL(offset + 22), #left box right
            read2bytesGL(offset + 24), #right child
            read2bytesGL(offset + 26), #left child
    ]







def findMapIndex():
    for i in range(directoryCount):
        name = read8bytes(directoryOffset + i * 16 + 8)
        if name.rstrip('\0').lower() == mapName.lower():
            return i
    return -1

def findMapIndexGL():
    for i in range(directoryCountGL):
        name = read8bytesGL(directoryOffsetGL + i * 16 + 8)
        if name.rstrip('\0').lower() == "gl_"+mapName.lower():
            return i
    return -1


mapIndex = findMapIndex()

if not noGL:
    mapIndexGL = findMapIndexGL()










def readMapVertex(): #vertex = map + 4
    offset = read4bytes(directoryOffset + (mapIndex+4) * 16)
    size = read4bytes(directoryOffset + (mapIndex+4) * 16 + 4)
    numberOfVertex = size / 4
    vertexList = []
    for i in range(int(numberOfVertex)):
        d = readVertexData(offset + i * 4)
        if d[0] > 65536/2:
            d[0] = d[0] - 65536
        if d[1] > 65536/2:
            d[1] = d[1] - 65536
        vertexList.append(d)
    return vertexList

def readMapLinedefs(): #linedef = map + 2
    offset = read4bytes(directoryOffset + (mapIndex+2) * 16)
    size = read4bytes(directoryOffset + (mapIndex+2) * 16 + 4)
    numberOfLinedefs = size / 14
    linedefList = []
    for i in range(int(numberOfLinedefs)):
        d = readLinedefData(offset + i * 14)
        linedefList.append(d)
    return linedefList

def readMapThings(): #things = map + 1
    offset = read4bytes(directoryOffset + (mapIndex+1) * 16)
    size = read4bytes(directoryOffset + (mapIndex+1) * 16 + 4)
    numberOf = size / 10
    lis = []
    for i in range(int(numberOf)):
        d = readThingData(offset + i * 10)
        if d[0] > 65536/2:
            d[0] = d[0] - 65536
        if d[1] > 65536/2:
            d[1] = d[1] - 65536
        lis.append(d)
    return lis

def readMapSegs(): #segs = map + 5
    offset = read4bytes(directoryOffset + (mapIndex+5) * 16)
    size = read4bytes(directoryOffset + (mapIndex+5) * 16 + 4)
    numberOf = size / 12
    lis = []
    for i in range(int(numberOf)):
        d = readSegData(offset + i * 12)
        if d[3] > 65536/2:
            d[3] = d[3] - 65536
        lis.append(d)
    return lis

def readMapSubsectors(): #subsectors = map + 6
    offset = read4bytes(directoryOffset + (mapIndex+6) * 16)
    size = read4bytes(directoryOffset + (mapIndex+6) * 16 + 4)
    numberOf = size / 4
    lis = []
    for i in range(int(numberOf)):
        d = readSubsectorData(offset + i * 4)
        lis.append(d)
    return lis

def readMapNodes(): #nodes = map + 7
    offset = read4bytes(directoryOffset + (mapIndex+7) * 16)
    size = read4bytes(directoryOffset + (mapIndex+7) * 16 + 4)
    numberOf = size / 28
    lis = []
    for i in range(int(numberOf)):
        d = readNodeData(offset + i * 28)
        if d[0] > 65536/2:
            d[0] = d[0] - 65536
        if d[1] > 65536/2:
            d[1] = d[1] - 65536
        if d[2] > 65536/2:
            d[2] = d[2] - 65536
        if d[3] > 65536/2:
            d[3] = d[3] - 65536
        if d[4] > 65536/2:
            d[4] = d[4] - 65536
        if d[5] > 65536/2:
            d[5] = d[5] - 65536
        if d[6] > 65536/2:
            d[6] = d[6] - 65536
        if d[7] > 65536/2:
            d[7] = d[7] - 65536
        if d[8] > 65536/2:
            d[8] = d[8] - 65536
        if d[9] > 65536/2:
            d[9] = d[9] - 65536
        if d[10] > 65536/2:
            d[10] = d[10] - 65536
        if d[11] > 65536/2:
            d[11] = d[11] - 65536
        lis.append(d)
    return lis

def readMapSectors(): #sectors = map + 8
    offset = read4bytes(directoryOffset + (mapIndex+8) * 16)
    size = read4bytes(directoryOffset + (mapIndex+8) * 16 + 4)
    numberOf = size / 26
    lis = []
    for i in range(int(numberOf)):
        d = readSectorData(offset + i * 26)
        if d[0] > 65536/2:
            d[0] = d[0] - 65536
        if d[1] > 65536/2:
            d[1] = d[1] - 65536
        lis.append(d)
    return lis

def readMapSidedefs(): #sectors = map + 3
    offset = read4bytes(directoryOffset + (mapIndex+3) * 16)
    size = read4bytes(directoryOffset + (mapIndex+3) * 16 + 4)
    numberOf = size / 30
    lis = []
    for i in range(int(numberOf)):
        d = readSidedefData(offset + i * 30)
        if d[0] > 65536/2:
            d[0] = d[0] - 65536
        if d[1] > 65536/2:
            d[1] = d[1] - 65536
        lis.append(d)
    return lis

def readMapGLVertex(): #glvertex = map + 1
    offset = read4bytesGL(directoryOffsetGL + (mapIndexGL+1) * 16)
    size = read4bytesGL(directoryOffsetGL + (mapIndexGL+1) * 16 + 4)
    numberOfVertex = size / 8
    vertexList = []
    for i in range(int(numberOfVertex)):
        d = readGLVertData(offset + i * 8 + 4)#add 4 because of Nd1-Nd5
        if d[1] > 65536/2:
            d[1] = d[1] - 65536
        if d[3] > 65536/2:
            d[3] = d[3] - 65536
        vertexList.append([d[1],d[3]])
    return vertexList

def readMapGLSegs(): #glsegs = map + 2
    offset = read4bytesGL(directoryOffsetGL + (mapIndexGL+2) * 16)
    size = read4bytesGL(directoryOffsetGL + (mapIndexGL+2) * 16 + 4)
    numberOfVertex = size / 10
    lis = []
    for i in range(int(numberOfVertex)):
        d = readGLSegsData(offset + i * 10)
        lis.append(d)
    return lis

def readMapGLSubsectors(): #glsubsectors = map + 3
    offset = read4bytesGL(directoryOffsetGL + (mapIndexGL+3) * 16)
    size = read4bytesGL(directoryOffsetGL + (mapIndexGL+3) * 16 + 4)
    numberOf = size / 4
    lis = []
    for i in range(int(numberOf)):
        d = readGLSubsectorData(offset + i * 4)
        lis.append(d)
    return lis

def readMapGLNodes(): #glnodes = map + 4
    offset = read4bytesGL(directoryOffsetGL + (mapIndexGL+4) * 16)
    size = read4bytesGL(directoryOffsetGL + (mapIndexGL+4) * 16 + 4)
    numberOf = size / 28
    lis = []
    for i in range(int(numberOf)):
        d = readGLNodeData(offset + i * 28)
        if d[0] > 65536/2:
            d[0] = d[0] - 65536
        if d[1] > 65536/2:
            d[1] = d[1] - 65536
        if d[2] > 65536/2:
            d[2] = d[2] - 65536
        if d[3] > 65536/2:
            d[3] = d[3] - 65536
        if d[4] > 65536/2:
            d[4] = d[4] - 65536
        if d[5] > 65536/2:
            d[5] = d[5] - 65536
        if d[6] > 65536/2:
            d[6] = d[6] - 65536
        if d[7] > 65536/2:
            d[7] = d[7] - 65536
        if d[8] > 65536/2:
            d[8] = d[8] - 65536
        if d[9] > 65536/2:
            d[9] = d[9] - 65536
        if d[10] > 65536/2:
            d[10] = d[10] - 65536
        if d[11] > 65536/2:
            d[11] = d[11] - 65536
        lis.append(d)
    return lis

#print(readMapVertex())
#print(readMapLinedefs())
#print(readMapThings())
#print(readMapSegs())
#print(readMapSubsectors())
#print(readMapNodes())
#print(readMapSectors())
#print(readMapSidedefs())
#print(readMapGLVertex())
#print(readMapGLSegs())
#print(readMapGLSubsectors())







def findPlaypalIndex():
    for i in range(directoryCount):
        name = read8bytes(directoryOffset + i * 16 + 8)
        if name.rstrip('\0') == "PLAYPAL":
            return i
    return -1

def readPlaypal():
    offset = read4bytes(directoryOffset + findPlaypalIndex() * 16)
    size = read4bytes(directoryOffset + findPlaypalIndex() * 16 + 4)
    playPal1Size = size / 14
    playpal=[]
    for c in range(256):
        playpal+=[[read1byte(offset + c * 3),read1byte(offset + c * 3 + 1),read1byte(offset + c * 3 + 2)]]
    return playpal


def findF_START():
    for i in range(directoryCount):
        name = read8bytes(directoryOffset + i * 16 + 8)
        if name.rstrip('\0') == "F_START":
            return i
    return -1

def findF_END():
    for i in range(directoryCount):
        name = read8bytes(directoryOffset + i * 16 + 8)
        if name.rstrip('\0') == "F_END":
            return i
    return -1

def findP_START():
    for i in range(directoryCount):
        name = read8bytes(directoryOffset + i * 16 + 8)
        if name.rstrip('\0') == "P_START":
            return i
    return -1

def findP_END():
    for i in range(directoryCount):
        name = read8bytes(directoryOffset + i * 16 + 8)
        if name.rstrip('\0') == "P_END":
            return i
    return -1

def findFlats():
    flats={}
    playpal = readPlaypal()
    a=0
    for t in range(findF_START()+2,findF_END()):
        offset = read4bytes(directoryOffset + t * 16)
        size = read4bytes(directoryOffset + t * 16 + 4)
        name = read8bytes(directoryOffset + t * 16 + 8)
        if name[2] != "_":
            a+=1
            c=[]
            cc=[]
            for i in range(64):
                for l in range(64):
                    c += [playpal[read1byte(offset + i * 64 + l)]]
                cc += [c]
                c=[]
            flats[name.rstrip("\x00")] = cc
    return flats

def findTextures(texture1):
    textures={}
    a=0
    playpal = readPlaypal()
    for t in range(findP_START()+2,findP_END()):
        offset = read4bytes(directoryOffset + t * 16)
        size = read4bytes(directoryOffset + t * 16 + 4)
        name = read8bytes(directoryOffset + t * 16 + 8).rstrip('\x00')
        if name[2] != "_":
            a+=1
            c=[]
            cc=[]
            width=read2bytes(offset)
            height=read2bytes(offset + 2)
            try:
                patch = texture1[name]
                for i in range(width):
                    newOffset = read4bytes(offset + 8 + i * 4)
                    print(newOffset) 
                    for l in range(height):
                        c += [playpal[read1byte(newOffset + 1 + i * width + l)]]
                    cc += [c]
                    c=[]
                textures[patch[2]] = cc
            except:
                pass
    return textures

def findPnames():
    pnames=[]
    for i in range(directoryCount):
        offset = read4bytes(directoryOffset + i * 16)
        size = read4bytes(directoryOffset + i * 16 + 4)
        name = read8bytes(directoryOffset + i * 16 + 8).rstrip('\x00')
        if name == "PNAMES":
            count = read4bytes(offset)
            for i in range(count):
                pnames += [read8bytes(offset + 4 + i * 8)]
    return pnames

def searchTexture1(pnames):
    texture1={}
    for i in range(directoryCount):
        offset = read4bytes(directoryOffset + i * 16)
        size = read4bytes(directoryOffset + i * 16 + 4)
        name = read8bytes(directoryOffset + i * 16 + 8).rstrip('\x00')
        if name == "TEXTURE1":
            count = read4bytes(offset)
            offsets = []
            for i in range(count):
                offsets.append(read4bytes(offset + 4 + i * 4))
                tex = offset + read4bytes(offset + 4 + i * 4)
                tname = read8bytes(tex).rstrip('\x00')
                width = read2bytes(tex + 12)
                height = read2bytes(tex + 14)
                index = read2bytes(tex + 26)
                texture1[pnames[index].rstrip('\x00')] = [width,height,tname]
    return texture1

pnames = findPnames()
texture1 =  searchTexture1(pnames)
textures = findTextures(texture1)

print(textures.keys())

from PIL import Image
import numpy as np
a = np.array(textures["DOOR1"], dtype=np.uint8)
img = Image.fromarray(a) 
img.show()