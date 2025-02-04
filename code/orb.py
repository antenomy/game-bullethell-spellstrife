import sys, pygame
from settings import *
from functions import *

class Orb():
    def __init__(self, position, velocity, acceleration):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

        self.velocity_memory = Vector2(0, 0)
        
        self.image = load_image("enemies/orb.png", Vector2(64, 64), True)
        self.radius = self.image.get_size()[0] * 0.5


    def draw(self, screen):
        screen.blit(self.image, self.position)
    
    
    def move(self): # MOVES THE ORB WITH RESPECT TO VELOCITY AND ADJUSTS THAT VELOCITY ###
        self.position += self.velocity
        
        if self.acceleration < 1:
            self.velocity *= self.acceleration
        else:
            self.velocity += self.velocity_memory * self.acceleration
        
        if self.velocity.magnitude() <= 0.01:
            self.velocity = Vector2(0, 0)
            self.acceleration = 0


    def check_out_of_bounds(self): # DELETE BULLETS OUTSIDE OF SCREEN ###
        
        if self.position[0] < -70 or self.position[0] > SCREEN_WIDTH+70:
            return True
        elif self.position[1] < -70 or self.position[1] > SCREEN_HEIGHT+70:
            return True
        else:
            return False