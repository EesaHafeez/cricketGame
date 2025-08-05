# fielding_game.py

import pygame
import random

# Load assets (make sure these files exist or use placeholders)
pitch_img = pygame.image.load("pitch.png")
ball_img = pygame.image.load("ball.png")
bird_img = pygame.image.load("bird.png")
heart_img = pygame.image.load("heart.png")

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
            self.rect.y = random.randint(50, 150)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def run_fielding_game(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arialblack", 30)

    balls = []
    bird = Bird(y=100)
    score = 0
    lives = MAX_LIVES
    last_ball_time = pygame.time.get_ticks()

    running = True
    while running:
        screen.blit(pitch_img, (0, 0))

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
            if ball.rect.top > 450:
                balls.remove(ball)
                lives -= 1

        # Update and draw bird
        bird.update()
        bird.draw(screen)

        # Draw score
        score_text = font.render(f"Score: {score}", True, "black")
        screen.blit(score_text, (10, 10))

        # Draw hearts
        for i in range(lives):
            screen.blit(heart_img, (700 + i * 30, 10))

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

        if lives <= 0:
            game_over_text = font.render("Game Over!", True, "red")
            screen.blit(game_over_text, (300, 200))
            pygame.display.update()
            pygame.time.delay(2000)
            running = False

        pygame.display.update()
        clock.tick(60)
