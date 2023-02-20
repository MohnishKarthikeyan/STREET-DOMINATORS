import pygame
import button
from fighter import Fighter
from street import Street
from pygame import mixer
x = 100
y = 100
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
pygame.init()


#create game windows

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Street Dominator")


#game variables
game_paused = False
menu_state = "main"

#define fonts
font = pygame.font.SysFont("arialblack", 40)

#define colours
TEXT_COL = (255, 255, 255)

#load button images
resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
bg_image = pygame.image.load("images/mainmenu.png").convert_alpha()

#create button instances
resume_button = button.Button(304, 125, resume_img, 1)
quit_button = button.Button(336, 375, quit_img, 1)


def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))
'''def intro():
    pygame.mixer.quit()
    movie = pygame.movie.Movie("images/sample.mp4")  
    screen = pygame.display.set_mode(movie.get_size())  
    movie_screen = pygame.Surface(movie.get_size()).convert()  
    movie.set_display(movie_screen)  
    movie.play()  
    playing = True  
    while playing:  
        for event in pygame.event.get():  
         if event.type == pygame.QUIT:  
           movie.stop()  
           playing = False  
        screen.blit(movie_screen,(0,0))  
        pygame.display.update()  
        clock.tick(FPS)  
        pygame.quit()'''
'''def pausebutton():
    pause_button = button.Button(100,100,pause_img,1)'''
'''def paused():
    paused = True
    while paused:
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_r:
            paused = False
          elif event.key ==pygame.K_q:
            pygame.quit()
      screen.fill("black")
      message_to_screen("Paused",white,-100,size="large")
      message_to_screen("Press R to resume and Q to quit",white,25)
      pygame.display.update()
      clock.tick(5)'''
#game loop
run = True
while run:
  draw_bg()
  #screen.fill((52, 78, 91))

  #check if game is paused
  if game_paused == True:
    #check menu state
    if menu_state == "main":
      #draw pause screen buttons
      if resume_button.draw(screen):
        game_paused = False
        Street()
        break

      if quit_button.draw(screen):
        run = False

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      game_paused = True
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()
