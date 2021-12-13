import readWad
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

things = readWad.readMapThings()
vertexes = readWad.readMapVertex()
linedefs = readWad.readMapLinedefs()
sidedefs = readWad.readMapSidedefs()
sectors = readWad.readMapSectors()
subsectors = readWad.readMapSubsectors()
segs = readWad.readMapSegs()
glvertexes= readWad.readMapGLVertex()
glsegs = readWad.readMapGLSegs()
glsubsectors = readWad.readMapGLSubsectors()

def getPlayerPosition():
    for thing in things:
        if thing[3] == 1:
            return [thing[0], thing[1]]
    

def drawWalls():
    glFrontFace(GL_CW)
    glCullFace(GL_BACK)
    for linedef in linedefs:
        l=vertexes[linedef[0]]
        r=vertexes[linedef[1]]
        if linedef[6]==65535: 
            glEnable(GL_CULL_FACE)
            f=sectors[sidedefs[linedef[5]][5]][0]
            c=sectors[sidedefs[linedef[5]][5]][1]

            glColor4f(f/255, c/255, c/255, 1)
            glBegin(GL_QUADS)
            glVertex3f((l[0]-1000)/20, (l[1]+3000)/20, f/20)
            glVertex3f((l[0]-1000)/20, (l[1]+3000)/20, c/20)
            glVertex3f((r[0]-1000)/20, (r[1]+3000)/20, c/20)
            glVertex3f((r[0]-1000)/20, (r[1]+3000)/20, f/20)
            glEnd()
        else:
            glDisable(GL_CULL_FACE)
            f1=sectors[sidedefs[linedef[5]][5]][0]
            f2=sectors[sidedefs[linedef[6]][5]][0]
            c1=sectors[sidedefs[linedef[5]][5]][1]
            c2=sectors[sidedefs[linedef[6]][5]][1]

            glColor4f(f1/255, c1/255, c1/255, 1)
            glBegin(GL_QUADS)
            glVertex3f((l[0]-1000)/20, (l[1]+3000)/20, f1/20)
            glVertex3f((l[0]-1000)/20, (l[1]+3000)/20, f2/20)
            glVertex3f((r[0]-1000)/20, (r[1]+3000)/20, f2/20)
            glVertex3f((r[0]-1000)/20, (r[1]+3000)/20, f1/20)
            glEnd()

            glColor4f(f2/255, c2/255, c2/255, 1)
            glBegin(GL_QUADS)
            glVertex3f((l[0]-1000)/20, (l[1]+3000)/20, c1/20)
            glVertex3f((l[0]-1000)/20, (l[1]+3000)/20, c2/20)
            glVertex3f((r[0]-1000)/20, (r[1]+3000)/20, c2/20)
            glVertex3f((r[0]-1000)/20, (r[1]+3000)/20, c1/20)
            glEnd()

            glEnable(GL_CULL_FACE)


def drawFloor():
    if readWad.useGLnodes():
        for glsubsector in glsubsectors:
            v=[]
            f=0
            c=0
            for size in range(glsubsector[0]):
                    vx=0
                    vy=0
                    if glsegs[glsubsector[1]+size][1]==0:
                        vx=vertexes[glsegs[glsubsector[1]+size][0]]
                        v+=[[(vx[0]-1000)/20,(vx[1]+3000)/20]]
                    else:
                        vx=glvertexes[glsegs[glsubsector[1]+size][0]]
                        v+=[[(vx[0]-1000)/20,(vx[1]+3000)/20]]
                    if glsegs[glsubsector[1]+size][3]==0:
                        vy=vertexes[glsegs[glsubsector[1]+size][2]]
                        v+=[[(vy[0]-1000)/20,(vy[1]+3000)/20]]
                    else:
                        vy=glvertexes[glsegs[glsubsector[1]+size][2]]
                        v+=[[(vy[0]-1000)/20,(vy[1]+3000)/20]]
                    if glsegs[glsubsector[1]+size][4] != 65535:
                        if glsegs[glsubsector[1]+size][5]==0:
                            f=sectors[sidedefs[linedefs[glsegs[glsubsector[1]+size][4]][5]][5]][0]
                            c=sectors[sidedefs[linedefs[glsegs[glsubsector[1]+size][4]][5]][5]][1]
                        else:
                            f=sectors[sidedefs[linedefs[glsegs[glsubsector[1]+size][4]][6]][5]][0]
                            c=sectors[sidedefs[linedefs[glsegs[glsubsector[1]+size][4]][6]][5]][1]

            glColor4f(1, 1, 0, 1)
            glCullFace(GL_BACK)
            glBegin(GL_TRIANGLE_FAN)
            for s in v:
                glVertex3f(s[0],s[1],f/20)
            glEnd()

            glColor4f(0, .2, .2, 1)
            glCullFace(GL_FRONT)
            glBegin(GL_TRIANGLE_FAN)
            for s in v:
                glVertex3f(s[0],s[1],c/20)
            glEnd()
    else:
        for subsector in subsectors:
            glColor4f(1, 1, 0, 1)
            glCullFace(GL_BACK)
            glBegin(GL_TRIANGLE_FAN)
            f=0
            for size in range(subsector[0]):
                vx=vertexes[segs[subsector[1]+size][0]]
                vy=vertexes[segs[subsector[1]+size][1]]
                if segs[subsector[1]+size][4]==0:
                    f=sectors[sidedefs[linedefs[segs[subsector[1]+size][3]][5]][5]][0]
                else:
                    f= sectors[sidedefs[linedefs[segs[subsector[1]+size][3]][6]][5]][0]
                glVertex3f((vx[0]-1000)/20,(vx[1]+3000)/20,f/30)
                glVertex3f((vy[0]-1000)/20,(vy[1]+3000)/20,f/30)
            glEnd()

            glColor4f(1, 0, 1, 1)
            glCullFace(GL_FRONT)
            glBegin(GL_TRIANGLE_FAN)
            f=0
            for size in range(subsector[0]):
                vx=vertexes[segs[subsector[1]+size][0]]
                vy=vertexes[segs[subsector[1]+size][1]]
                if segs[subsector[1]+size][4]==0:
                    c=sectors[sidedefs[linedefs[segs[subsector[1]+size][3]][5]][5]][1]
                else:
                    c= sectors[sidedefs[linedefs[segs[subsector[1]+size][3]][6]][5]][1]
                glVertex3f((vx[0]-1000)/20,(vx[1]+3000)/20,c/30)
                glVertex3f((vy[0]-1000)/20,(vy[1]+3000)/20,c/30)
            glEnd()


pygame.init()
display = (1000, 600)
scree = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)



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

# init mouse movement and center mouse on screen
displayCenter = [500,300]
mouseMove = [0, 0]
pygame.mouse.set_pos(displayCenter)

up_down_angle = 0.0
paused = False
run = True



clock = pygame.time.Clock()
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
            if event.type == pygame.MOUSEMOTION:
                mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]

    if not paused:
        # get keys
        keypress = pygame.key.get_pressed()
    
        # init model view matrix
        glLoadIdentity()

        # apply the look up and down
        if not keypress[pygame.K_q]:
            up_down_angle += mouseMove[1]*0.1
            glRotatef(up_down_angle, 1.0, 0.0, 0.0)

        # init the view matrix
        glPushMatrix()
        glLoadIdentity()


        speed=.3

        # apply the movment 
        if keypress[pygame.K_LSHIFT]:
            speed=1
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

        #glColor4f(1, 1, 1, 1)
        #glBegin(GL_TRIANGLE_FAN)
        #glVertex3f(1, 1, 1)
        #glVertex3f(100, 100, 100)
        #glVertex3f(100, -100, -100)
        #glVertex3f(-100, 0, -100)
        #glEnd()

        glPopMatrix()

        pygame.display.flip()

        clock.tick()
        pygame.display.set_caption("fps: " + str(clock.get_fps()))
        pygame.time.wait(1)
        pygame.mouse.set_pos(displayCenter)  

pygame.quit()