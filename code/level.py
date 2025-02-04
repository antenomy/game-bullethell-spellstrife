import pygame, random, copy
from settings import *
from event import Event

class Level():
    def __init__(self):
        
        # LIST OF ALL EVENTS IN THE GAME ###
        self.event_list = list()
        
        # TRACKS THE CURRENT STAGE AND STAGE TEXT ANIMATION ###
        self.stage = 0
        self.stage_draw_active = False
        self.stage_draw_count = 0
        
        # LIST OF STAGES THAT BEEN COMPLETED COME YET ###
        self.remaining_stages = copy.deepcopy(STAGE_COUNTS)
        
        
        # STAGE 1 EVENTS ###
        self.event_list.append(Event("surround_bullet_attack", STAGE_COUNTS[0]+60, spawn_frequency=6, bullet_speed=6))
        
        for i in range(10):
            self.event_list.append(Event("spinner_slam", start_count = STAGE_COUNTS[0]+300+(60*i)))
        
        
        # STAGE 2 EVENTS ###   
        self.event_list.append(Event("surround_bullet_attack", start_count = STAGE_COUNTS[1]+60, spawn_frequency=20, honing_aim = True, ring_width_modifier = 0.05, bullet_speed=10))
        self.event_list.append(Event("orb_assault", start_count = STAGE_COUNTS[1]+270))
        
        for i in range(10):
            self.event_list.append(Event("spinner_slam", start_count = STAGE_COUNTS[1]+600+(10*i)))


        # STAGE 3 EVENTS ###
        self.event_list.append(Event("surround_bullet_attack", STAGE_COUNTS[2]+60, spawn_frequency=6, activation_type = "uniform", randomize_speed=True, randomize_angle=True, bullet_speed=6))
        for i in range(10):
            self.event_list.append(Event("spinner_slam", start_count = STAGE_COUNTS[2]+480+(10*i)))
            
        self.event_list.append(Event("surround_bullet_attack", STAGE_COUNTS[2]+900, spawn_frequency=3, activation_type = "random", randomize_speed=True, randomize_angle=True, bullet_speed=5))
        for i in range(10):
            self.event_list.append(Event("spinner_slam", start_count = STAGE_COUNTS[2]+1020+(10*i)))
    

    def level_check(self, frame_count, player_position): # RUNS EVENT CHECK FOR EACH EVENT IN THE GAME ###
        for event in self.event_list:
            event.event_check(frame_count, player_position)
    
    
    def stage_check(self, frame_count): # CHECK IF THE CURRENT STAGE IS CHANGING ###
        if len(self.remaining_stages) > 0:
            if frame_count > self.remaining_stages[0]:
                self.remaining_stages.pop(0)
                self.stage += 1
                self.stage_draw_active = True
    
    
    def draw_stage(self, screen, font): # DRAW THE STAGE TEXT ###
        
        if self.stage_draw_active:
            stage_text_surface = font.render(str(f"STAGE {self.stage}"), False, (255, 255, 255))
            text_surface_size = Vector2(stage_text_surface.get_size())*0.5

            if self.stage_draw_count < 60:
                draw_alpha = self.stage_draw_count*5
            elif self.stage_draw_count < 180:
                draw_alpha = 255
            else:
                draw_alpha = 255 - ((self.stage_draw_count-180)*5)

            stage_text_surface.set_alpha(draw_alpha)
            screen.blit(stage_text_surface, CENTER_VECTOR - text_surface_size)
            self.stage_draw_count += 1
        
        if self.stage_draw_count == 240:
            self.stage_draw_active = False
            self.stage_draw_count = 0
        




