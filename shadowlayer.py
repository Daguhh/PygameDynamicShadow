import pygame
from pygame.locals import *
import numpy as np
import PIL
import time

from perso import Perso, Obj
from math_tools import get_intersections_list

class ShadowLayer :

    def __init__(self, fenetre) :

        self.fenetre = fenetre
        self.darkness_intensity = 230
        self.resolution = 15

        # init
        self.im = PIL.Image.new("RGBA",
                                (640,480),
                                (0,0,0,self.darkness_intensity))
        self.layer = PIL.ImageDraw.Draw(self.im)

        self.sources = list()
        self.occultants = list()

        self.polygons = 0

    def clear(self) :

        self.im.paste((0,0,0,self.darkness_intensity), [0,0,self.im.size[0],self.im.size[1]])

    def get_source_rect(self, pos, lenght, angle, aper) :
        """ define a rectangle containing lighted zone"""
        p1 = pos
        p2 = pos +lenght * np.array([np.cos(angle + aper),
                                     np.sin(angle + aper)])
        p3 = pos + lenght * np.array([np.cos(angle - aper),
                                      np.sin(angle - aper)])
        x0 = np.min([p1[0], p2[0], p3[0]])
        x1 = np.max([p1[0], p2[0], p3[0]])
        y0 = np.min([p1[1], p2[1], p3[1]])
        y1 = np.max([p1[1], p2[1], p3[1]])

        rect = np.array([[x0,y0], [x1, y1]])

        return rect

    def add_light(self) :
        """ make hole in shadow layer
            from intersection between light rays and segments, draw triangles
            with two successives interactions points ans source
            those triangles are in fact composed of multiples trapezuim that
            transparency decay as they move away from source """

        # list segments of all object that can stop light
        for source in self.sources :
            # rectangular area that can be lighted by source
            source_rect = self.get_source_rect(source.pos,
                                          source.lenght,
                                          source.angle,
                                          source.aperture)
            # search form segment in source_rect area
            segments=list()
            for elmt in self.occultants :
                for sgmt in elmt.segment :
                    if ((sgmt[0,:]>source_rect[0,:]).all() and (sgmt[0,:]<source_rect[1,:]).all())  or  ((sgmt[1,:]>source_rect[0,:]).all() and (sgmt[1,:]<source_rect[1,:]).all()) :
                        segments.append(sgmt)

            # if no segment in the area : create a fake one at distance
            if segments == [] :
                segments = [np.array([[-1000,-1000],[-1001,-1001]])]

            # compute intersection points between rays and segembts
            pts = get_intersections_list(source, segments) #pts[0]

            # source parameters
            pos = source.pos
            I = source.intensity
            R = source.decrease_rate
            L = source.lenght

            # go throught intersections points
            for i in range(len(pts)-1) :

                # vector from source for parametric equations
                dir1 = pts[i] - pos
                dir1_norm = dir1 / np.sqrt(np.dot(dir1,dir1))
                dir2 = pts[i+1] - pos
                dir2_norm = dir2 / np.sqrt(np.dot(dir2,dir2))

                # a,b,c,d are summit of our polygons
                a, b = pos, pos
                last_pt = False
                # go thought polygons
                for j,n in enumerate(np.linspace(0,L,R)) :
                    c = n * dir1_norm + pos
                    d = n * dir2_norm + pos
                    # stop if n is bigger than source lenght
                    if n > np.sqrt(np.dot(dir1,dir1)) or n > np.sqrt(np.dot(dir2,dir2)) :
                        c = pts[i]
                        d = pts[i+1]
                        last_pt = True
                    # transparency decay as trapezium move away from source
                    color = (0,0,0,I+int(5*j+15*(np.sin(0.3*np.pi*time.time()))**2))
                    # not darker than shadow
                    if color[3] > self.darkness_intensity :
                        color = (0,0,0,self.darkness_intensity)

                    # draw polygon
                    self.layer.polygon([(a[0],a[1]),
                                        (b[0],b[1]),
                                        (c[0],c[1]),
                                        (d[0],d[1])],
                                        fill = color)
                    if last_pt : break
                    # start of the new polygon = end of the old one
                    a,b = d,c

    def gen_color(self, intensity, decrease, variation, variation_intensity) :

        if variation == "sin" :
            pass

    def add_light_debug(self) : # draw light rays

        segments=list()
        for elmt in self.occultants :
            for segment in elmt.segment :
                segments.append(segment)
        if 1 :
            intersec = []
            for source in self.sources :
                intersec = self.get_interactions(source, segments)

                for pt in intersec :
                    self.layer.line([pt[0,0],pt[0,1],pt[1,0],pt[1,1]],(250,0,0))

    def get_pygame_surface(self):

        mode = self.im.mode
        size = self.im.size
        data = self.im.tobytes()

        shadow_surface = pygame.image.fromstring(data, size, mode).convert_alpha()

    def show(self) :
        mode = self.im.mode
        size = self.im.size
        data = self.im.tobytes()

        shadow_surface = pygame.image.fromstring(data, size, mode).convert_alpha()

        self.fenetre.blit(shadow_surface, (0,0))












