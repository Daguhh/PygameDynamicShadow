import pygame
from pygame.locals import *
import numpy as np
import PIL

from perso import Perso, Obj
from math_tools import *
from shadowlayer import ShadowLayer


pygame.init()
pygame.key.set_repeat(400, 30)
ecran = pygame.display.set_mode((640, 480), RESIZABLE)

background = pygame.image.load("assets/background.png")

perso = Perso(ecran)
list_obj=[]
obj_num = 30
for i in range(obj_num) :
    list_obj.append(Obj(ecran, (np.random.randint(640), np.random.randint(480)), np.random.randint(70)+30))


shadow_layer = ShadowLayer(ecran)
shadow_layer.sources=[]
shadow_layer.occultants=[]
shadow_layer.sources.append(perso.flashlight)
#shadow_layer.sources.append(perso.lightpower)
for obj in list_obj :
    shadow_layer.occultants.append(obj)
continuer = True
perso.move_toward()
perso.rotate("LEFT")
while continuer:

# gameplay loop

    mouse_pos = pygame.mouse.get_pos()
    #perso.turn_to_mouse(mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_LEFT :
                perso.rotate("LEFT")
            elif event.key == K_RIGHT :
                perso.rotate("RIGHT")
            elif event.key == K_UP :
                perso.move_toward()

    shadow_layer.clear()
    shadow_layer.add_light()

# render

    ecran.blit(background, (0,0))
    for obj in list_obj :
        obj.show()
    perso.show()
    shadow_layer.show()

# display

    pygame.display.flip()

pygame.quit()
