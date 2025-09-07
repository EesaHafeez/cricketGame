# bowling.py
import pygame
import math
import random
import button

# Load assets
pitch_img = pygame.image.load("images/pitch.png")
wickets_img = pygame.image.load("images/wickets.png")
home_img = pygame.image.load("images/home.png")
restart_img = pygame.image.load("images/restart.png")
pause_img = pygame.image.load("images/pause.png")
resume_img = pygame.image.load("images/resume.png")

# Creating button instances
home_button = button.Button(305, 280, home_img, 1)
resume_button = button.Button(400, 280, resume_img, 1)
restart_button = button.Button(495, 280, restart_img, 1)
pause_button = button.Button(750, 50, pause_img, 0.8)


def run_bowling_game(screen): # subroutine to run bowling mode
    clock = pygame.time.Clock()

    #game variables for stage 1
    disc_x = 150 # disc starting pos
    disc_speed = 50 # initial disc speed
    disc_frozen = False
    stored_x_position = None

    # game variables for stage 2
    click_count = 0
    stage2_start_time = None
    stage2_duration = 10  # seconds

    # game variables for stage 3
    ball_pos = None
    bounce_done = False
    ball_hit_wicket = False

    # game state varaiables
    stage = 1
    paused = False
    game_over = False

    # Wickets
    wickets_x = 100
    bottom_of_wickets = 430
    top_of_wickets = bottom_of_wickets - wickets_img.get_height()


    # Game stats
    balls_bowled = 0
    total_clicks = 0
    wickets_hit_count = 0

    # Fonts
    font_big = pygame.font.SysFont("arialblack", 40)
    font_small = pygame.font.SysFont("arialblack", 30)

    # subroutine to display text
    def draw_text(text, font, color, x, y):
        img = font.render(text, True, color)
        rect = img.get_rect(center=(x, y)) # center at (x, y)
        screen.blit(img, rect)

    running = True
    while running:
        screen.blit(pitch_img, (0, 0)) # displaying pitch
        screen.blit(wickets_img, (63, top_of_wickets)) # displaying wickets

        if not paused and not game_over:
            # Draw top-right pause button
            if pause_button.draw(screen):
                paused = True
            # stage 1 - set bounce
            if stage == 1:
                if not disc_frozen:
                    draw_text("Press SPACE to stop the disc to set bounce:", font_small, 'black', 400, 130)
                    disc_x += disc_speed # make the disc move along
                    if disc_x >= 760: # if disc hits right boundary
                        disc_x = 760
                        disc_speed = -random.randint(40,60) # reverse the disc direction with random speeds between 15 and 20
                    elif disc_x <= 155: # if disc hits left boundary
                        disc_x = 155
                        disc_speed = random.randint(40,60) # reverse the disc direction with random speeds between 15 and 2
                    pygame.draw.circle(screen, "white", (disc_x, 400), 5) # drawing disc
                else: # if disc frozen
                    draw_text("Bounce position stored ", font_small, 'black', 400, 110)
                    draw_text("Press ENTER to continue:", font_small, 'black', 400, 150)
                    pygame.draw.circle(screen, "white", (stored_x_position, 400), 5) # diplaying position of stored disc

            # stage 2 - setting speed
            elif stage == 2:
                if stage2_start_time is not None: 
                    elapsed = (pygame.time.get_ticks() - stage2_start_time) // 1000 # time passed
                    time_left = max(0, stage2_duration - elapsed) 
                    draw_text("CLICK as many times as you can: ", font_small, 'black', 400, 120)
                    draw_text(f"Clicks: {click_count}", font_big, 'blue', 400, 170) # displaying clicks
                    draw_text(f"Time left: {time_left}", font_big, 'red', 400, 210) # displaying time left
                    if elapsed >= stage2_duration:
                        ball_pos = [800, 50] # setting starting ball postion for stage 3
                        stage = 3
                else: # time hasn't started
                    draw_text("CLICK as many times as you can in 10 seconds", font_small, 'black', 400, 110)
                    draw_text("Number of clicks will determine your speed", font_small, 'black', 400, 150)

            # stage 3 - ball delivery
            elif stage == 3:
                base_speed = 10
                ball_speed = base_speed + click_count * 0.2 # speed proportional to clicks in stage 2

                if not bounce_done: # before bounce
                    dx = stored_x_position - ball_pos[0] 
                    dy = 400 - ball_pos[1]
                    dist = math.hypot(dx, dy)
                    if dist <= ball_speed: # jumps to bounce pos if it can reach it in this frame
                        ball_pos[0] = stored_x_position
                        ball_pos[1] = 400
                        bounce_done = True
                    else: # if not, increment ball position
                        ball_pos[0] += dx / dist * ball_speed
                        ball_pos[1] += dy / dist * ball_speed
                else: # after bounce
                    end_x = wickets_x
                    min_bounce = 155
                    max_bounce = 760

                    # ratio of ball bounce relative to wickets
                    ratio = (stored_x_position - min_bounce) / (max_bounce - min_bounce)
                    # using bounce ratio to calculate where the ball should end
                    end_y = bottom_of_wickets - int((bottom_of_wickets) * ratio)

                    dx = end_x - ball_pos[0]
                    dy = end_y - ball_pos[1]
                    dist = math.hypot(dx, dy)
                    if dist <= ball_speed: # jumps to end pos if it can reach it in this frame
                        ball_pos[0] = end_x
                        ball_pos[1] = end_y
                        game_over = True 
                        balls_bowled += 1 # increments balls bowled
                        total_clicks += click_count # updates total clicks
                        if end_y + 10 >= top_of_wickets: # if ball hits the wickets
                            ball_hit_wicket = True
                            wickets_hit_count += 1
                        else: # if ball misses wickets
                            ball_hit_wicket = False
                    else: # if can't reach in frame, update ball position
                        ball_pos[0] += dx / dist * ball_speed
                        ball_pos[1] += dy / dist * ball_speed

                pygame.draw.circle(screen, 'white', (int(ball_pos[0]), int(ball_pos[1])), 10) # drawing the ball


        # stage 4 - game over screen
        elif game_over:
            pygame.draw.circle(screen, 'white', (int(ball_pos[0]), int(ball_pos[1])), 10) # draw final ball pos
            avg_speed = total_clicks / balls_bowled # calculating average speed
            avg_accuracy = (wickets_hit_count / balls_bowled * 100) # calculating average accuracy

            draw_text("Ball bowled!", font_big, 'red', 400, 50)
            draw_text(f"Wickets hit: {'YES' if ball_hit_wicket else 'NO'}", font_big, 'blue', 400, 90)
            draw_text(f"Balls bowled: {balls_bowled}", font_small, 'black', 400, 150)
            draw_text(f"Average speed: {avg_speed:.1f}", font_small, 'black', 400, 180)
            draw_text(f"Average accuracy: {avg_accuracy:.1f}%", font_small, 'black', 400, 210)

            # Buttons
            if restart_button.draw(screen): # if game is restarted
                # Reset all game variables
                game_over = False
                stage = 1
                disc_x = 150
                disc_frozen = False
                stored_x_position = None
                click_count = 0
                stage2_start_time = None
                ball_pos = None
                bounce_done = False
                ball_hit_wicket = False
                balls_bowled = 0
                total_clicks = 0
                wickets_hit_count = 0
            elif home_button.draw(screen): # if home button pressed
                pygame.time.delay(200)
                return 'menu'
            elif resume_button.draw(screen): # if resume button pressed (bowl another ball)
                # resetting a few game variables
                game_over = False
                stage = 1
                disc_x = 150
                disc_frozen = False
                stored_x_position = None
                click_count = 0
                stage2_start_time = None
                ball_pos = None
                bounce_done = False
                ball_hit_wicket = False
                pygame.time.delay(200)  # avoid immediate click

        # pause menu
        if paused: # if paused
            draw_text("Paused", font_big, "black", 400, 170)
            if resume_button.draw(screen): # if resume button pressed
                pygame.time.delay(150)
                paused = False
            elif restart_button.draw(screen): # if restart button pressed
                pygame.time.delay(150)
                # Reset entire game
                stage = 1
                disc_x = 150
                disc_frozen = False
                stored_x_position = None
                click_count = 0
                stage2_start_time = None
                ball_pos = None
                bounce_done = False
                ball_hit_wicket = False
                balls_bowled = 0
                total_clicks = 0
                wickets_hit_count = 0
                paused = False
            elif home_button.draw(screen): # if home button pressed
                pygame.time.delay(200)
                return  'menu'

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # close the window if red x is clicked
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN: # if a key is pressed
                # freeze disc and store position when spacebar is pressed
                if stage == 1 and event.key == pygame.K_SPACE and not disc_frozen:
                    disc_frozen = True
                    stored_x_position = disc_x
                # go to stage 2 if entered pressed to continue
                elif stage == 1 and event.key == pygame.K_RETURN and disc_frozen:
                    stage = 2
            # if mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if stage 2 and timer not started, start timer. Also increment clicks
                if stage == 2:
                    if stage2_start_time is None:
                        stage2_start_time = pygame.time.get_ticks()
                    click_count += 1

        pygame.display.update()
        clock.tick(60)
