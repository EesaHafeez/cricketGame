# fielding_game.py
import pygame
import random
import button

# Load assets 
pitch_img = pygame.image.load("images/pitch.png")
ball_img = pygame.image.load("images/ball.png")
bird_img = pygame.image.load("images/bird.png")
heart_img = pygame.image.load("images/heart.png")
home_img = pygame.image.load("images/home.png")
resume_img = pygame.image.load("images/resume.png")
restart_img = pygame.image.load("images/restart.png")
pause_img = pygame.image.load("images/pause.png")

# Creating button instances
home_button = button.Button(305, 280, home_img, 1)
resume_button = button.Button(400, 280, resume_img, 1)
restart_button = button.Button(495, 280, restart_img, 1)
pause_button = button.Button(750, 50, pause_img, 0.8)

# ball class
class Ball:
    def __init__(self, x, speed,):
        self.image = ball_img
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed

    def update(self,screen):
        self.rect.y += self.speed
        screen.blit(self.image, self.rect)

# bird class
class Bird:
    def __init__(self, y):
        self.image = bird_img
        self.rect = self.image.get_rect(midleft=(0, y))
        self.speed = 3

    def update(self,screen):
        self.rect.x += self.speed
        if self.rect.left > 800:  # reset bird
            self.rect.right = 0
            self.rect.y = random.randint(50, 250)
        screen.blit(self.image, self.rect)

# subroutine to run game
def run_fielding_game(screen):
    clock = pygame.time.Clock()

    # Game state variables
    game_over = False
    paused = False
    game_started = False

    # Fonts
    font_big = pygame.font.SysFont("arialblack", 40)
    font_small = pygame.font.SysFont("arialblack", 30)

    # subroutine to display text
    def draw_text(text, font, color, x, y):
        img = font.render(text, True, color)
        rect = img.get_rect(center=(x, y)) # center at (x, y)
        screen.blit(img, rect)

    balls = []
    bird = Bird(y=100)
    score = 0
    lives = 3

    # game loop
    running = True
    while running:
        screen.blit(pitch_img, (0, 0))

        # gameplay
        if not game_started: # added a short explanation and press enter to start game
            draw_text('Balls will fall from the sky', font_small, 'black', 400,160)
            draw_text('CLICK on the balls and avoid the birds', font_small, 'black', 400,200)
            draw_text('Press ENTER to start', font_small, 'black', 400,240)
        elif not paused and not game_over:
            current_time = pygame.time.get_ticks()
            if current_time - last_ball_time > 1000:
                # dropping another ball
                x = random.randint(50, 750)
                speed = random.randint(3, 7)
                balls.append(Ball(x,speed))
                last_ball_time = current_time

            # Update and draw balls
            for ball in balls[:]:
                ball.update(screen)
                # checking if ball hit the ground
                if ball.rect.bottom > 384:
                    balls.remove(ball)
                    lives -= 1

            # Update and draw bird
            bird.update(screen)

            # Draw score
            draw_text(f"Score: {score}", font_big, 'black', 100, 35)

            # Draw hearts
            for i in range(lives):
                screen.blit(heart_img, (470 + 75*i, 0))

            # Pause button
            if pause_button.draw(screen):
                paused = True

        # paused menu
        elif paused:
            draw_text("Paused", font_big, "black", 400, 170)
            if resume_button.draw(screen):
                paused = False
            if restart_button.draw(screen):
                return run_fielding_game(screen)
            if home_button.draw(screen):
                pygame.time.delay(200)                
                return 'menu'

        # game over screen
        elif game_over:
            draw_text("Game Over!", font_big, "red", 400, 100)
            draw_text(f"Final Score: {score}", font_big, "black", 400, 160)
            if restart_button.draw(screen):
                return run_fielding_game(screen)
            if home_button.draw(screen):
                pygame.time.delay(200)
                return 'menu'
            
        # Check for game over
        if lives <= 0 and not game_over:
            game_over = True


        # event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and not game_started:
                if event.key == pygame.K_RETURN:
                    game_started = True # start game when enter is pressed
                    last_ball_time = pygame.time.get_ticks()  # start timer

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not paused and not game_over:
                pos = pygame.mouse.get_pos()

                # Ball click check
                for ball in balls[:]:
                    if ball.rect.collidepoint(pos):
                        balls.remove(ball)
                        score += 1
                    

                # Bird click check
                if bird.rect.collidepoint(pos):
                    lives -= 1



        pygame.display.update()
        clock.tick(60)
