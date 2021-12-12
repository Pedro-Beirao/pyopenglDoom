import struct

wadPath = "doom.wad"
mapName = input("What level? (ex: e1m1 / map01)\n\n")

wadFile = open(wadPath, "rb")

wadType = wadFile.read(4)

#read 2 bytes with offset
def read2bytes(offset = 0):
    wadFile.seek(offset)
    return struct.unpack("<H", wadFile.read(2))[0]

#read 4 bytes with offset
def read4bytes(offset = 0):
    wadFile.seek(offset)
    return struct.unpack("<I", wadFile.read(4))[0]

def read8bytes(offset = 0):
        wadFile.seek(offset)
        sss = ''
        c = ''
        for i in range(0, 8):
            try:
                c += str(struct.unpack('<c', wadFile.read(1))[0], "ascii")
            except: pass
        return c

directoryCount = read4bytes(4)
directoryOffset = read4bytes(8)

#print(wadType)
#print(directoryCount)
#print(directoryOffset)

for i in range(directoryCount):
    #read 4 bytes with offset
    offset = read4bytes(directoryOffset + i * 16)
    #read 4 bytes with offset
    size = read4bytes(directoryOffset + i * 16 + 4)
    name = read8bytes(directoryOffset + i * 16 + 7)
    #print(offset)
    #print(size)
    #print(name)


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
            read2bytes(offset + 26) #left child
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
    return [read2bytes(offset), #no clue what this is, the documentation sucks
            read2bytes(offset + 2),#x
            read2bytes(offset + 4), #no clue
            read2bytes(offset + 6) #y
    ]
def readGLSegsData(offset):
    return [int(bin(read2bytes(offset))[2:].zfill(16)[1:],2), #start
            int(bin(read2bytes(offset))[2:].zfill(16)[0]),
            int(bin(read2bytes(offset+2))[2:].zfill(16)[1:],2), #end
            int(bin(read2bytes(offset+2))[2:].zfill(16)[0]),
            read2bytes(offset + 4), #linedef
            read2bytes(offset + 6), #side
            read2bytes(offset + 8) #partner seg
    ]

def readGLSubsectorData(offset):
    return [read2bytes(offset), #seg count
            read2bytes(offset + 2) #no clue what this is, the documentation sucks
    ]





def findMapIndex():
    for i in range(directoryCount):
        name = read8bytes(directoryOffset + i * 16 + 8)
        if name.rstrip('\0').lower() == mapName.lower():
            return i
    return -1

mapIndex = findMapIndex()

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

def readMapGLVertex(): #glvertex = map + 12
    offset = read4bytes(directoryOffset + (mapIndex+12) * 16)
    size = read4bytes(directoryOffset + (mapIndex+12) * 16 + 4)
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

def readMapGLSegs(): #glsegs = map + 13
    offset = read4bytes(directoryOffset + (mapIndex+13) * 16)
    size = read4bytes(directoryOffset + (mapIndex+13) * 16 + 4)
    numberOfVertex = size / 10
    lis = []
    for i in range(int(numberOfVertex)):
        d = readGLSegsData(offset + i * 10)
        print(d)
        lis.append(d)
    return lis

def readMapGLSubsectors(): #glsubsectors = map + 14
    offset = read4bytes(directoryOffset + (mapIndex+14) * 16)
    size = read4bytes(directoryOffset + (mapIndex+14) * 16 + 4)
    numberOf = size / 4
    lis = []
    for i in range(int(numberOf)):
        d = readGLSubsectorData(offset + i * 4)
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
readMapGLSegs()
#print(readMapGLSubsectors())