# 02A-Wad_file

This project will have 3 files:
- readWad.py - read data from the WAD file
- main2d.py - render the automap
- main.py - 3d renderer

Create a readWad.py file

Import the following modules:

```python
import struct
import sys
```

Struct is useful for reading binary data.
Sys is used to get the filename from the command line.

Let's setup basic logic to get the WAD file and the map name from the command line.

```python
wadPath = ""

if len(sys.argv) > 1:
    wadPath = sys.argv[1]
else:
    print("\nNo IWAD specified\n")
    exit()

wadFile = open(wadPath, "rb")

mapName = input("What level? (ex: e1m1)\n")
```

Lets setup some basic functions to read bytes from the WAD file.

```python
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
        c = ''
        for i in range(0, 8):
            c += str(struct.unpack('<c', wadFile.read(1))[0], "ascii")
        return c
```

At the start of WAD file there is always a header.
```
Position	| Length  |	Name	        | Description
0x00	    | 4	      | identification	| The ASCII characters "IWAD" or "PWAD".
0x04	    | 4	      | numlumps	    | An integer specifying the number of lumps in the WAD.
0x08	    | 4	      | infotableofs	| An integer holding a pointer to the location of the directory.
```

You can print the WAD type by reading the first 4 bytes of the file. Lets also store the number of lumps in the WAD and the offset of the directory.
```python
print("WAD type: " + str(read4bytes(0)))
directoryCount = read4bytes(4)
directoryOffset = read4bytes(8)
```

So now that we've covered the headers and we have the number of lumps and the offset of the directory we can start reading the directory.

Let's first define every lump we will need for displaying the map (excluding GL nodes for now).

## Things:
```
Offset	| Size (bytes)	| Type	    | Description
0	    | 2	            | int16_t	| x position
2	    | 2	            | int16_t	| y position
4	    | 2	            | int16_t	| Angle facing
6	    | 2	            | int16_t	| DoomEd thing type
8	    | 2	            | int16_t	| Flags
```
```python
def readThingData(offset):
    return [read2bytes(offset), #x
            read2bytes(offset + 2), #y
            read2bytes(offset + 4), #direction
            read2bytes(offset + 6), #type
            read2bytes(offset + 8) #flags
    ]
```

## Linedefs:
```
Offset	| Size (bytes)	| Type  	|Description
0	    | 2	            | int16_t	|Start Vertex
2	    | 2	            | int16_t	|End Vertex
4	    | 2	            | int16_t	|Flags
6	    | 2	            | int16_t	|Special Type
8	    | 2	            | int16_t	|Sector Tag
10	    | 2	            | int16_t	|Front Sidedef
12	    | 2	            | int16_t	|Back Sidedef 
```
```python
def readLinedefData(offset):
    
    return [read2bytes(offset), #Start vertex
            read2bytes(offset + 2), #End vertex
            read2bytes(offset + 4), #Flags
            read2bytes(offset + 6), #LineType
            read2bytes(offset + 8), #Sector tag
            read2bytes(offset + 10), #Right sidedef
            read2bytes(offset + 12) #Left sidedef
    ]
```

## Sidedefs:
```
Offset	| Size (bytes)	| Type	    | Description
0	    | 2	            | int16_t	| x offset
2	    | 2	            | int16_t	| y offset
4	    | 8	            | int8_t 	| Name of upper texture
12	    | 8	            | int8_t 	| Name of lower texture
20	    | 8	            | int8_t 	| Name of middle texture
28	    | 2	            | int16_t	| Sector number this sidedef 'faces'
```
```python
def readSidedefData(offset):
    return [read2bytes(offset), #x
            read2bytes(offset + 2), #y
            read8bytes(offset + 4).rstrip('\x00'), #upper texture
            read8bytes(offset + 12).rstrip('\x00'), #lower texture
            read8bytes(offset + 20).rstrip('\x00'), #middle texture
            read2bytes(offset + 28) #sector
    ]
```

## Vertexes:
```
Offset	| Size (bytes)	|Type	    | Description
0	    | 2	            |int16_t    | x position
2	    | 2	            |int16_t    | y position
```
```python
def readVertexData(offset):
    return [read2bytes(offset), #x
            read2bytes(offset + 2)] #y
```

## Segs:
```
Offset	| Size (bytes)	| Type	    |Description
0	    | 2	            | int16_t	|Starting vertex number
2	    | 2	            | int16_t	|Ending vertex number
4	    | 2	            | int16_t	|Angle, full circle is -32768 to 32767.
6	    | 2	            | int16_t	|Linedef number
8	    | 2	            | int16_t	|Direction: 0 (same as linedef) or 1 (opposite of linedef)
10	    | 2	            | int16_t	|Offset: distance along linedef to start of seg
```
```python
def readSegData(offset):
    return [read2bytes(offset), #x
            read2bytes(offset + 2), #y
            read2bytes(offset + 4), #angle
            read2bytes(offset + 6), #line
            read2bytes(offset + 8), #side
            read2bytes(offset + 10) #offset
    ]
```

## Subsectors:
```
Offset	| Size (bytes)	| Type	    | Description
0	    | 2	            | int16_t	| Seg count
2	    | 2	            | int16_t	| First seg number
```
```python
def readSubsectorData(offset):
    return [read2bytes(offset), #seg count
            read2bytes(offset + 2) #first seg
    ]
```

## Node:
```
Offset	| Size (bytes)	| Type  	| Description
0	    | 2	            | int16_t	| x coordinate of partition line start
2	    | 2	            | int16_t	| y coordinate of partition line start
4	    | 2	            | int16_t	| Change in x from start to end of partition line
6	    | 2	            | int16_t	| Change in y from start to end of partition line
8	    | 8	            | int16_t	| Right bounding box
16	    | 8	            | int16_t	| Left bounding box
24	    | 2	            | int16_t	| Right child
26	    | 2	            | int16_t	| Left child
```
```python
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
```

## Sectors:
```
Offset	Size (bytes)	C99 type	Description
0	2	int16_t	Floor height
2	2	int16_t	Ceiling height
4	8	int8_t[8]	Name of floor texture
12	8	int8_t[8]	Name of ceiling texture
20	2	int16_t	Light level
22	2	int16_t	Special Type
24	2	int16_t	Tag number
```
```python
def readSectorData(offset):
    return [read2bytes(offset), #floor height
            read2bytes(offset + 2), #ceiling height
            read8bytes(offset + 4).rstrip('\x00'), #floor texture
            read8bytes(offset + 12).rstrip('\x00'), #ceiling texture
            read2bytes(offset + 20), #light level
            read2bytes(offset + 22), #special
            read2bytes(offset + 24) #tag
    ]
```


Thats all for today.

In the next part we will try to extract the actual data from the WAD