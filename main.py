import pygame
import button
from fighter import Fighter
from pygame import mixer
x = 100
y = 100
import os
import sys
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
pygame.init()

def Street():
  i=0
  victory=False
  x=100
  y=100
  os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

  mixer.init()
  pygame.init()

  #create game windows
  SCREEN_WIDTH = 1000
  SCREEN_HEIGHT = 600

  screen = pygame.display.set_mode((SCREEN_WIDTH+100, SCREEN_HEIGHT))
  pygame.display.set_caption("STREET DOMINATORS")

  #set framerate
  clock = pygame.time.Clock()
  FPS = 60

  #define colours
  RED = (255, 0, 0)
  YELLOW = (255, 255, 0)
  WHITE = (255, 255, 255)

  #define game variables
  intro_count = 3
  last_count_update = pygame.time.get_ticks()
  score = [0, 0]#player scores. [P1, P2]
  round_over = False
  ROUND_OVER_COOLDOWN = 2000

  #define fighter variables
  fire_spirit_SIZE = 128
  fire_spirit_SCALE = 2.5
  fire_spirit_OFFSET = [30, 52]
  fire_spirit_DATA = [fire_spirit_SIZE, fire_spirit_SCALE, fire_spirit_OFFSET]
  WIZARD_SIZE = 128
  WIZARD_SCALE = 2.5
  WIZARD_OFFSET = [72, 50]
  WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

  #load music and sounds
  pygame.mixer.music.load("assets/audio/music.mp3")
  pygame.mixer.music.set_volume(0.5)
  pygame.mixer.music.play(-1, 0.0, 5000)
  sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
  sword_fx.set_volume(0.5)
  magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
  magic_fx.set_volume(0.75)

  #load background image
  bg1_image = pygame.image.load("assets/images/background/background_image.jfif").convert_alpha()
  bg2_image = pygame.image.load("assets/images/background/backround1.png").convert_alpha()
  bg3_image = pygame.image.load("assets/images/background/backround2.png").convert_alpha()
  bg4_image = pygame.image.load("assets/images/background/backround3.png").convert_alpha()
  bg5_image = pygame.image.load("assets/images/background/backround4.png").convert_alpha()
  backround=[bg1_image,bg2_image,bg3_image,bg4_image,bg5_image]

  #load spritesheets
  fire_spirit_sheet = pygame.image.load("assets/images/warrior/Sprites/Fire_Spirit.png").convert_alpha()
  #wizard_sheet = pygame.image.load("assets/images/fire_spirit/Sprites/fire_spirit.png").convert_alpha()
  wizard_sheet = pygame.image.load("assets/images/warrior/Sprites/Magician_Square1.png").convert_alpha()

  #load vicory image
  victory_img = pygame.image.load("assets/images/icons/victory2.jpg").convert_alpha()

  #define number of steps in each animation
  fire_spirit_ANIMATION_STEPS = [7, 8, 9, 5, 8, 3, 6,14]
  WIZARD_ANIMATION_STEPS = [8,8,8,7,18,4,4,15]
  #WIZARD_ANIMATION_STEPS = [10,8,1,7,7,3,7]

  #define font
  count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
  score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

  #function for drawing text
  def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

  #function for drawing background
  def draw_bg():
    scaled_bg = pygame.transform.scale(backround[i], (SCREEN_WIDTH+100, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

  #function for drawing fighter health bars
  def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 3, y - 3, 406, 36))
    pygame.draw.rect(screen, WHITE, (x - 3, y - 3, 406, 36))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

  def draw_special_bar(special, x, y,COLOUR1,COLOUR2):
    ratio = special / 100
    pygame.draw.rect(screen, WHITE, (x - 3, y - 3, 200, 36))
    pygame.draw.rect(screen, COLOUR1, (x, y, 195, 30))
    pygame.draw.rect(screen, COLOUR2, (x, y, 195 * ratio, 30))

  #create two instances of fighters
  fighter_1 = Fighter(1, 200, 310, False, fire_spirit_DATA, fire_spirit_sheet, fire_spirit_ANIMATION_STEPS, sword_fx)
  fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

  #game loop
  run = True
  while run:

    clock.tick(FPS)

    #draw background
    draw_bg()

    #show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 685, 20)
    draw_special_bar(fighter_1.special, 20, 550,RED,YELLOW)
    draw_special_bar(fighter_2.special, 885, 550,YELLOW,RED)
    draw_text("Player 1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("Player 2: " + str(score[1]), score_font, RED, 685, 60)

    #update countdown
    if intro_count <= 0:
      #move fighters
      fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
      fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
      #display count timer
      draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
      #update count timer
      if (pygame.time.get_ticks() - last_count_update) >= 1000:
        intro_count -= 1 #for the count display
        last_count_update = pygame.time.get_ticks()

    #update fighters
    fighter_1.update()
    fighter_2.update()

    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #check for player defeat
    if round_over == False:
      if(fighter_1.alive==False and fighter_2.alive==False):
        round_over = True
        #Insert the Draw Image
        #screen.blit(victory_img, (360, 150))
        round_over_time = pygame.time.get_ticks()
      elif fighter_1.alive == False:
        score[1] += 1
        round_over = True
        round_over_time = pygame.time.get_ticks()
      elif fighter_2.alive == False:
        score[0] += 1
        round_over = True
        round_over_time = pygame.time.get_ticks()
    else:
      #display victory image
      if score[0]==3:
        score[0]=0
        score[1]=0
        victory=True
      elif score[1]==3:
        score[0]=0
        score[1]=0
        victory=True

      if i+1==5:
        i=0
      else:
        i+=1
      screen.blit(victory_img, (140, 60))
      if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
        round_over = False
        intro_count = 3
        fighter_1 = Fighter(1, 200, 310, False, fire_spirit_DATA, fire_spirit_sheet, fire_spirit_ANIMATION_STEPS, sword_fx)
        fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

    #event handler
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.mixer.quit()
        return
        run = False


    #update display
    pygame.display.update()

  #exit pygame
  pygame.quit()


#create game windows

SCREEN_WIDTH = 1100
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
fight_img = pygame.image.load("images/Fight.png").convert_alpha()
quit_img = pygame.image.load("images/Quit.png").convert_alpha()
bg_image = pygame.image.load("images/mainmenu.png").convert_alpha()
guide_img=pygame.image.load("images/Guide.png").convert_alpha()
tut_img=pygame.image.load("assets/images/background/Tutorial.png").convert_alpha()
back_img=pygame.image.load("images/button_back.png").convert_alpha()

#create button instances
fight_button = button.Button(10, 250, fight_img , 0.45)
quit_button = button.Button(930, 250, quit_img, 0.4)
guide_button = button.Button(930, 350, guide_img, 0.4)
back_button = button.Button(950, 520, back_img, 1)



def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def draw_bg(screen1):
  scaled_bg = pygame.transform.scale(screen1, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#game loop
run = True
menu_state="main"
while run:
  if menu_state=="main":
    draw_bg(bg_image)
  #screen.fill((52, 78, 91))
  #check if game is paused
  if game_paused == True:
    #check menu state
    if menu_state == "main":
      #draw pause screen buttons
      if fight_button.draw(screen):
        game_paused = False
        Street()
        game_paused=True
      if quit_button.draw(screen):
        run = False
      if guide_button.draw(screen):
        menu_state="guide"
        draw_bg(tut_img)
    if menu_state=="guide":
      if back_button.draw(screen):
        menu_state="main"
  #event handler
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      game_paused = True
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()
