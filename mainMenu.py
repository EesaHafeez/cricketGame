import pygame 
import button
import fielding
import bowling

pygame.init()

# create game window
screen_width = 800
screen_height = 450
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cricket game")
pygame.display.set_icon(pygame.image.load('images/cricketLogo.png'))

# define fonts
font = pygame.font.SysFont("arialblack", 40)

# define colours
text_clr = 'black'

# load button images
battingSymbol_img = pygame.image.load("images/battingButton.png").convert_alpha()
bowlingSymbol_img = pygame.image.load("images/bowlingButton.png").convert_alpha()
fieldingSymbol_img = pygame.image.load("images/fieldingButton.png").convert_alpha()
settingsSymbol_img = pygame.image.load('images/settingsButton.png').convert_alpha()

# create button instances
batting_button = button.Button(65, 87, battingSymbol_img, 0.95)
bowling_button = button.Button(409, 87, bowlingSymbol_img, 0.95)
fielding_button = button.Button(65, 272, fieldingSymbol_img, 0.95)
settings_button = button.Button(409, 272, settingsSymbol_img, 0.95)

# subroutine to draw text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# game loop
running = True
mode = "menu"   # can be "menu", "bowling", "fielding"

while running:
    screen.fill((0,0,255))

    if mode == "menu":
        draw_text("Main Menu", font, text_clr, 280, 0)
        draw_text("Select an option:", font, text_clr, 210, 32)
        
        if batting_button.draw(screen):
            print("batting")
        if bowling_button.draw(screen):
            mode = "bowling"
        if fielding_button.draw(screen):
            mode = "fielding"
        if settings_button.draw(screen):
            print("settings")

    elif mode == "bowling":
        result = bowling.run_bowling_game(screen)
        if result == "menu": # returned when Home is pressed
            mode = "menu"

    elif mode == "fielding":
        result = fielding.run_fielding_game(screen)
        if result == "menu": # returned when Home is pressed
            mode = "menu"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
