import pygame, sys, copy
from pygame.math import Vector2

from settings import *
from functions import *
from player import Player
from level import Level
from button import Button  
from orb import Orb

def main():
    
    # GENERAL SETUP ###
    pygame.init()
    clock = pygame.time.Clock()

    frame_count = 1
    menu_active = True
    controls_active = False
    game_active = True
    pause_active = False


    # DISPLAY AND SURFACE SETUP ###
    screen = pygame.display.set_mode((SCREEN_WIDTH,  SCREEN_HEIGHT), flags=pygame.SCALED, vsync=1)

    title_screen_image = load_image("general/title_screen.png", transform_size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = load_image("general/background.jpg", transform_size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    bound_box = load_image("general/bound_box.png", transform_size=BOUND_BOX_DIMENSIONS, alpha=True)
    controls_image = load_image("general/control_screen.png", transform_size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    game_over_screen_image = load_image("general/game_over_screen.png", transform_size=(SCREEN_WIDTH, SCREEN_HEIGHT))

    icon = load_image("general/icon.png") 
    life_icon = load_image("player/player.png", transform_size=Vector2(48, 48), alpha=True)
    pause_icon = load_image("general/pause.png", (120, 120), alpha=True)

    pygame.display.set_caption("Spellstrife", str(round(clock.get_fps())))
    pygame.display.set_icon(icon)


    # LEVEL CLASS SETUP ###
    level = Level()


    # PLAYER CLASS SETUP ###
    player = Player(PLAYER_HP, Vector2(HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT), pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE, pygame.K_UP)


    # SCORE SETUP ###
    score = 0
    with open(DIRECTORY + "/data/highscore.txt", "r") as file:
        highscore = int(file.read())
    
    font = pygame.font.Font(DIRECTORY+"/font/monogram.ttf", 50)
    score_counter_surface = font.render("SCORE " + str(score).zfill(5), False, (255, 255, 255))
    highscore_counter_surface = font.render("HIGHSCORE " + str(highscore).zfill(5), False, (255, 255, 255))


    # BUTTON IMAGE SETUP ###
    start_button = Button("menu/start.png", "menu/start_pressed.png", Vector2(HALF_SCREEN_WIDTH-(BUTTON_PIXEL_WIDTH*BUTTON_FACTOR*0.5), (SCREEN_HEIGHT/3)-(BUTTON_PIXEL_HEIGHT*BUTTON_FACTOR*0.5)), Vector2(BUTTON_PIXEL_WIDTH, BUTTON_PIXEL_HEIGHT)*BUTTON_FACTOR, Vector2(BUTTON_PIXEL_WIDTH, BUTTON_PIXEL_HEIGHT-1)*BUTTON_FACTOR)
    controls_button = Button("menu/controls.png", "menu/controls_pressed.png", Vector2(HALF_SCREEN_WIDTH-(BUTTON_PIXEL_WIDTH*BUTTON_FACTOR*0.5), (SCREEN_HEIGHT/2)-(BUTTON_PIXEL_HEIGHT*BUTTON_FACTOR*0.5)), Vector2(BUTTON_PIXEL_WIDTH, BUTTON_PIXEL_HEIGHT)*BUTTON_FACTOR, Vector2(BUTTON_PIXEL_WIDTH, BUTTON_PIXEL_HEIGHT-1)*BUTTON_FACTOR)
    exit_button = Button("menu/exit.png", "menu/exit_pressed.png", Vector2(HALF_SCREEN_WIDTH-(BUTTON_PIXEL_WIDTH*BUTTON_FACTOR*0.5), (2*SCREEN_HEIGHT/3)-(BUTTON_PIXEL_HEIGHT*BUTTON_FACTOR*0.5)), Vector2(BUTTON_PIXEL_WIDTH, BUTTON_PIXEL_HEIGHT)*BUTTON_FACTOR, Vector2(BUTTON_PIXEL_WIDTH, BUTTON_PIXEL_HEIGHT-1)*BUTTON_FACTOR)
    back_button = Button("menu/back.png", "menu/back_pressed.png", Vector2(BUTTON_PIXEL_HEIGHT*BUTTON_FACTOR*0.5, SCREEN_HEIGHT-(BUTTON_PIXEL_HEIGHT*BUTTON_FACTOR*1.5)), Vector2(BUTTON_PIXEL_WIDTH, BUTTON_PIXEL_HEIGHT)*BUTTON_FACTOR, Vector2(BUTTON_PIXEL_WIDTH, BUTTON_PIXEL_HEIGHT-1)*BUTTON_FACTOR)
    button_list = (start_button, controls_button, exit_button)


    # INTRO ANIMATION ###
    fade_screen(screen, title_screen_image, clock)
    pygame.time.delay(1000)
    fade_screen(screen, title_screen_image, clock, True)


    # MENU LOOP ###
    while menu_active:
        exit_check()

        # BUTTON CLICK CHECKS ##
        if exit_button.check_click():
            pygame.quit()
            sys.exit()
        if controls_button.check_click():
            controls_active = True

        
        # CONTROLS LOOP ###
        while controls_active:
            exit_check()
            
            # CHECK BACK BUTTON CLICK ###
            if back_button.check_click():
                controls_active = False

            # DRAW SURFACES ###
            screen.blit(controls_image, (0,0))
            back_button.draw(screen)
            screen_update(clock)


        # BUTTON CLICK CHECK ###
        if start_button.check_click():
            menu_active = False


        # DRAW SURFACES ###
        screen.blit(background_image, (0, 0))
        for button in button_list:
            button.draw(screen)
        screen_update(clock)
    
    pygame.mouse.set_visible(False)


    # TRANSITION ANIMATION ###
    screen_save = screen.copy()
    fade_screen(screen, screen_save, clock, True)

    screen.blit(background_image, (0, 0))
    screen.blit(bound_box, (HALF_SCREEN_WIDTH - (BOUND_BOX_DIMENSIONS[0]*0.5), HALF_SCREEN_HEIGHT - (BOUND_BOX_DIMENSIONS[1]*0.5)))

    screen.blit(score_counter_surface, (HALF_SCREEN_WIDTH-(BOUND_BOX_DIMENSIONS[0]* 0.5), HALF_SCREEN_HEIGHT+(BOUND_BOX_DIMENSIONS[1]*0.5)))
    highscore_counter_surface_size = Vector2(highscore_counter_surface.get_size())
    screen.blit(highscore_counter_surface, (HALF_SCREEN_WIDTH+(BOUND_BOX_DIMENSIONS[0]* 0.5)-highscore_counter_surface_size[0], HALF_SCREEN_HEIGHT+(BOUND_BOX_DIMENSIONS[1]*0.5)))

    player.draw(screen, frame_count)
    
    for iteration in range(min(player.health, 10)):
        screen.blit(life_icon, (16, 16 + iteration*56))

    screen_save = screen.copy()
    fade_screen(screen, screen_save, clock)
    

    # MAIN GAMEPLAY LOOP ###

    while game_active is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                update_highscore(score, highscore)
                game_active = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                update_highscore(score, highscore)
                pause_active = True
        
        
        # PAUSE LOOP ###

        while pause_active is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_active = False
                    pause_active = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pause_active = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                    player.health += 1
            screen.blit(pause_icon, (20, SCREEN_HEIGHT- 140))
            screen_update(clock)
        

        # PLAYER MOVEMENT PROCESSING ###

        player.process_input()
        player.burst_check()
        player.movement() 
        player.bounce_check(HALF_SCREEN_WIDTH, 0)
        player.bounce_check(HALF_SCREEN_HEIGHT, 1)

        player.ring_check()


        # EVENT PROCESSING ###

        level.level_check(frame_count, player.position)


        # DRAW BACKGROUND ###

        screen.blit(background_image, (0, 0))
        screen.blit(bound_box, (HALF_SCREEN_WIDTH - (BOUND_BOX_DIMENSIONS[0]*0.5), HALF_SCREEN_HEIGHT - (BOUND_BOX_DIMENSIONS[1]*0.5)))

        if frame_count % 600 == 0:
            score += 100
        if frame_count % 60 == 0:
            score += 10

        score_counter_surface = font.render("SCORE " + str(score).zfill(5), False, (255, 255, 255))
        highscore_counter_surface = font.render("HIGHSCORE " + str(max(score, highscore)).zfill(5), False, (255, 255, 255))
        highscore_counter_surface_size = Vector2(highscore_counter_surface.get_size())
        
        screen.blit(highscore_counter_surface, (HALF_SCREEN_WIDTH+(BOUND_BOX_DIMENSIONS[0]* 0.5)-highscore_counter_surface_size[0], HALF_SCREEN_HEIGHT+(BOUND_BOX_DIMENSIONS[1]*0.5)))
        screen.blit(score_counter_surface, (HALF_SCREEN_WIDTH-(BOUND_BOX_DIMENSIONS[0]* 0.5), HALF_SCREEN_HEIGHT+(BOUND_BOX_DIMENSIONS[1]*0.5)))


        # DRAW ENTITIES ###

        for ring in player.ring_list: 
            ring.fade_draw(screen)
            if ring.lifespan <= 0:
                player.ring_list.remove(ring)
        
        player.draw(screen, frame_count)

        
        # HANDLE ALL RELEVANT ENEMIES ###

        orb_save = list()

        for event in level.event_list:
            for enemy in event.enemy_list:
                enemy.move() 
                if type(enemy) == Orb:
                    orb_save.append([enemy, event])
                else:
                    if enemy.check_out_of_bounds():
                        event.enemy_list.remove(enemy)
                    elif enemy.check_collide(player.rotated_image_center, player.radius) and not player.hit_invulnerability:
                        event.enemy_list.remove(enemy)
                        player.hit_invulnerability = True
                        player.invulnerability_count = PLAYER_INVULNERABILITY_COUNT
                        player.health -= 1
                    else: 
                        enemy.draw(screen)
        
        for orb_instance in orb_save:
            if orb_instance[0].check_out_of_bounds():
                orb_instance[1].enemy_list.remove(orb_instance[0])
            else: 
                orb_instance[0].draw(screen)

        
        # HIT INVULNERABILITY HANDLING ###
        
        if player.hit_invulnerability:
            player.invulnerability_count -= 1
            if player.invulnerability_count <= 0:
                player.invulnerability_count = 0
                player.hit_invulnerability = False


        # FINAL MISC ###

        level.stage_check(frame_count)
        level.draw_stage(screen, font)
        
        for iteration in range(min(player.health, 10)):
            screen.blit(life_icon, (16, 16 + iteration*56))

        if player.health <= 0:
            screen_save = screen.copy()
            update_highscore(score, highscore)
            fade_screen(screen, screen_save, clock, True)
            fade_screen(screen, game_over_screen_image, clock)
            pygame.time.delay(3000)
            game_active = False
        
        screen_update(clock)
        frame_count += 1

main()
pygame.quit()
sys.exit()