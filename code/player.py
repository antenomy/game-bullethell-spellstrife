import pygame, random, copy
from settings import *
from functions import *
from pygame.math import Vector2

from ring import Ring

class Player():
    def __init__(self, start_health, start_position, rotate_left_key, rotate_right_key, boost_key, burst_key):
        
        self.image = load_image("player/player.png", PLAYER_SIZE, True)
        self.burst_hold_image = load_image("player/player_burst_hold.png", PLAYER_SIZE, True)
        self.burst_charged_image = load_image("player/player_burst_charged.png", PLAYER_SIZE, True)
        self.hit_image = load_image("player/player_hit.png", PLAYER_SIZE, True)
        self.radius = self.image.get_size()[0] * 0.5
        
        self.health = start_health

        self.rotate_left_key, self.rotate_right_key, self.boost_key, self.burst_key = rotate_left_key, rotate_right_key, boost_key, burst_key

        self.angle = Vector2(-1, 0)
        self.position = start_position
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)

        self.rotated_image_center = self.position

        # USED TO STOP PLAYERS FROM HOLDING SPACE BUTTON ###
        self.space_memory = False

        self.hit_invulnerability = False
        self.invulnerability_count = 0

        self.active_burst = False
        self.holding_burst = False
        self.burst_held_count = 0

        self.ring_list = list()


        
    def process_input(self):

        keys = pygame.key.get_pressed()
        if keys[self.boost_key] and self.space_memory is False and self.holding_burst is False:
            self.acceleration = pygame.math.Vector2.clamp_magnitude(self.acceleration + self.angle * ACCELERATION_RATE, 0, ACCELERATION_LIMIT)
            self.space_memory = True
            
            # ADDS A RING TO THE LIST OF RINGS TO ANIMATE ###
            self.ring_list.append(Ring(copy.deepcopy(self.position + (self.angle*-5)), copy.deepcopy(self.angle), copy.deepcopy(self.velocity)))

        elif self.space_memory and keys[self.boost_key] is False:
            self.space_memory = False

        if keys[self.rotate_right_key] and not keys[self.rotate_left_key]:
            self.angle.rotate_ip(ROTATION_SPEED * 1)
        elif keys[self.rotate_left_key] and not keys[self.rotate_right_key]:
            self.angle.rotate_ip(ROTATION_SPEED * -1)


        if keys[self.burst_key] and self.holding_burst:
            self.burst_held_count += 1
        elif self.holding_burst and not keys[self.burst_key]:
            self.holding_burst = False
            if self.burst_held_count < 15:
                self.burst_held_count = 0
            else:
                self.burst_held_count = min(self.burst_held_count, 60)
                self.active_burst = True
        elif keys[self.burst_key] and not self.holding_burst:
            self.holding_burst = True
            self.burst_held_count = 1

    def burst_check(self):
        if self.active_burst:
            if self.burst_held_count > 0:
                self.burst_held_count -= 3
            else:
                self.active_burst = False
                self.burst_held_count = 0

    def movement(self):

        # CHECK FOR IF PLAYER IS HOLDING BURST ###

        if self.holding_burst:
            self.velocity *= DECCELLERATION_RATE
            self.acceleration *= 0
        else:
            self.velocity += self.acceleration

        
        # CHANGE POSITION BY VELOCITY ###
        
        self.position += self.velocity


        # ADJUST ACCELERATION IF BURST IS ACTIVE OTHERWISE APPLY FRICTION ###
        if self.active_burst and self.burst_held_count == 57:
            self.acceleration = self.angle * 10
        elif self.active_burst and self.burst_held_count > 0:
            self.acceleration = self.angle * (1 + self.burst_held_count/60)
        else:
           self.acceleration *= DECCELLERATION_RATE**2


        # SET SMALL VALUES TO ZERO ###

        if self.velocity.length() < 0.005:
            self.velocity = Vector2(0, 0)
        else:
           self.velocity *= DECCELLERATION_RATE

        if self.acceleration.length() < 0.05:
            self.acceleration = Vector2(0, 0)
    

    def bounce_check(self, center_coordinate, axis): # FUNCTION TO CHECK IF PLAYER BOUNCES ON THE BOUND BOX EDGE ###
        
        # THE EXACT DISTANCE FROM THE CENTER A PLAYER BOUNCES AT ALONG AN AXIS###
        edge_distance = (BOUND_BOX_DIMENSIONS[axis] * 0.5) - (20*BOUND_BOX_FACTOR) - self.radius

        # CHECKS IF PLAYER IS TOUCHING OR PAST AN EDGE ###
        if self.position[axis] <= center_coordinate - edge_distance:
            
            # SETS PLAYER POSITION TO AVOID PASSING THROUGH EDGE ###
            self.position[axis] = center_coordinate - edge_distance + 1
            
            # DECREASES AND INVERTS PLAYERS VELOCITY ACROSS THE RELEVANT AXIS ###
            self.velocity[axis] *= -BOUNCE_DECCELLERATION
            
            # SETS POINTING ANGLE TO THE NEW VELOCITY DIRECTION ###
            self.angle = self.velocity.normalize()
            
            # ALSO ADJUSTS ACCELERATION ALONG THE RELEVANT AXIS ###
            self.acceleration[axis] *= -(BOUNCE_DECCELLERATION**2)
            
        # CHECKS IF PLAYER IS TOUCHING OR PAST THE OPPOSITE EDGE ###
        elif self.position[axis] >= center_coordinate + edge_distance:
            
            # SAME AS PREVIOUS BUT FOR OPPOSITE###
            self.position[axis] = center_coordinate + edge_distance - 1
            self.velocity[axis] *= -BOUNCE_DECCELLERATION
            self.angle = self.velocity.normalize()
            self.acceleration[axis] *= -(BOUNCE_DECCELLERATION**2)


    def ring_check(self): # CHECKS IF A BURST IS ACTIVE AND ADDS RINGS TO ANIMATE DURING SOME OF THE ANIMATION FRAMES ###

        if self.active_burst and self.burst_held_count in range (0,55):
            self.ring_list.append(Ring(copy.deepcopy(self.position + (self.angle*-5)), copy.deepcopy(self.angle), copy.deepcopy(self.velocity)))
            self.ring_list.append(Ring(copy.deepcopy(self.position + (self.angle*-10)), copy.deepcopy(self.angle), copy.deepcopy(self.velocity)))
    

    def draw(self, screen, frame_count):

        # SETS IMAGE TO CORRECT ONE DEPENDING ON MODE ###
        if self.hit_invulnerability:
            image = self.hit_image
        elif self.burst_held_count > 60 and self.holding_burst:
            image = self.burst_charged_image
        elif self.holding_burst:
            image = self.burst_hold_image
        else:
            image = self.image
        
        # ROTATE IMAGE TO MATCH YOUR POINTING DIRECTION ###
        rotated_image = pygame.transform.rotozoom(image, self.angle.angle_to(Vector2(-1, 0)), 1.0)

        # ADD SHAKING EFFECT AND CHANGES VISUAL APPEARANCE WHILE HOLDING BURST ###
        if self.burst_held_count > 90 and self.holding_burst:
            random_shake_vector = Vector2(random.uniform(-1,1) * (self.burst_held_count-29), random.uniform(-1,1) * (self.burst_held_count-29)).clamp_magnitude(0,1)
            self.rotated_image_center = self.position - (Vector2(rotated_image.get_size()) * 0.5) + random_shake_vector
        elif self.burst_held_count > 45 and frame_count % 4 == 0 and self.holding_burst:
            random_shake_vector = Vector2(random.uniform(-1,1) * (self.burst_held_count-29), random.uniform(-1,1) * (self.burst_held_count-29)).clamp_magnitude(0,1)
            self.rotated_image_center = self.position - (Vector2(rotated_image.get_size()) * 0.5) + random_shake_vector
        else:
            self.rotated_image_center = self.position - (Vector2(rotated_image.get_size()) * 0.5)
        
        # DRAWS PLAYER ###
        screen.blit(rotated_image, self.rotated_image_center)
        