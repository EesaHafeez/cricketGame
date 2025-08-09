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
blueBox_img = pygame.image.load("images/blueBox.png")

# Creating button instances
home_button = button.Button(250, 250, home_img, 1)
resume_button = button.Button(375, 250, resume_img, 1)
restart_button = button.Button(475, 250, restart_img, 1)
pause_button = button.Button(720, 20, pause_img, 0.8)

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

    # Game state variables
    game_over = False
    paused = False

    # Font
    font = pygame.font.SysFont("arialblack", 40)

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

        # -------------------- GAMEPLAY --------------------
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
                screen.blit(heart_img, (470 + 75*i, 0))

            # Pause button
            if pause_button.draw(screen):
                paused = True

        # -------------------- PAUSE MENU --------------------
        elif paused:
            draw_text("Paused", font, "black", 320, 130)
            if resume_button.draw(screen):
                paused = False
            if restart_button.draw(screen):
                return run_fielding_game(screen)
            if home_button.draw(screen):
                pygame.time.delay(200)                
                return

        # -------------------- GAME OVER SCREEN --------------------
        elif game_over:
            draw_text("Game Over!", font, "red", 275, 100)
            draw_text(f"Final Score: {score}", font, "black", 250, 160)
            if restart_button.draw(screen):
                return run_fielding_game(screen)
            if home_button.draw(screen):
                pygame.time.delay(200)
                return

        # -------------------- EVENT HANDLING --------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not paused and not game_over:
                pos = pygame.mouse.get_pos()

                # Ball click check
                for ball in balls[:]:
                    if ball.rect.collidepoint(pos):
                        balls.remove(ball)
                        score += 1
                        break

                # Bird click check
                if bird.rect.collidepoint(pos):
                    lives -= 1

        # Check for game over
        if lives <= 0 and not game_over:
            game_over = True

        pygame.display.update()
        clock.tick(60)
