import pygame
from settings import *
from functions import *
from pygame.math import Vector2

class Ring():
    def __init__(self, position, angle, velocity):
        self.image = load_image("player/ring.png", (12, 35), True)

        self.angle = angle
        self.velocity = velocity

        self.rotated_image = pygame.transform.rotozoom(self.image, self.angle.angle_to(Vector2(-1, 0)), 1.0)
        self.position = position

        self.scaled_size = Vector2(self.rotated_image.get_size()) * 0.275
        
        # SAVES START SIZE SINCE IT IS RELEVANT FOR THE ANIMATION ###
        self.start_size = Vector2(self.rotated_image.get_size())

        # DESIGNATES THE AMOUNT OF CYCLES A RING EXISTS BEFORE BEING DELETED ###
        self.lifespan = 20

    def fade_draw(self, screen): # MOVES THE RING AND ADJUSTS ITS APPEARANCE BEFORE DRAWING IT ###
        self.position += pygame.math.Vector2.clamp_magnitude(self.velocity.magnitude() * self.angle * -1, 0, 5)
        self.velocity *= DECCELLERATION_RATE

        self.rotated_image.set_alpha(self.lifespan*3)
        self.scaled_size += (((1.04**self.lifespan) - 1)*self.start_size) / self.lifespan

        screen.blit(pygame.transform.scale(self.rotated_image, self.scaled_size), self.position-(Vector2(pygame.transform.scale(self.rotated_image, self.scaled_size).get_size()) * 0.5))
        self.lifespan -= 1
