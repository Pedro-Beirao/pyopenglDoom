from os import read
import readWad
import pygame
import random
import math

things = readWad.readMapThings()
vertexes = readWad.readMapVertex()
linedefs = readWad.readMapLinedefs()
sidedefs = readWad.readMapSidedefs()
sectors = readWad.readMapSectors()
nodes =readWad.readMapNodes()
segs = readWad.readMapSegs()
subsectors = readWad.readMapSubsectors()
glvertexes= readWad.readMapGLVertex()
glsegs = readWad.readMapGLSegs()
glsubsectors = readWad.readMapGLSubsectors()

mapX=100
mapY=500

pygame.init()
display = (1000, 600)
scree = pygame.display.set_mode(display)

def getStartPosition():
    for thing in things:
        if thing[3] == 1:
            return [thing[0], thing[1]]

startPos = getStartPosition()

def calculateOffsetX(x,angle,offset):
    x=x+offset*math.cos(angle)
    return x
def calculateOffsetY(y,angle,offset):
    y=y+offset*math.sin(angle)
    return y

def drawWalls():
    for linedef in linedefs:
        l=vertexes[linedef[0]]
        r=vertexes[linedef[1]]
        pygame.draw.line(scree, (200,200,200), (l[0]/10+mapX,l[1]/10+mapY),(r[0]/10+mapX,r[1]/10+mapY),2)

def drawPlayerDot():
    pygame.draw.line(scree, (250,0,0), (startPos[0]/10+mapX,startPos[1]/10+mapY),(startPos[0]/10+mapX,startPos[1]/10+mapY),5)

def drawSectors():
    for sector in sectors:
        c=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        s=[]
        for linedef in linedefs:
            if sectors[sidedefs[linedef[5]][5]]==sector:
                print("ok")
                s+=[[vertexes[linedef[0]][0]/10+mapX,vertexes[linedef[0]][1]/10+mapY]]
                s+=[[vertexes[linedef[1]][0]/10+mapX,vertexes[linedef[1]][1]/10+mapY]]
        try: pygame.draw.polygon(scree, (c[0],c[1],c[2]), s)
        except: pass
        s=[]

def drawNode(node):
    #if node[12]>237 or node[13]>237: return
    r=pygame.Rect((node[6]/10+mapX,node[4]/10+mapY),((node[7]/10+mapX)-(node[6]/10+mapX)+1,(node[5]/10+mapY)-(node[4]/10+mapY)+1))
    pygame.draw.rect(scree, (250,0,0), r,1)

    rr=pygame.Rect((node[10]/10+mapX,node[8]/10+mapY),((node[11]/10+mapX)-(node[10]/10+mapX)+1,(node[9]/10+mapY)-(node[8]/10+mapY)+1))
    pygame.draw.rect(scree, (0,250,0), rr,1)

    pygame.draw.line(scree, (0,0,250), (node[0]/10+mapX,node[1]/10+mapY),((node[0]/10+mapX)+node[2]/10,(node[1]/10+mapY)+node[3]/10),1)

def drawSubsectors():
    for subsector in subsectors:
        c=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        v=[]
        for size in range(subsector[0]):
            vx=vertexes[segs[subsector[1]+size][0]]
            vy=vertexes[segs[subsector[1]+size][1]]
            l=linedefs[segs[subsector[1]+size][3]]
            v.append([vx[0]/10+mapX,vx[1]/10+mapY])
            v.append([vy[0]/10+mapX,vy[1]/10+mapY])
            #v.append([vertexes[l[0]][0]/10+mapX,vertexes[l[0]][1]/10+mapY])
            #v.append([vertexes[l[1]][0]/10+mapX,vertexes[l[1]][1]/10+mapY])
        try:
            pygame.draw.polygon(scree, (c[0],c[1],c[2]), v)
        except: pass

def debug():
    for glsubsector in glsubsectors:
        c=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        v=[]
        for size in range(glsubsector[0]):
                vx=0
                vy=0
                if glsegs[glsubsector[1]+size][1]==0:
                    vx=vertexes[glsegs[glsubsector[1]+size][0]]
                    v+=[[vx[0]/10+mapX,vx[1]/10+mapY]]
                else:
                    vx=glvertexes[glsegs[glsubsector[1]+size][0]]
                    v+=[[vx[0]/10+mapX,vx[1]/10+mapY]]
                if glsegs[glsubsector[1]+size][3]==0:
                    vy=vertexes[glsegs[glsubsector[1]+size][2]]
                    v+=[[vy[0]/10+mapX,vy[1]/10+mapY]]
                else:
                    vy=glvertexes[glsegs[glsubsector[1]+size][2]]
                    v+=[[vy[0]/10+mapX,vy[1]/10+mapY]]
                #pygame.draw.line(scree, (c[0],c[1],c[2]), (vx[0]/10+mapX,vx[1]/10+mapY),(vy[0]/10+mapX,vy[1]/10+mapY))
        pygame.draw.polygon(scree, (c[0],c[1],c[2]), v)
        
    
def drawSegs():
    for subsector in subsectors:
        c=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        for size in range(subsector[0]):
            vx=vertexes[segs[subsector[1]+size][0]]
            vy=vertexes[segs[subsector[1]+size][1]]
            pygame.draw.line(scree, (c[0],c[1],c[2]), (vx[0]/10+mapX,vx[1]/10+mapY),(vy[0]/10+mapX,vy[1]/10+mapY))


def drawGLSegs():
    for glsubsector in glsubsectors:
        c=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        glvv=[]
        for glv in glvertexes:
            glvx=glv[0]/10+mapX
            glvy=glv[1]/10+mapY
            glvv.append([glvx,glvy])
        vs=vertexes
        for size in range(glsubsector[0]):
            try:
                vx=vs[glsegs[glsubsector[1]+size][0]]
                vy=vs[glsegs[glsubsector[1]+size][1]]
                pygame.draw.line(scree, (c[0],c[1],c[2]), (vx[0]/10+mapX,vx[1]/10+mapY),(vy[0]/10+mapX,vy[1]/10+mapY))
            except: pass

# init mouse movement and center mouse on screen
displayCenter = [500,300]
mouseMove = [0, 0]
pygame.mouse.set_pos(displayCenter)

paused = False
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                run = False
            if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                paused = not paused
                pygame.mouse.set_pos(displayCenter)   

    if not paused:
        # get keys
        scree.fill((0,0,0))
        keypress = pygame.key.get_pressed()
        #mouseMove = pygame.mouse.get_rel()

        if keypress[pygame.K_UP]:
            mapY -= 100
        if keypress[pygame.K_DOWN]:
            mapY += 100
        if keypress[pygame.K_LEFT]:
            mapX -= 100
        if keypress[pygame.K_RIGHT]:
            mapX += 100
        if keypress[pygame.K_r]:
            mapX = 100
            mapY = 500

        

        drawWalls()

        #drawPlayerDot()

        #for node in nodes:
        #    drawNode(node)
        #drawNode(nodes[0])

        #drawSegs()
        #drawSubsectors()
        debug()
        #drawSectors()

        pygame.display.flip()
        pygame.time.wait(100)

pygame.quit()