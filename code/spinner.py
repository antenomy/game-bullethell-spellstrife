import pygame, copy
from settings import *
from functions import *

class Spinner():
    def __init__(self, spawn_angle, spawn_position, spawn_velocity):
        self.angle = spawn_angle
        self.position = spawn_position
        self.spawn_velocity = copy.deepcopy(spawn_velocity)
        self.velocity = copy.deepcopy(spawn_velocity)
        
        self.image = load_image("enemies/spinner.png", Vector2(16, 64), True)
        self.rotated_image = pygame.transform.rotozoom(self.image, self.angle.angle_to(Vector2(-1, 0)), 1.0)
        self.rotated_image_center = Vector2(self.rotated_image.get_size()) * 0.5
        self.radius = self.image.get_size()[1] * 0.5 + 5


    def draw(self, screen): # DRAWS AND ROTATES THE SPINNERS SURFACE ###
        self.angle.rotate_ip(37)
        self.rotated_image = pygame.transform.rotozoom(self.image, self.angle.angle_to(Vector2(-1, 0)), 1.0)
        draw_position = Vector2(self.rotated_image.get_size()) * 0.5
        screen.blit(self.rotated_image, self.position.elementwise() - draw_position)
    
    def move(self):
        self.position += self.velocity

    def check_collide(self, player_position, player_radius): # CHECK FOR COLLISIONS BETWEEN SPINNER AND PLAYER ###
        if self.position.distance_to(player_position) < self.radius + player_radius:
            return True
        else:
            return False


    def check_out_of_bounds(self): # DELETE SPINNERS OUTSIDE OF SCREEN ###
        if not int(round(self.position[0], 0)) in range(-350, SCREEN_WIDTH+350):
            return True
        elif not int(round(self.position[1], 0)) in range(-350, SCREEN_HEIGHT+350):
            return True
        else:
            return False