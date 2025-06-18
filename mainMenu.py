import pygame
import button

pygame.init()

#create game window
screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cricket game")

#game variables
menu = True

#define fonts
font = pygame.font.SysFont("arialblack", 40)

#define colours
text_clr = 'black'

#load button images
battingSymbol_img = pygame.image.load("battingButton.png").convert_alpha()
bowlingSymbol_img = pygame.image.load("bowlingButton.png").convert_alpha()
fieldingSymbol_img = pygame.image.load("fieldingButton.png").convert_alpha()
settingsSymbol_img = pygame.image.load('settingsButton.png').convert_alpha()

#create button instances
batting_button = button.Button(8, 130, battingSymbol_img, 1.1)
bowling_button = button.Button(415, 130, bowlingSymbol_img, 1.1)
fielding_button = button.Button(8, 360, fieldingSymbol_img, 1.1)
settings_button = button.Button(415, 360, settingsSymbol_img, 1.1)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#game loop
running = True
while running:
  

  screen.fill((0,0,255))
  if menu == True:
    draw_text("Main Menu", font, text_clr, 280, 5)
    draw_text("Select an option:", font, text_clr, 210, 50)

    if batting_button.draw(screen):
        print("batting")
    if bowling_button.draw(screen):
        print("bowling")
    if fielding_button.draw(screen):
        print("fielding")
    if settings_button.draw(screen):
        print("settings")

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  pygame.display.update()

pygame.quit()