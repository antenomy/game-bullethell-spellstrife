import random, copy
from pygame import Vector2

from settings import *
from functions import *
from bullet import Bullet
from spinner import Spinner
from orb import Orb

class Event():
    def __init__(self, event_type, start_count=0, spawn_frequency=4, activation_type = "sequence", randomize_speed=False, randomize_angle=False, honing_aim = False, ring_width_modifier = 0, randomize_axis = False, bullet_speed=10):
        
    # EVENT VARIABLES ###
        
        # STRING WITH NAME OF EVENT ###
        self.event_type = event_type

        # BOOLEANS AFFECTING SOME OR ALL EVENTS ###
        self.randomize_speed = randomize_speed
        self.randomize_angle = randomize_angle
        self.randomize_axis = randomize_axis
        self.honing_aim = honing_aim 

        # INTS AND FLOATS AFFECTING SOME OR ALL EVENTS ###
        self.start_count = start_count
        self.spawn_frequency = spawn_frequency
        self.ring_width_modifier = ring_width_modifier
        self.bullet_speed = bullet_speed
        
        # STRING AFFECTING WHAT WAY A SURROUND BULLET ATTACK IS ACTIVATED ###
        self.activation_type = activation_type
        

    # ENEMY VARIABLES ###
        
        self.enemy_position_memory = Vector2(0,1)
        self.angle_memory = Vector2(0,1).rotate(random.randint(0, 360))

        self.enemy_list = list()
        self.enemy_number_list = sorted([i for i in range(72)])

        self.random_axis = random.randint(0, 1)
        self.random_direction = random.choice([-1,1])
        self.spawn_count = 0




    def event_check(self, frame_count, player_position): # RUNS THE EVENT METHOD CORRESPONDING TO THE TYPE OF THE EVENT ###
        if self.event_type == "surround_bullet_attack":
            self.surround_bullet_attack(frame_count, player_position)
        elif self.event_type == "spinner_attack":
            self.spinner_attack(frame_count)
        elif self.event_type == "orb_assault":
            self.orb_assault(frame_count)
        elif self.event_type == "spinner_slam":
            self.spinner_slam(frame_count)


    def surround_bullet_attack(self, frame_count, player_position = Vector2(0,0)): # EVENT METHOD ###

        # CREATES BULLETS ###
        if frame_count in range(self.start_count, (self.start_count + (72 * self.spawn_frequency))):
            if frame_count % self.spawn_frequency == 0:
                bullet_colour = 1 if self.honing_aim else 3
                self.enemy_position_memory = CENTER_VECTOR + (Vector2(1, 0.65).elementwise()*(SCREEN_WIDTH*(0.45+self.ring_width_modifier)*self.angle_memory)) - Vector2(8,8)
                self.enemy_list.append(Bullet(bullet_colour, copy.deepcopy(self.angle_memory), copy.deepcopy(self.enemy_position_memory), Vector2(0, 0), self.spawn_count))
                self.spawn_count += 1
                self.angle_memory.rotate_ip(5)

        # IF UNIFROM ACTIVATES ALL AT ONCE ###
        elif self.activation_type == "uniform" and frame_count == self.start_count + (72 * self.spawn_frequency) + 61:
            for enemy in self.enemy_list:
                if self.honing_aim:
                    enemy.angle = (enemy.position - player_position).normalize()
                elif self.randomize_angle:
                    enemy.angle = enemy.angle.rotate(random.randint(-15, 15))
                else:
                    enemy.angle
                enemy.velocity = enemy.angle * -random.uniform(0.1, 3) if self.randomize_speed else enemy.angle * -self.bullet_speed

        # OTHERWISE ACTIVATES ONE AT A TIME WITH DELAY ###
        elif not self.activation_type == "uniform" and frame_count in range(self.start_count + (72 * self.spawn_frequency) + 60, self.start_count + (2 * 72 * self.spawn_frequency) + 60):
            if frame_count % self.spawn_frequency == 0 and len(self.enemy_number_list) > 0:
                activate_enemy_number = random.choice(self.enemy_number_list) if self.activation_type == "random" else self.enemy_number_list[0]
                for enemy in self.enemy_list:
                    if enemy.number == activate_enemy_number:
                        if self.honing_aim:
                            enemy.angle = (enemy.position - player_position).normalize()
                        elif self.randomize_angle:
                            enemy.angle = enemy.angle.rotate(random.randint(-15, 15))
                        else:
                            enemy.angle

                        enemy.velocity = enemy.angle * -random.uniform(0.1, 3) if self.randomize_speed else enemy.angle * -self.bullet_speed
                        if activate_enemy_number in self.enemy_number_list:
                            self.enemy_number_list.remove(activate_enemy_number)
    

    def spinner_attack(self, frame_count): # EVENT METHOD ###
        if frame_count == self.start_count:
            velocity_angle = Vector2(0,-5).rotate(random.randint(-20,20))
            self.enemy_list.append(Spinner(copy.deepcopy(velocity_angle), Vector2(CENTER_VECTOR[0], SCREEN_HEIGHT+20), copy.deepcopy(velocity_angle*1.5)))


    def orb_assault(self, frame_count): # EVENT METHOD ###
        
        # CREATES AN ORB AT START COUNT ###
        if frame_count == self.start_count:
            self.enemy_list.append(Orb(Vector2(-40, SCREEN_HEIGHT-100), Vector2(ORB_SPEED, 0), 1))
            
        # CYCLES THROUGH 4 ANIMATION STAGES AND SPAWNS BULLETS ON THE 2ND ###
        if len(self.enemy_list) > 0:
            if type(self.enemy_list[0]) is Orb:
                if frame_count % ORB_ANIMATION_INTERVAL == ORB_ANIMATION_INTERVAL*1/4:
                    self.enemy_list[0].acceleration = 0.97
                elif frame_count % ORB_ANIMATION_INTERVAL == ORB_ANIMATION_INTERVAL*2/4:
                    self.enemy_list[0].acceleration = 0
                    for i in range(10):
                        self.enemy_list.append(Bullet(0, copy.deepcopy(Vector2(-1, -1).rotate(i*-5)), copy.deepcopy(self.enemy_list[0].position + (Vector2(self.enemy_list[0].image.get_size()) * 0.5)), copy.deepcopy(Vector2(-3, -3).rotate(i*9))))
                elif frame_count % ORB_ANIMATION_INTERVAL == ORB_ANIMATION_INTERVAL*3/4:
                    self.enemy_list[0].velocity = Vector2(ORB_SPEED/(ORB_ANIMATION_INTERVAL/4), 0)
                    self.enemy_list[0].velocity_memory = Vector2(ORB_SPEED/(ORB_ANIMATION_INTERVAL/4), 0)
                    self.enemy_list[0].acceleration = 1
                if frame_count % ORB_ANIMATION_INTERVAL == 0:
                    self.enemy_list[0].velocity = Vector2(ORB_SPEED, 0)
                    self.enemy_list[0].acceleration = 1
                

    def spinner_slam(self, frame_count): # EVENT METHOD ###
        
        # SPAWNS AND SETS A STARTING POSITION FOR THE ENEMY FROM EARLIER RANDOM VARIABLES ###
        if frame_count == self.start_count:
            spawn_position_coord_a = CENTER_VECTOR[self.random_axis]+(BOUND_BOX_DIMENSIONS[self.random_axis]*random.uniform(-0.45, 0.45))
            spawn_position_coord_b = ((self.random_direction+1)*0.5*SCREEN_VECTOR[1-self.random_axis])+(self.random_direction*20)
            spawn_position = Vector2(spawn_position_coord_a, spawn_position_coord_b) if self.random_axis == 0 else Vector2(spawn_position_coord_b, spawn_position_coord_a)
            
            spawn_velocity = Vector2(self.random_direction*-1*self.random_axis, self.random_direction*(self.random_axis-1))*2

            self.enemy_list.append(Spinner(Vector2(0, -1), copy.deepcopy(spawn_position), copy.deepcopy(spawn_velocity)))
            
        # STOPS THE SPINNERS MOVEMENT AFTER 30 CYCLES ###
        elif frame_count == self.start_count + 30:
            for enemy in self.enemy_list:
                enemy.velocity = Vector2(0, 0)
        
        # RESUMES THE SPINNERS MOVEMENT AFTER ANOTHER 90 CYCLES ###
        elif frame_count == self.start_count+120:
            for enemy in self.enemy_list:
                enemy.velocity = enemy.spawn_velocity*3