import pygame


class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame_x, frame_y, width, height, scale, color=None):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame_x*width),
                   (frame_y*height), width, height))
        image = pygame.transform.scale(image, (width*scale, height*scale))
        image.get_rect().center = (0, 0)
        image.set_colorkey(color)
        return image
