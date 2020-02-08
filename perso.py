
import pygame
from pygame.locals import *
import numpy as np
import PIL.Image
import PIL.ImageDraw
from matplotlib import pyplot as plt

def gen_rotation_transformation(origine, theta) :

    def rot_tr(xy, origine=origine, theta=theta) :

        xy = np.array(xy)
        rot = np.array([[np.cos(theta), -np.sin(theta)],
                        [np.sin(theta),  np.cos(theta)]])
        transformed = np.dot(rot, xy) + np.array(origine)  # rotation + translation
        return tuple(np.round(transformed).astype(int))

    return rot_tr

class Obj:

    def __init__(self, fenetre, pos, size) :

        self.fenetre = fenetre
        self.pos = pos
        self.image = pygame.Surface((size,size))
        self.image.fill((0,0,0))
        self.segment = [pos+np.array([[0+1,0+1],[0,size]]),
                        pos+np.array([[0+1,0+1],[size,0]]),
                        pos+np.array([[0,size],[size+1,size+1]]),
                        pos+np.array([[size,0],[size+1,size+1]])]

    def show(self) :

        self.fenetre.blit(self.image, self.pos)

    def get_segment(self) :

        return self.segment


class WalkAnimation() :

    def __init__(self) :

        self.walk = list()
        self.walk.append(pygame.image.load("assets/walk0.png").convert_alpha())
        self.walk.append(pygame.image.load("assets/walk1.png").convert_alpha())
        self.walk.append(pygame.image.load("assets/walk3.png").convert_alpha())
        self.walk.append(pygame.image.load("assets/walk4.png").convert_alpha())
        self.walk.append(pygame.image.load("assets/walk3.png").convert_alpha())
        self.walk.append(pygame.image.load("assets/walk1.png").convert_alpha())

    def walkframe(self) :
        i = 0
        max_iter = 6
        while True :
            i += 1
            if i == max_iter :
                i = 0
            yield self.walk[i]

class Perso :
    def __init__(self, fenetre) :
        self.fenetre = fenetre
        self.real_pos = (100,230)
        self.angle = 0
        self.flashlight = LightSource()
        self.lightpower = LightSource(pos = (300,350),
                                      angle = 0,
                                      aperture = 2*np.pi,
                                      lenght = 200,
                                      intensity = 100,
                                      decrease_rate = 30,
                                      resolution = 25)

        wg = WalkAnimation()
        self.walkframe = wg.walkframe()

    def show(self):

        self.fenetre.blit(self.new_im, self.rect_pos)

    def update(self):

        self.gen_new_frame()
        # new rect pos (perso position for pygame)
        self.set_rect_pos()
        # update flashlight pos
        self.flashlight.pos = self.real_pos
        # update light angle
        self.flashlight.angle = self.angle

    def gen_new_frame(self) :

        frame = next(self.walkframe)
        angle = -90 - self.angle * 180 / np.pi # degree
        self.new_im = pygame.transform.rotate(frame, angle)

    def set_rect_pos(self) :

        R = 22.62
        theta = self.angle%(np.pi/2) + np.pi/4
        pos = self.real_pos
        self.rect_pos = (pos[0] - R*np.sin(theta),
                         pos[1] - R*np.sin(theta))

    def move_toward(self) :

        v = 3
        x = self.real_pos[0] + round(v*np.cos(self.angle))
        y = self.real_pos[1] + round(v*np.sin(self.angle))
        self.real_pos = (x,y)

        self.update()

    def rotate(self, direction):

        if direction == "RIGHT" :
            self.angle += np.pi/10
        if direction == "LEFT" :
            self.angle -= np.pi/10

        self.update()

##############################################################################
    def move_toward_mouse(self, pos_mouse) :

        # get next walk animation index
        self.walk_frame += 1
        if self.walk_frame >= 6 :
            self.walk_frame = 0

        # make perso turn on self
        angle = self.turn_to_mouse(pos_mouse)

        # move perso in mouse direction
        velocity = 3
        x = self.real_pos[0] + round(velocity*np.cos(angle))
        y = self.real_pos[1] + round(velocity*np.sin(angle))
        self.real_pos = (x,y)

        # update light position
        self.flashlight.pos = self.real_pos


    def turn_to_mouse(self, pos_mouse):

        try :
            # get angle between x axe and pos_mouse
            dy = pos_mouse[1] - self.real_pos[1]
            dx = pos_mouse[0] - self.real_pos[0]
            self.angle =   np.pi * (dx<0) + (np.arctan(dy/dx)) # rad
            angle = self.angle * 180 / np.pi # degree
            # rotate image
            self.new_im = pygame.transform.rotate(self.walk[self.walk_frame], -90-angle)
            # compute rect position for pygame
            R = 22.62
            theta = self.angle%(np.pi/2) + np.pi/4
            self.rect_pos = (self.real_pos[0] - R*np.sin(theta),
                   self.real_pos[1] - R*np.sin(theta))

            # update light angle
            self.flashlight.angle = self.angle

            return self.angle

        except :
            print( "divide by zero")
            return self.walk[0]
##############################################################################

class LightSource :

    def __init__(self, pos=(0,0), angle=0, aperture=np.pi/5, lenght=200, intensity=120, decrease_rate=25, resolution=25) :
        self.status = False
        self.pos = pos
        self.angle = angle # in rad : angle of the light axe with x coord
        self.aperture = aperture # in rad : "thickness" of the light
        self.lenght = lenght # in pixel : lighed zone length
        self.intensity = intensity # transparency of shadow layer
        self.decrease_rate = decrease_rate # transparency per pixel
        self.resolution = resolution



