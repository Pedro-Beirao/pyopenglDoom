import readWad
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
from PIL import Image
import numpy
import sys
import os

isSussu=False
isImage=False
for arg in sys.argv:
    if arg == '-sussu':
        import images
        isSussu=True
        image = numpy.array(images.sussu, dtype=numpy.uint8)
    elif arg == '-image':
        isImage=True
        img = Image.open(os.path.dirname(os.path.realpath(__file__))+'/image.png')
        image = numpy.array(img, dtype=numpy.uint8)

things = readWad.readMapThings()
vertexes = readWad.readMapVertex()
linedefs = readWad.readMapLinedefs()
sidedefs = readWad.readMapSidedefs()
sectors = readWad.readMapSectors()
subsectors = readWad.readMapSubsectors()
segs = readWad.readMapSegs()
nodes = readWad.readMapNodes()
if readWad.useGLnodes():
    glvertexes= readWad.readMapGLVertex()
    glsegs = readWad.readMapGLSegs()
    glsubsectors = readWad.readMapGLSubsectors()
    glnodes = readWad.readMapGLNodes()

pnames = readWad.findPnames()
texture1 = readWad.searchTexture1(pnames)
textures = readWad.findTextures(texture1)
flats = readWad.findFlats()

# rgbList=[]
# for i in range(200):
#     rgbList.append([250,250,250])

ttt=[]
for linedef in linedefs:
    if not sidedefs[linedef[5]][4] in ttt:
        ttt+= [sidedefs[linedef[5]][4]]

def getPlayerPosition():
    for thing in things:
        if thing[3] == 1:
            return [thing[0], thing[1]]

playerStart = getPlayerPosition()
px=playerStart[0]
py=playerStart[1]+150

glFloor = []

#color profiles:
#0: black floor random walls
#1: yellow floor blue walls
colorProfile=0
hhh=0

def isOnleftSide(x, y, node):
    dx = x - node[0]
    dy = y - node[1]
    return (((dx * node[3]) - (dy * node[2])) <= 0)

def searchForPlayer(node):
    isOnLeft = isOnleftSide(px, px , node)

    print(isOnLeft)

    if isOnLeft:
        return node[13]
    else:
        return node[12]

def drawWalls():
    glFrontFace(GL_CW)
    glCullFace(GL_BACK)
    for linedef in linedefs:
        l=vertexes[linedef[0]]
        r=vertexes[linedef[1]]
        dist = math.sqrt(((r[0]-px)-(l[0]-px))**2+((r[1]-px)-(l[1]-px))**2)
        if linedef[6]==65535: 
            glEnable(GL_CULL_FACE)
            f=sectors[sidedefs[linedef[5]][5]][0]-hhh
            c=sectors[sidedefs[linedef[5]][5]][1]-hhh
            # color=[]
            # if colorProfile==0:
            #     color=rgbList[ttt.index(sidedefs[linedef[5]][4])]
            # elif colorProfile==1:
            #     color=[f/255-c/255, c/255-f/255, c/255-f/255]
            li=sectors[sidedefs[linedef[5]][5]][4]
            glColor4f(li/255, li/255, li/255, 1)
            if sidedefs[linedef[5]][4] != '-':
                t=textures[sidedefs[linedef[5]][4].upper()]
                glBindTexture(GL_TEXTURE_2D, t[0])
                wi = t[1]
                he = t[2]
            glBegin(GL_QUADS)
            glTexCoord2f(0, (c-f)/he)
            glVertex3f((l[0]-px)/20, (l[1]-py)/20, f/20)
            glTexCoord2f(0, 0)
            glVertex3f((l[0]-px)/20, (l[1]-py)/20, c/20)
            glTexCoord2f(dist/wi, 0)
            glVertex3f((r[0]-px)/20, (r[1]-py)/20, c/20)
            glTexCoord2f(dist/wi, (c-f)/he)
            glVertex3f((r[0]-px)/20, (r[1]-py)/20, f/20)
            glEnd()
        else:
            glDisable(GL_CULL_FACE)
            f1=sectors[sidedefs[linedef[5]][5]][0]-hhh
            f2=sectors[sidedefs[linedef[6]][5]][0]-hhh
            c1=sectors[sidedefs[linedef[5]][5]][1]-hhh
            c2=sectors[sidedefs[linedef[6]][5]][1]-hhh
            li=sectors[sidedefs[linedef[5]][5]][4]
            # color=[]
            # if colorProfile==0:
            #     color=rgbList[ttt.index(sidedefs[linedef[5]][4])]
            # elif colorProfile==1:
            #     color=[f1/255, c1/255, c1/255]
            glColor4f(li/255, li/255, li/255, 1)
            if sidedefs[linedef[5]][3] != '-':
                t=textures[sidedefs[linedef[5]][3].upper()]
                glBindTexture(GL_TEXTURE_2D, t[0])
                wi = t[1]
                he = t[2]
            glBegin(GL_QUADS)
            glTexCoord2f(0, (f2-f1)/he)
            glVertex3f((l[0]-px)/20, (l[1]-py)/20, f1/20)
            glTexCoord2f(0, 0)
            glVertex3f((l[0]-px)/20, (l[1]-py)/20, f2/20)
            glTexCoord2f(dist/wi, 0)
            glVertex3f((r[0]-px)/20, (r[1]-py)/20, f2/20)
            glTexCoord2f(dist/wi, (f2-f1)/he)
            glVertex3f((r[0]-px)/20, (r[1]-py)/20, f1/20)
            glEnd()

            glColor4f(li/255, li/255, li/255, 1)
            if sidedefs[linedef[5]][2] != '-':
                t=textures[sidedefs[linedef[5]][2].upper()]
                glBindTexture(GL_TEXTURE_2D, t[0])
                wi = t[1]
                he = t[2]
            glBegin(GL_QUADS)
            glTexCoord2f(dist/wi, 0)
            glVertex3f((l[0]-px)/20, (l[1]-py)/20, c1/20)
            glTexCoord2f(dist/wi, (c2-c1)/he)
            glVertex3f((l[0]-px)/20, (l[1]-py)/20, c2/20)
            glTexCoord2f(0, (c2-c1)/he)
            glVertex3f((r[0]-px)/20, (r[1]-py)/20, c2/20)
            glTexCoord2f(0, 0)
            glVertex3f((r[0]-px)/20, (r[1]-py)/20, c1/20)
            glEnd()

            glEnable(GL_CULL_FACE)


def drawFloor():
    glPolygonMode(GL_FRONT,GL_FILL)
    if readWad.useGLnodes():
        for se in glFloor:
            glColor4f(se[5]/255, se[5]/255, se[5]/255, 1)
            glBindTexture(GL_TEXTURE_2D, flats[se[3]])
            glCullFace(GL_BACK)
            glBegin(GL_TRIANGLE_FAN)
            for s in se[0]:
                    glTexCoord2f (s[0]/3, s[1]/3)
                    glVertex3f(s[0],s[1],se[1]/20)
            glEnd()
        for se in glFloor:
            glColor4f(se[5]/255, se[5]/255, se[5]/255, 1)
            glBindTexture(GL_TEXTURE_2D, flats[se[4]])
            glCullFace(GL_FRONT)
            glBegin(GL_TRIANGLE_FAN)
            for s in se[0]:
                    glTexCoord2f (s[0]/3, s[1]/3)
                    glVertex3f(s[0],s[1],se[2]/20)
            glEnd()
    else:
        for subsector in subsectors:
            glCullFace(GL_BACK)
            glColor4f(255, 255, 255, 1)
            glBegin(GL_TRIANGLE_FAN)
            f=0
            for size in range(subsector[0]):
                vx=vertexes[segs[subsector[1]+size][0]]
                vy=vertexes[segs[subsector[1]+size][1]]
                if segs[subsector[1]+size][4]==0:
                    f=sectors[sidedefs[linedefs[segs[subsector[1]+size][3]][5]][5]][0]-hhh
                else:
                    f= sectors[sidedefs[linedefs[segs[subsector[1]+size][3]][6]][5]][0]-hhh
                glVertex3f((vx[0]-px)/20,(vx[1]-py)/20,f/30)
                glVertex3f((vy[0]-px)/20,(vy[1]-py)/20,f/30)
            glEnd()

            glCullFace(GL_FRONT)
            glColor4f(255, 255, 255, 1)
            glBegin(GL_TRIANGLE_FAN)
            f=0
            for size in range(subsector[0]):
                vx=vertexes[segs[subsector[1]+size][0]]
                vy=vertexes[segs[subsector[1]+size][1]]
                if segs[subsector[1]+size][4]==0:
                    c=sectors[sidedefs[linedefs[segs[subsector[1]+size][3]][5]][5]][1]-hhh
                else:
                    c= sectors[sidedefs[linedefs[segs[subsector[1]+size][3]][6]][5]][1]-hhh
                glVertex3f((vx[0]-px)/20,(vx[1]-py)/20,c/30)
                glVertex3f((vy[0]-px)/20,(vy[1]-py)/20,c/30)
            glEnd()


pygame.init()
display = (1000, 600)
scree = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

def loadFlat(path):
    # img = Image.open(path)
    # img_data = numpy.fromstring(img.tobytes(), dtype=numpy.uint8)
    if(isSussu or isImage):
        a = image
    else:
        a = numpy.array(flats[path], dtype=numpy.uint8)
    img_data = numpy.fromstring(a.tobytes(), dtype=numpy.uint8) 
    width, height = numpy.shape(a)[1], numpy.shape(a)[0]
    texture = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_COMBINE)
    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0,
        GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    return texture

def loadTexture(path):
    if(isSussu or isImage):
        a = image
    else:
        a = numpy.array(textures[path], dtype=numpy.uint8)
        a = numpy.rot90(a, 3)
    img_data = numpy.fromstring(a.tobytes(), dtype=numpy.uint8) 
    width, height = numpy.shape(a)[1], numpy.shape(a)[0]
    # width, height = len(textures[path][0]), len(textures[path])
    texture = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0,
        GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    return [texture, width, height]

flatList = list(flats.keys())
for flat in range(len(flatList)):
    flats[flatList[flat]] = loadFlat(flatList[flat])

textureList = list(textures.keys())
for texture in range(len(textureList)):
    textures[textureList[texture]] = loadTexture(textureList[texture])


def main():
    global glFloor, hhh

    curNode = len(glnodes) - 1
    while int(curNode & 0x8000):
        curNode = searchForPlayer(glnodes[curNode])

    hhh=sectors[sidedefs[linedefs[glsegs[glsubsectors[int(curNode & (~0x8000))][1]][3]][5]][5]][0]+35
    
    if readWad.useGLnodes():
        for glsubsector in glsubsectors:
            v=[]
            f=0
            c=0
            l=150
            for size in range(glsubsector[0]):
                vx=0
                vy=0
                if glsegs[glsubsector[1]+size][1]==0:
                    vx=vertexes[glsegs[glsubsector[1]+size][0]]
                    v+=[[(vx[0]-px)/20,(vx[1]-py)/20]]
                else:
                    vx=glvertexes[glsegs[glsubsector[1]+size][0]]
                    v+=[[(vx[0]-px)/20,(vx[1]-py)/20]]
                if glsegs[glsubsector[1]+size][3]==0:
                    vy=vertexes[glsegs[glsubsector[1]+size][2]]
                    v+=[[(vy[0]-px)/20,(vy[1]-py)/20]]
                else:
                    vy=glvertexes[glsegs[glsubsector[1]+size][2]]
                    v+=[[(vy[0]-px)/20,(vy[1]-py)/20]]
                if glsegs[glsubsector[1]+size][4] != 65535:
                    if glsegs[glsubsector[1]+size][5]==0:
                        f=sectors[sidedefs[linedefs[glsegs[glsubsector[1]+size][4]][5]][5]][0]-hhh
                        c=sectors[sidedefs[linedefs[glsegs[glsubsector[1]+size][4]][5]][5]][1]-hhh
                        tf=sectors[sidedefs[linedefs[glsegs[glsubsector[1]+size][4]][5]][5]][2]
                        tc=sectors[sidedefs[linedefs[glsegs[glsubsector[1]+size][4]][5]][5]][3]
                        l=sectors[sidedefs[linedefs[glsegs[glsubsector[1]+size][4]][5]][5]][4]
                    else:
                        f=sectors[sidedefs[linedefs[glsegs[glsubsector[1]+size][4]][6]][5]][0]-hhh
                        c=sectors[sidedefs[linedefs[glsegs[glsubsector[1]+size][4]][6]][5]][1]-hhh
                        if linedefs[glsegs[glsubsector[1]+size][4]][6]!=65535:
                            tf=sectors[sidedefs[linedefs[glsegs[glsubsector[1]+size][4]][6]][5]][2]
                            tc=sectors[sidedefs[linedefs[glsegs[glsubsector[1]+size][4]][6]][5]][3]
                            l=sectors[sidedefs[linedefs[glsegs[glsubsector[1]+size][4]][6]][5]][4]
            glFloor+=[[v,f,c,tf,tc,l]]
        
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])


    glMatrixMode(GL_PROJECTION)
    glPre = gluPerspective(60, (display[0]/display[1]), 0.1, 200.0)

    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    glLoadIdentity()

    glEnable(GL_TEXTURE_2D)

    # init mouse movement and center mouse on screen
    displayCenter = [500,300]
    mouseMove = [0, 0]
    pygame.mouse.set_pos(displayCenter)

    up_down_angle = 0.0
    paused = False
    run = True

    clock = pygame.time.Clock()
    while run:
        deltaTime=clock.get_fps()/90
        if deltaTime==0: deltaTime=0.1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    run = False
                if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                    paused = not paused
                    pygame.mouse.set_pos(displayCenter) 
                if event.key == pygame.K_t: 
                    if colorProfile<1:
                        colorProfile+=1
                    else:
                        colorProfile=0
            if not paused: 
                if event.type == pygame.MOUSEMOTION:
                    mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]

        if not paused:
            keypress = pygame.key.get_pressed()
        
            glLoadIdentity()

            if not keypress[pygame.K_q]:
                up_down_angle += mouseMove[1]*0.1
                glRotatef(up_down_angle, 1.0, 0.0, 0.0)

            glPushMatrix()
            glLoadIdentity()


            speed=.3/deltaTime

            # apply the movment 
            if keypress[pygame.K_LSHIFT]:
                speed=1/deltaTime
            if keypress[pygame.K_w]:
                glTranslatef(0,0,speed)
            if keypress[pygame.K_s]:
                glTranslatef(0,0,-speed)
            if keypress[pygame.K_d]:
                glTranslatef(-speed,0,0)
            if keypress[pygame.K_a]:
                glTranslatef(speed,0,0)
            if keypress[pygame.K_SPACE]:
                glTranslatef(0,-speed/2,0)
            if keypress[pygame.K_c]:
                glTranslatef(0,speed/2,0)
            if not keypress[pygame.K_q]: 
                glRotatef(mouseMove[0]*0.2, 0.0, 1.0, 0.0) 


            # multiply the current matrix by the get the new view matrix and store the final vie matrix 
            glMultMatrixf(viewMatrix)
            viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

            # apply view matrix
            glPopMatrix()
            glMultMatrixf(viewMatrix)

            glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            glPushMatrix()

            drawWalls()
            drawFloor()

            glPopMatrix()

            pygame.display.flip()

            clock.tick()
            pygame.display.set_caption("fps: " + str(clock.get_fps()))
            #pygame.time.wait(1)
            pygame.mouse.set_pos(displayCenter)  

    pygame.quit()