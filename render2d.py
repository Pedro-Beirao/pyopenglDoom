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
if readWad.useGLnodes():
    glvertexes= readWad.readMapGLVertex()
    glsegs = readWad.readMapGLSegs()
    glsubsectors = readWad.readMapGLSubsectors()
    glnodes = readWad.readMapGLNodes()



pygame.init()
display = (1000, 600)
scree = pygame.display.set_mode(display)

def getStartPosition():
    for thing in things:
        if thing[3] == 1:
            return [thing[0], thing[1]]

startPos = getStartPosition()
print(startPos)
mapX=100 #(500-startPos[0]/10)
mapY=600 #(300+startPos[1]/10)
print(mapX,mapY)
zoom=20

def isOnleftSide(x, y, node):
    dx = x - node[0]
    dy = y - node[1]
    return (((dx * node[3]) - (dy * node[2])) <= 0)

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
        pygame.draw.line(scree, (200,200,200), (l[0]/zoom+mapX,l[1]/zoom+mapY),(r[0]/zoom+mapX,r[1]/zoom+mapY),2)

def drawPlayerDot():
    pygame.draw.line(scree, (250,0,0), (startPos[0]/zoom+mapX,startPos[1]/zoom+mapY),(startPos[0]/zoom+mapX,startPos[1]/zoom+mapY),5)

def drawSectors():
    for sector in sectors:
        c=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        s=[]
        for linedef in linedefs:
            if sectors[sidedefs[linedef[5]][5]]==sector:
                s+=[[vertexes[linedef[0]][0]/zoom+mapX,vertexes[linedef[0]][1]/zoom+mapY]]
                s+=[[vertexes[linedef[1]][0]/zoom+mapX,vertexes[linedef[1]][1]/zoom+mapY]]
        try: pygame.draw.polygon(scree, (c[0],c[1],c[2]), s)
        except: pass
        s=[]

def drawNode(node):
    #if node[12]>237 or node[13]>237: return
    r=pygame.Rect((node[6]/zoom+mapX,node[4]/zoom+mapY),((node[7]/zoom+mapX)-(node[6]/zoom+mapX)+1,(node[5]/zoom+mapY)-(node[4]/zoom+mapY)+1))
    pygame.draw.rect(scree, (0,250,0), r,1)

    rr=pygame.Rect((node[10]/zoom+mapX,node[8]/zoom+mapY),((node[11]/zoom+mapX)-(node[10]/zoom+mapX)+1,(node[9]/zoom+mapY)-(node[8]/zoom+mapY)+1))
    pygame.draw.rect(scree, (250,0,0), rr,1)

    pygame.draw.line(scree, (0,0,250), (node[0]/zoom+mapX,node[1]/zoom+mapY),((node[0]/zoom+mapX)+node[2]/zoom,(node[1]/zoom+mapY)+node[3]/zoom),1)

def searchForPlayer(node):
    drawNode(node)
    
    isOnLeft = isOnleftSide(startPos[0],startPos[1], node)

    print(isOnLeft)

    if isOnLeft:
        return node[13]
    else:
        return node[12]


def drawSubsectors():
    for subsector in subsectors:
        c=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        v=[]
        for size in range(subsector[0]):
            vx=vertexes[segs[subsector[1]+size][0]]
            vy=vertexes[segs[subsector[1]+size][1]]
            l=linedefs[segs[subsector[1]+size][3]]
            v.append([vx[0]/zoom+mapX,vx[1]/zoom+mapY])
            v.append([vy[0]/zoom+mapX,vy[1]/zoom+mapY])
        try:
            pygame.draw.polygon(scree, (c[0],c[1],c[2]), v)
        except: pass

def drawGLSubsectors():
    for glsubsector in glsubsectors:
        c=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        v=[]
        for size in range(glsubsector[0]):
                vx=0
                vy=0
                if glsegs[glsubsector[1]+size][1]==0:
                    vx=vertexes[glsegs[glsubsector[1]+size][0]]
                    v+=[[vx[0]/zoom+mapX,vx[1]/zoom+mapY]]
                else:
                    vx=glvertexes[glsegs[glsubsector[1]+size][0]]
                    v+=[[vx[0]/zoom+mapX,vx[1]/zoom+mapY]]
                if glsegs[glsubsector[1]+size][3]==0:
                    vy=vertexes[glsegs[glsubsector[1]+size][2]]
                    v+=[[vy[0]/zoom+mapX,vy[1]/zoom+mapY]]
                else:
                    vy=glvertexes[glsegs[glsubsector[1]+size][2]]
                    v+=[[vy[0]/zoom+mapX,vy[1]/zoom+mapY]]
        pygame.draw.polygon(scree, (c[0],c[1],c[2]), v)

def drawGLSubsector(glsubsector):
    c=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    v=[]
    for size in range(glsubsector[0]):
            vx=0
            vy=0
            if glsegs[glsubsector[1]+size][1]==0:
                vx=vertexes[glsegs[glsubsector[1]+size][0]]
                v+=[[vx[0]/zoom+mapX,vx[1]/zoom+mapY]]
            else:
                vx=glvertexes[glsegs[glsubsector[1]+size][0]]
                v+=[[vx[0]/zoom+mapX,vx[1]/zoom+mapY]]
            if glsegs[glsubsector[1]+size][3]==0:
                vy=vertexes[glsegs[glsubsector[1]+size][2]]
                v+=[[vy[0]/zoom+mapX,vy[1]/zoom+mapY]]
            else:
                vy=glvertexes[glsegs[glsubsector[1]+size][2]]
                v+=[[vy[0]/zoom+mapX,vy[1]/zoom+mapY]]
    pygame.draw.polygon(scree, (c[0],c[1],c[2]), v)
        
    
def drawSegs():
    for subsector in subsectors:
        c=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        for size in range(subsector[0]):
            vx=vertexes[segs[subsector[1]+size][0]]
            vy=vertexes[segs[subsector[1]+size][1]]
            pygame.draw.line(scree, (c[0],c[1],c[2]), (vx[0]/zoom+mapX,vx[1]/zoom+mapY),(vy[0]/zoom+mapX,vy[1]/zoom+mapY))


def drawGLSegs():
    for glsubsector in glsubsectors:
        c=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        glvv=[]
        for glv in glvertexes:
            glvx=glv[0]/zoom+mapX
            glvy=glv[1]/zoom+mapY
            glvv.append([glvx,glvy])
        vs=vertexes
        for size in range(glsubsector[0]):
            try:
                vx=vs[glsegs[glsubsector[1]+size][0]]
                vy=vs[glsegs[glsubsector[1]+size][1]]
                pygame.draw.line(scree, (c[0],c[1],c[2]), (vx[0]/zoom+mapX,vx[1]/zoom+mapY),(vy[0]/zoom+mapX,vy[1]/zoom+mapY))
            except: pass

def chooseType():
    a = input("[1] - Render map\n[2] - Render segs\n[3] - Render subsectors\n[4] - Search for player\n")
    if a.replace(' ', '') == "1":
        return 1
    elif a.replace(' ', '') == "2":
        return 2
    elif a.replace(' ', '') == "3":
        return 3
    elif a.replace(' ', '') == "4":
        return 4
    else:
        print("Invalid input")
        chooseType()

renderType = chooseType()

# init mouse movement and center mouse on screen
displayCenter = [500,300]
mouseMove = [0, 0]
pygame.mouse.set_pos(displayCenter)

paused = False
run = True
clock = pygame.time.Clock()
curNode = len(glnodes)-1
print(curNode)
getTicksLastFrame=0
tt=0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                paused = not paused
                pygame.mouse.set_pos(displayCenter)   
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                mapY += 100
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                mapY -= 100
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                mapX += 100
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                mapX -= 100
            if event.key == pygame.K_r:
                mapX = 100
                mapY = 500
            if event.key == pygame.K_PLUS:
                zoom -= 2
            if event.key == pygame.K_MINUS:
                zoom += 2
            if event.key == pygame.K_RETURN:
                renderType = chooseType()

    if not paused:
        # get keys
        scree.fill((0,0,0))
        keypress = pygame.key.get_pressed()
        #mouseMove = pygame.mouse.get_rel()

        if renderType==1 or renderType==3 or renderType==4:
            drawWalls()

        drawPlayerDot()

        t = pygame.time.get_ticks()
        deltaTime = (t - getTicksLastFrame) / 1000.0
        getTicksLastFrame = t
        tt+=deltaTime
        if renderType==4:
            if(tt>1):
                if int(curNode & 0x8000):
                    tt=0
                    curNode = len(glnodes)-1
                else:
                    curNode = searchForPlayer(glnodes[curNode])
                    tt=0
            else:
                if not int(curNode & 0x8000):
                    drawNode(glnodes[curNode])


        #drawSegs()
        #drawSubsectors()
        #drawGLSubsectors()
        #debug1(drawGLSubsector[76])
        #drawSectors()

        pygame.display.flip()
        clock.tick()
        pygame.display.set_caption("fps: " + str(clock.get_fps()))



pygame.quit()