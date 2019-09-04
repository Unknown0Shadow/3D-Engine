import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
from numpy import sin, arccos

pygame.init()
display_width = 800
display_height = 600
display = pygame.display.set_mode((display_width, display_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('OurGame')
gluPerspective(45.0, (display_width / display_height), 1, 50.0)
glTranslatef(-16.0, 0.0, -38.0)
glRotatef(45, 90, 90, 0)
glEnable(GL_DEPTH_TEST)

colours = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1)]


def distance(a, b):
    '''a and b are touples (x,y,z)'''
    return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) ** 2) ** 0.5


def area(a, b, c):
    '''a and b and c are touples (x,y,z)'''
    ab = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    ac = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
    vectorial_product = (ab[0]) * (ac[0]) + (ab[1]) * (ac[1]) + (ab[2]) * (ac[2])
    modular_product = distance(a, b) * distance(a, c)
    try:
        angle = arccos(vectorial_product / modular_product)  # radians
    except:
        angle = arccos(0)
    return sin(angle) * modular_product / 2


def isInside(quad, x, y, z):
    vertexes = []
    for vertex in quad:
        if vertex not in vertexes:
            vertexes.append(vertex)
    if (x, y, z) in vertexes:
        return True
    a1 = area(vertexes[0], vertexes[1], (x, y, z))
    a2 = area(vertexes[1], vertexes[2], (x, y, z))
    if len(vertexes) == 4:
        a3 = area(vertexes[0], vertexes[3], (x, y, z))
        a4 = area(vertexes[2], vertexes[3], (x, y, z))
        ah2 = area(vertexes[0], vertexes[3], vertexes[2])
    if len(vertexes) == 3:
        a3 = area(vertexes[2], vertexes[0], (x, y, z))
        a4 = 0
        ah2 = 0
    ah1 = area(vertexes[0], vertexes[1], vertexes[2])
    if round(a1 + a2 + a3 + a4, 2) == round(ah1 + ah2, 2):
        return True
    return False


def drawCube(x, y, z):
    glBegin(GL_QUADS)
    glColor3fv((1, 1, 1))
    glVertex3fv((x + 0.3, y - 0.3, z - 0.3))
    glVertex3fv((x + 0.3, y - 0.3, z + 0.3))
    glVertex3fv((x - 0.3, y - 0.3, z + 0.3))
    glVertex3fv((x - 0.3, y - 0.3, z - 0.3))

    glVertex3fv((x + 0.3, y + 0.3, z - 0.3))
    glVertex3fv((x + 0.3, y + 0.3, z + 0.3))
    glVertex3fv((x - 0.3, y + 0.3, z + 0.3))
    glVertex3fv((x - 0.3, y + 0.3, z - 0.3))

    glVertex3fv((x + 0.3, y + 0.3, z - 0.3))
    glVertex3fv((x + 0.3, y + 0.3, z + 0.3))
    glVertex3fv((x + 0.3, y - 0.3, z + 0.3))
    glVertex3fv((x + 0.3, y - 0.3, z - 0.3))

    glVertex3fv((x - 0.3, y + 0.3, z - 0.3))
    glVertex3fv((x - 0.3, y + 0.3, z + 0.3))
    glVertex3fv((x - 0.3, y - 0.3, z + 0.3))
    glVertex3fv((x - 0.3, y - 0.3, z - 0.3))

    glVertex3fv((x + 0.3, y - 0.3, z - 0.3))
    glVertex3fv((x + 0.3, y + 0.3, z - 0.3))
    glVertex3fv((x - 0.3, y + 0.3, z - 0.3))
    glVertex3fv((x - 0.3, y - 0.3, z - 0.3))

    glVertex3fv((x + 0.3, y - 0.3, z + 0.3))
    glVertex3fv((x + 0.3, y + 0.3, z + 0.3))
    glVertex3fv((x - 0.3, y + 0.3, z + 0.3))
    glVertex3fv((x - 0.3, y - 0.3, z + 0.3))
    glEnd()


def drawQuads(quads):
    for quad in quads:
        glBegin(GL_QUADS)
        r, g, b = quad[0]
        glColor3f(r, g, b)
        for vertex in quad[1:]:
            glVertex3fv(vertex)
        glEnd()


def drawGrid(n):
    glBegin(GL_LINES)
    for i in range(n):
        glColor3fv((1, 1, 1))
        if i < 20:
            glVertex3fv((i, 0, 0))
            glVertex3fv((i, 0, n // 2))
        if i >= 20:
            glVertex3fv((0, 0, i - n // 2))
            glVertex3fv((n // 2, 0, i - n // 2))
    glEnd()


def main():
    cube_x = cube_y = cube_z = 0
    quads = []
    i = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP4:
                    # glTranslatef(1.0, 0.0, 0.0)
                    cube_x += -1
                elif event.key == pygame.K_KP6:
                    # glTranslatef(-1.0, 0.0, 0.0)
                    cube_x += 1
                elif event.key == pygame.K_KP8:
                    # glTranslatef(0.0, 0.0, 1.0)
                    cube_z += -1
                elif event.key == pygame.K_KP5:
                    # glTranslatef(0.0, 0.0, -1.0)
                    cube_z += 1
                elif event.key == pygame.K_KP9:
                    # glTranslatef(0.0, 0.0, -1.0)
                    cube_y += -1
                elif event.key == pygame.K_KP7:
                    # glTranslatef(0.0, 0.0, -1.0)
                    cube_y += 1
                elif event.key == pygame.K_q:
                    if i % 4 == 0:
                        quads.append([])
                        r, g, b = colours[random.randrange(0, 6)]
                        quads[-1].append((r, g, b))
                        i = 0
                    if len(quads) == 0:
                        quads.append([])
                    quads[-1].append((cube_x, cube_y, cube_z))
                    i+=1
                elif event.key == pygame.K_r:
                    if len(quads) > 0:
                        quads.pop()
                        i = 0
                elif event.key == pygame.K_d:
                    for quad in quads:
                        if len(set(quad)) > 3:
                            if isInside(quad[1:], cube_x, cube_y, cube_z):
                                quads.remove(quad)
                                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0.0, 1.0, 0.0)
                elif event.button == 5:
                    glTranslatef(0.0, -1.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        drawGrid(40)
        drawQuads(quads)
        drawCube(cube_x, cube_y, cube_z)
        pygame.display.flip()
        pygame.time.wait(10)


main()