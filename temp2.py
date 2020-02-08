import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_DOWN, K_UP

# Game dimensions
screen_width, screen_height = 800, 800

pygame.mixer.pre_init(44100, -16, 2, 2048)  # sounds
pygame.init()

pygame.display.set_caption("Lighting test")  # Set app name
pygame.key.set_repeat(200, 80)           # delay, interval

# Set up game screen
screen = pygame.display.set_mode((screen_width, screen_height))
# Frames per second
fps = 60

# Create a black background so transparent tiles look like shadowed tiles
background = pygame.Surface((screen_width, screen_height))
background.fill((0, 0, 0))
background.convert()

# SRCALPHA flag means that blit uses source alpha blending.
# It is required for pixels_alpha().
image = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

# Let's load an image file to a Surface object.
# We're using a 24x24 png here. You can find it at:
# http://i.imgur.com/hqTvoIt.png
image_to_surface = pygame.image.load("tile.png")
image_to_surface.set_alpha(128)

# Get width and height from Surface
width, height = image_to_surface.get_size()

# Fill the Surface with the tile pattern
i = 0
while i*width < screen_width:
    j = 0
    while j*height < screen_height:
        image.blit(image_to_surface, (width*i, height*j))
        j += 1
    i += 1

# Create a 2d array that contains per-pixel transparency
# values of the Surface. (0-255)
# This is a reference, so it affects original
transparency_array = pygame.surfarray.pixels_alpha(image)

# rectangle 100*100 to fully opaque
width, height = 100, 100  # width and height of the light source
x, y = 200, 200  # x and y position of the center of the light source
transparency_array[round(x-width/2):round(x+width/2), round(y-width/2):round(y+width/2)] = 255
del transparency_array  # this is not a good way to do this


# Take input from user
def take_input():
    for event in pygame.event.get():

        # If for example you click the red x in upper right corner
        if event.type == QUIT:
            return False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return False


def draw():
    screen.blit(background, (0, 0))
    screen.blit(image, (0, 0))
    pygame.display.update()

while True:
    if take_input() is False:
        break
    draw()
pygame.time.Clock().tick(fps)


