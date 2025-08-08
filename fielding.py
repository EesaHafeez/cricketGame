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

# creating button instances
home_button = button.Button(65, 87, home_img, 0.95)
resume_button = button.Button(409, 87, resume_img, 0.95)
restart_button = button.Button(65, 272, restart_img, 0.95)
pause_button = button.Button(700, 60, pause_img, 0.3)


# Constants
BALL_SPAWN_TIME = 1000  # milliseconds
BIRD_SPEED = 3
MAX_LIVES = 3


class Ball:
    def __init__(self, x, y, speed):
        self.image = ball_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Bird:
    def __init__(self, y):
        self.image = bird_img
        self.rect = self.image.get_rect(midleft=(0, y))
        self.speed = BIRD_SPEED

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > 800:  # reset bird
            self.rect.right = 0
            self.rect.y = random.randint(50, 250)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def run_fielding_game(screen):
    clock = pygame.time.Clock()

    # game variables
    game_over = False
    paused = False

    # define font
    font = pygame.font.SysFont("arialblack", 40)

    # subroutine to draw text on screen
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    balls = []
    bird = Bird(y=100)
    score = 0
    lives = MAX_LIVES
    last_ball_time = pygame.time.get_ticks()

    running = True
    while running:
        screen.blit(pitch_img, (0, 0))
        if not paused and not game_over:
            current_time = pygame.time.get_ticks()
            if current_time - last_ball_time > BALL_SPAWN_TIME:
                x = random.randint(50, 750)
                speed = random.randint(3, 7)
                balls.append(Ball(x, 0, speed))
                last_ball_time = current_time

            # Update and draw balls
            for ball in balls[:]:
                ball.update()
                ball.draw(screen)
                if ball.rect.bottom > 384:
                    balls.remove(ball)
                    lives -= 1

            # Update and draw bird
            bird.update()
            bird.draw(screen)

            # Draw score
            draw_text(f"Score: {score}", font, 'black', 10, 10)

            # Draw hearts
            for i in range(lives):
                screen.blit(heart_img, (550 + 75*i, 0))
            if pause_button.draw(screen):
                paused = True

        elif paused:
            if restart_button.draw(screen):
                return run_fielding_game(screen)
            elif home_button.draw(screen):
                return
            elif resume_button.draw(screen):
                paused = False

            elif game_over:
                draw_text("Game Over!", font, "red", 300, 100)
                draw_text(f"Final Score: {score}", font, "black", 280, 160)
                if restart_button.draw(screen):
                    return run_fielding_game(screen)
                if home_button.draw(screen):
                    return

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked_ball = False

                for ball in balls[:]:
                    if ball.rect.collidepoint(pos):
                        balls.remove(ball)
                        score += 1
                        clicked_ball = True
                        break

                if bird.rect.collidepoint(pos):
                    lives -= 1

        if lives <= 0 and not game_over:
            game_over = True


        pygame.display.update()
        clock.tick(60)
