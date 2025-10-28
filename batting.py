import pygame
import random
import math

# Load images
pitch_img = pygame.image.load("images/pitch.png")
wickets_img = pygame.image.load("images/wickets.png")

def run_batting_game(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arialblack", 30)

    # Game variables
    score = 0
    numbers = [6, 5, 4, 3, 2, 1]
    numbers_x = 750
    numbers_y_start = 50
    number_spacing = 50

    # Wickets
    wickets_x = 100
    bottom_of_wickets = 430
    top_of_wickets = bottom_of_wickets - wickets_img.get_height()
    middle_wicket_y = (top_of_wickets + bottom_of_wickets) // 2

    # Reset function for ball
    def reset_ball():
        ball_start_y = random.randint(70, 120)
        ball_bounce_x = random.randint(350, 550)
        ball_x = 700
        ball_y = ball_start_y
        ball_start_x = 700
        ball_bounce_y = 370
        ball_end_x = wickets_x + 30
        ball_end_y = middle_wicket_y
        ball_phase = 1
        ball_hit = False
        ball_target_number = 0
        t = 0
        bat_swinged = False
        swinging = False
        return (ball_x, ball_y, ball_start_x, ball_start_y, ball_bounce_x, ball_bounce_y,
                ball_end_x, ball_end_y, ball_phase, ball_hit, ball_target_number, t,
                bat_swinged, swinging)

    (ball_x, ball_y, ball_start_x, ball_start_y, ball_bounce_x, ball_bounce_y,
     ball_end_x, ball_end_y, ball_phase, ball_hit, ball_target_number, t,
     bat_swinged, swinging) = reset_ball()

    # Bat setup (pivot from top)
    bat_x = 130
    bat_y = 330  # lower for realistic height
    bat_width = 15
    bat_height = 90
    bat_angle = -45
    swing_speed = 8
    max_swing = 45
    ideal_angle = 0
    timing_window = 15  # how close to ideal angle to hit

    running = True
    while running:
        screen.blit(pitch_img, (0, 0))
        screen.blit(wickets_img, (63, top_of_wickets))

        def draw_text(text, font, color, x, y):
            img = font.render(text, True, color)
            rect = img.get_rect(center=(x, y))
            screen.blit(img, rect)

        # Draw numbers
        for i in range(len(numbers)):
            draw_text(str(numbers[i]), font, 'black', numbers_x, numbers_y_start + i * number_spacing)

        # --- Ball movement ---
        if not ball_hit:
            if ball_phase == 1:
                t += 0.02
                dx = ball_bounce_x - ball_start_x
                dy = ball_bounce_y - ball_start_y
                h = 120
                ball_x = ball_start_x + dx * t
                ball_y = ball_start_y + dy * t - 4 * h * t * (1 - t)
                if t >= 1:
                    ball_phase = 2
                    t = 0
                    ball_start_x = ball_bounce_x
                    ball_start_y = ball_bounce_y
            else:
                t += 0.02
                dx = ball_end_x - ball_start_x
                dy = ball_end_y - ball_start_y
                ball_x = ball_start_x + dx * t
                ball_y = ball_start_y + dy * t
                if t >= 1:
                    ball_hit = True
                    ball_target_number = 0  # missed

            # --- Collision only if swinging and precise timing ---
            if swinging and not bat_swinged:
                bat_surface = pygame.Surface((bat_width, bat_height), pygame.SRCALPHA)
                bat_surface.fill('black')
                rotated_bat = pygame.transform.rotate(bat_surface, bat_angle)
                bat_rect = rotated_bat.get_rect(topleft=(bat_x, bat_y))

                if bat_rect.collidepoint(ball_x, ball_y) and abs(bat_angle - ideal_angle) <= timing_window:
                    # Perfect timing: guaranteed reflection
                    ball_hit = True
                    bat_swinged = True
                    ball_target_number = random.choice([6, 5, 4, 3])  # guaranteed hit values

        else:
            # Ball hit → reflect toward numbers
            if ball_target_number > 0:
                idx = numbers.index(ball_target_number)
                target_x = numbers_x
                target_y = numbers_y_start + idx * number_spacing
                dx = target_x - ball_x
                dy = target_y - ball_y
                dist = math.hypot(dx, dy)
                if dist < 5:
                    score += ball_target_number
                    (ball_x, ball_y, ball_start_x, ball_start_y, ball_bounce_x, ball_bounce_y,
                     ball_end_x, ball_end_y, ball_phase, ball_hit, ball_target_number, t,
                     bat_swinged, swinging) = reset_ball()
                else:
                    ball_x += dx / dist * 10
                    ball_y += dy / dist * 10
            else:
                # Missed – goes into wickets and reset
                (ball_x, ball_y, ball_start_x, ball_start_y, ball_bounce_x, ball_bounce_y,
                 ball_end_x, ball_end_y, ball_phase, ball_hit, ball_target_number, t,
                 bat_swinged, swinging) = reset_ball()

        # Draw ball
        pygame.draw.circle(screen, 'red', (int(ball_x), int(ball_y)), 10)

        # --- Swing bat upward (pivot from top-left) ---
        if swinging and not bat_swinged:
            if bat_angle < max_swing:
                bat_angle += swing_speed
            else:
                swinging = False
        else:
            if bat_angle > -45:
                bat_angle -= swing_speed

        # Draw bat
        bat_surface = pygame.Surface((bat_width, bat_height), pygame.SRCALPHA)
        bat_surface.fill('black')
        rotated_bat = pygame.transform.rotate(bat_surface, bat_angle)
        bat_rect = rotated_bat.get_rect(topleft=(bat_x, bat_y))
        screen.blit(rotated_bat, bat_rect)

        draw_text(f"Score: {score}", font, 'black', 100, 30)

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not bat_swinged and not swinging:
                    swinging = True  # one swing per ball

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
