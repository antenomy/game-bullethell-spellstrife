import pygame
from settings import *

def load_image(file, transform_size=False, alpha=False):
    file_path = DIRECTORY+"/images/"+file

    if transform_size is False:
        loaded_image = pygame.image.load(file_path)
    else:
        loaded_image = pygame.transform.scale(pygame.image.load(file_path), transform_size)

    if alpha is True:
        return loaded_image.convert_alpha()
    else:
        return loaded_image.convert()
    
def update_highscore(score, highscore):
    if type(highscore) is int and type(score) is int:
        if score > highscore:
            with open(DIRECTORY+"/data/highscore.txt", "w") as file:
                file.write(str(score))
                file.close()
        
def exit_check(score = False, highscore = False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            update_highscore(score, highscore)
            pygame.quit()
            sys.exit()

def fade_screen(screen, underlying_image, clock, fade_in = False, colour = (0, 0, 0)):
    screen_fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen_fade.fill(colour)

    if fade_in:
        screen_start_alpha = 0
        fade_multiplier = 1
    else:
        screen_start_alpha = 300
        fade_multiplier = -1


    for i in range(150):
        exit_check()

        pygame.time.delay(1)
        screen_fade.set_alpha(screen_start_alpha+(fade_multiplier*i*2))

        screen.blit(underlying_image, (0, 0))
        screen.blit(screen_fade, (0, 0))

        screen_update(clock)

def screen_update(clock):
    pygame.display.set_caption("Spellstrife " + str(round(clock.get_fps())))  
    pygame.display.update()
    clock.tick(SCREEN_FPS)