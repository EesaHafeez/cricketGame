import pygame
import random
import math
import button  # same button module as fielding_game.py

def run_batting_game(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arialblack", 30)
    font_small = pygame.font.SysFont("arialblack", 25)

    # Load assets
    pitch_img = pygame.image.load("images/pitch.png").convert()
    wickets_img = pygame.image.load("images/wickets.png").convert_alpha()
    batsman_img = pygame.image.load("images/batsman.png").convert_alpha()
    bat_img = pygame.image.load("images/bat.png").convert_alpha()

    # UI images
    home_img = pygame.image.load("images/home.png")
    resume_img = pygame.image.load("images/resume.png")
    restart_img = pygame.image.load("images/restart.png")
    pause_img = pygame.image.load("images/pause.png")

    # Buttons
    home_button = button.Button(305, 280, home_img, 1)
    resume_button = button.Button(400, 280, resume_img, 1)
    restart_button = button.Button(495, 280, restart_img, 1)
    pause_button = button.Button(750, 50, pause_img, 0.8)

    # Game variables
    score = 0
    numbers = [6, 5, 4, 3, 2, 1]
    numbers_x = 750
    numbers_y_start = 110
    number_spacing = 50

    # Game state
    game_started = False
    paused = False
    game_over = False
    ready_delay = False
    delay_start_time = 0

    # Wickets
    wickets_x = 100
    bottom_of_wickets = 430
    top_of_wickets = bottom_of_wickets - wickets_img.get_height()

    # Bat setup
    bat_angle = 0
    swing_speed = 8
    max_swing = 150

    def reset_ball():
        ball_speed = random.uniform(0.04, 0.08)
        ball_start_y = random.randint(130, 300)
        ball_bounce_x = random.randint(350, 550)
        ball_x = 700
        ball_y = ball_start_y
        ball_start_x = 700
        ball_bounce_y = 410
        ball_end_x = wickets_x
        ball_end_y = 325
        ball_phase = 1
        ball_hit = False
        ball_target_number = 0
        t = 0
        bat_swinged = False
        swinging = False
        return (ball_x, ball_y, ball_start_x, ball_start_y, ball_bounce_x, ball_bounce_y,
                ball_end_x, ball_end_y, ball_phase, ball_hit, ball_target_number, t,
                bat_swinged, swinging, ball_speed)

    pygame.time.delay(200)
    (ball_x, ball_y, ball_start_x, ball_start_y, ball_bounce_x, ball_bounce_y,
     ball_end_x, ball_end_y, ball_phase, ball_hit, ball_target_number, t,
     bat_swinged, swinging, ball_speed) = reset_ball()

    # Utility functions
    def draw_text(text, font, color, x, y):
        img = font.render(text, True, color)
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)

    def rotate_surface(surface, angle, pivot):
        rotated_image = pygame.transform.rotate(surface, angle)
        rect = rotated_image.get_rect(center=pivot)
        return rotated_image, rect

    bat_pivot = pygame.math.Vector2(168, 298)

    running = True
    while running:
        # Always draw pitch + wickets
        screen.blit(pitch_img, (0, 0))
        screen.blit(wickets_img, (63, top_of_wickets))

        # --- START SCREEN ---
        if not game_started and not ready_delay:
            draw_text("Get Ready to Bat!", font, "black", 400, 140)
            draw_text("Press SPACE at the right time to hit the ball", font_small, "black", 400, 180)
            draw_text("Score runs based on timing — aim for 6!", font_small, "black", 400, 215)
            draw_text("Press ENTER to start", font, "black", 400, 270)

        # --- READY DELAY (show full scene) ---
        elif ready_delay:
            # Draw game setup scene (frozen)
            screen.blit(batsman_img, (175, 250))

            for i in range(len(numbers)):
                draw_text(str(numbers[i]), font, 'black', numbers_x, numbers_y_start + i * number_spacing)

            rotated_bat, bat_rect = rotate_surface(bat_img, bat_angle, bat_pivot)
            screen.blit(rotated_bat, bat_rect)
            draw_text(f"Score: {score}", font, 'black', 100, 30)
            pause_button.draw(screen)


            # After 1.5s, start the game
            if pygame.time.get_ticks() - delay_start_time > 1500:
                ready_delay = False
                game_started = True

        # --- MAIN GAMEPLAY ---
        elif not paused and not game_over:
            screen.blit(batsman_img, (175, 250))

            for i in range(len(numbers)):
                draw_text(str(numbers[i]), font, 'black', numbers_x, numbers_y_start + i * number_spacing)

            # Ball logic
            if not ball_hit:
                if ball_phase == 1:
                    t += ball_speed
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
                    t += ball_speed
                    dx = ball_end_x - ball_start_x
                    dy = ball_end_y - ball_start_y
                    ball_x = ball_start_x + dx * t
                    ball_y = ball_start_y + dy * t
                    if t >= 1:
                        game_over = True

                # Collision detection
                rotated_bat, bat_rect = rotate_surface(bat_img, bat_angle, bat_pivot)
                ball_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
                pygame.draw.circle(ball_surface, (255, 0, 0), (10, 10), 10)
                ball_mask = pygame.mask.from_surface(ball_surface)
                bat_mask = pygame.mask.from_surface(rotated_bat)
                offset = (int(ball_x - bat_rect.x), int(ball_y - bat_rect.y))

                if swinging and not bat_swinged:
                    if bat_mask.overlap(ball_mask, offset):
                        ball_hit = True
                        bat_swinged = True

                        # Hit grading logic
                        ideal_angle = 55
                        angle_diff = abs(bat_angle - ideal_angle)
                        ideal_distance = 100
                        bat_distance = math.hypot(ball_x - bat_pivot.x, ball_y - bat_pivot.y)
                        distance_diff = abs(bat_distance - ideal_distance)
                        timing_score = (angle_diff * 0.75) + (distance_diff * 0.25)

                        if timing_score < 12:
                            ball_target_number = 6
                        elif timing_score < 22:
                            ball_target_number = 5
                        elif timing_score < 35:
                            ball_target_number = 4
                        elif timing_score < 50:
                            ball_target_number = 3
                        elif timing_score < 70:
                            ball_target_number = 2
                        else:
                            ball_target_number = 1

            else:
                # Ball reflection animation
                if ball_target_number > 0:
                    idx = numbers.index(ball_target_number)
                    target_x = numbers_x
                    target_y = numbers_y_start + idx * number_spacing
                    dx = target_x - ball_x
                    dy = target_y - ball_y
                    dist = math.hypot(dx, dy)
                    if dist < 5:
                        score += ball_target_number
                        pygame.time.delay(200)
                        (ball_x, ball_y, ball_start_x, ball_start_y, ball_bounce_x, ball_bounce_y,
                         ball_end_x, ball_end_y, ball_phase, ball_hit, ball_target_number, t,
                         bat_swinged, swinging, ball_speed) = reset_ball()
                    else:
                        ball_x += dx / dist * 10
                        ball_y += dy / dist * 10
                else:
                    game_over = True

            # Draw ball
            pygame.draw.circle(screen, 'red', (int(ball_x), int(ball_y)), 10)

            # Bat motion
            if swinging and not bat_swinged:
                if bat_angle < max_swing:
                    bat_angle += swing_speed
                else:
                    swinging = False
            else:
                if bat_angle > 0:
                    bat_angle -= swing_speed

            # Draw bat
            rotated_bat, bat_rect = rotate_surface(bat_img, bat_angle, bat_pivot)
            screen.blit(rotated_bat, bat_rect)

            # Draw score
            draw_text(f"Score: {score}", font, 'black', 100, 30)

            # Pause button
            if pause_button.draw(screen):
                paused = True

        # --- PAUSE MENU ---
        elif paused:
            draw_text("Paused", font, "black", 400, 170)
            if resume_button.draw(screen):
                paused = False
            if restart_button.draw(screen):
                return run_batting_game(screen)
            if home_button.draw(screen):
                pygame.time.delay(200)
                return 'menu'

        # --- GAME OVER SCREEN ---
        elif game_over:
            draw_text("Game Over!", font, "red", 400, 130)
            draw_text(f"Final Score: {score}", font, "black", 400, 190)
            if restart_button.draw(screen):
                return run_batting_game(screen)
            if home_button.draw(screen):
                pygame.time.delay(200)
                return 'menu'

        # --- EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if not game_started and not ready_delay:
                    if event.key == pygame.K_RETURN:
                        ready_delay = True
                        delay_start_time = pygame.time.get_ticks()
                elif not paused and not game_over and game_started:
                    if event.key == pygame.K_SPACE and not bat_swinged and not swinging:
                        swinging = True

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
