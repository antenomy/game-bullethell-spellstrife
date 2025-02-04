import sys, pygame
from settings import *
from functions import *

class Bullet():
    def __init__(self, image_number, angle, position, velocity, number=0):
        self.angle = angle
        self.position = position
        self.velocity = velocity

        # LIST OF PATHS ALLOWS FOR RANDOM OR SPECIFIC COLOUR OF BULLETS ###
        bullet_image_list = ["bullet_a.png", "bullet_b.png","bullet_c.png","bullet_d.png"]
        
        self.image = load_image("enemies/bullets/" + bullet_image_list[image_number], Vector2(10, 10)*SIZE_MULTIPLIER, True)
        self.rotated_image = pygame.transform.rotozoom(self.image, self.angle.angle_to(Vector2(-1, 0)), 1.0)
        self.radius = self.image.get_size()[0] * 0.5

        # IF THE BULLETS ARE AFFECTED SEQUENTIALLY THIS NUMBER LOGS THE ORDER ###
        self.number = number


    def draw(self, screen): # DRAWS BULLET ###
        screen.blit(self.rotated_image, self.position)
    
    
    def move(self): # MOVES THE BULLET WITH RESPECT TO VELOCITY ###
        self.position += self.velocity


    def check_collide(self, player_position, player_radius): # CHECKS FOR COLLISIONS WITH A PLAYER ###
        if self.position.distance_to(player_position) < self.radius + player_radius:

            return True
        else:
            return False


    def check_out_of_bounds(self): # DELETE BULLETS OUTSIDE OF SCREEN ###
        if self.position[0] < -10 or self.position[0] > SCREEN_WIDTH+10:
            return True
        elif self.position[1] < -10 or self.position[1] > SCREEN_HEIGHT+10:
            return True
        else:
            return False