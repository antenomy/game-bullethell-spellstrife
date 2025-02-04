import pygame
from settings import *
from functions import *

class Button():
    def __init__(self, image_name, image_clicked_name, position, size, clicked_size):

        self.image = load_image(image_name, size, True)
        self.image_clicked = load_image(image_clicked_name, clicked_size, True)
        
        self.position = position
        self.size = size
        
        # LOGS IF MOUSE HAS CLICKED ON A BUTTON THIS CYCLE ###
        self.active_click = False
        
        # LOGS IF MOUSE WAS CLICKED ANYWHERE LAST CYCLE ###
        self.click_state_memory = False
        
        # BUFFER TO ALLOW TIME FOR ANIMATION ###
        self.click_buffer = 0


    def draw(self, screen): # DRAWS THE BUTTON ###
        screen.blit(self.image_clicked if self.active_click else self.image, self.position + Vector2(0, BUTTON_FACTOR) if self.active_click else self.position) 


    def check_click(self): # CHECKS FOR CLICKS AND MOUSE POSITIONING ###
        cursor_x, cursor_y = pygame.mouse.get_pos()
        left_click, right_click, middle_click = pygame.mouse.get_pressed()

        # RETURNS TRUE IF CLICK IS REGISTERED AFTER BUFFER PERIOD FOR ANIMATION TIME ###
        if self.click_buffer > 1:
            self.click_buffer -= 1
        elif self.click_buffer == 1:
            self.click_buffer = 0
            return True

        # CHECK FOR MOUSE POSITION ###
        if cursor_x in range(int(self.position[0]), int(self.position[0]+self.size[0])) and cursor_y in range(int(self.position[1]), int(self.position[1]+self.size[1])):
            cursor_on_button = True
        else:
            cursor_on_button = False

        # CHECK FOR NEW CLICK IN RIGHT POSITION ###
        if left_click and cursor_on_button and not self.click_state_memory:
            self.active_click = True
        
        # CHECK FOR CLICK RELEASE ###
        elif cursor_on_button and self.active_click and not left_click:
            self.active_click = False
            self.click_buffer = 3
        elif not left_click or not cursor_on_button:
            self.active_click = False
        
        # SAVE CURRENT STATE TO COMPARE DURING NEXT CYCLE ###
        self.click_state_memory = left_click 
