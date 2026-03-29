import pygame
import random
import sys


def start_game(difficulty_name="легкий"):
    pygame.init()

    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"Ping Pong - {difficulty_name}")

    if difficulty_name == "легкий":
        BOT_ERROR_MARGIN = 70
        BOT_REACTION_SPEED = 0.6
        MAX_BALL_SPEED = 15
    elif difficulty_name == "середній":
        BOT_ERROR_MARGIN = 30
        BOT_REACTION_SPEED = 0.85
        MAX_BALL_SPEED = 25
    else:  # важкий
        BOT_ERROR_MARGIN = 5
        BOT_REACTION_SPEED = 1.1
        MAX_BALL_SPEED = 40

    PLATFORM_WIDTH = 20
    PLATFORM_HEIGHT = 160
    BALL_SIZE = 30
    PLAYER_SPEED = 7

    font_obj = pygame.font.SysFont("Comic Sans MS", 50)

    player1 = pygame.Rect(50, SCREEN_HEIGHT // 2 - PLATFORM_HEIGHT // 2, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    player2 = pygame.Rect(SCREEN_WIDTH - 50 - PLATFORM_WIDTH, SCREEN_HEIGHT // 2 - PLATFORM_HEIGHT // 2, PLATFORM_WIDTH,
                          PLATFORM_HEIGHT)
    ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BALL_SIZE)

    pygame.mixer.music.load("assets/Virus.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

    ball_sx = 0
    ball_sy = 0
    ball_angle = 0
    score1 = 0
    score2 = 0

    plat_img = pygame.transform.scale(pygame.image.load("assets/Platform.jpg").convert_alpha(),
                                      (PLATFORM_WIDTH, PLATFORM_HEIGHT))
    ball_original = pygame.transform.scale(pygame.image.load("assets/ball.png").convert_alpha(), (BALL_SIZE, BALL_SIZE))
    bg = pygame.transform.scale(pygame.image.load("assets/bg.png").convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))

    ball_bounce_sound = pygame.mixer.Sound("assets/BounceYoFrankie.flac")

    def reset_ball():
        nonlocal ball_sx, ball_sy
        ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        ball_sx = random.choice([-7, 7])
        ball_sy = random.uniform(-4, 4)

    reset_ball()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= PLAYER_SPEED
        if keys[pygame.K_s] and player1.bottom < SCREEN_HEIGHT:
            player1.y += PLAYER_SPEED

        target_y = ball.centery + (random.uniform(-BOT_ERROR_MARGIN, BOT_ERROR_MARGIN) if random.random() > 0.9 else 0)

        bot_speed = abs(ball_sx) * BOT_REACTION_SPEED

        if player2.centery < target_y:
            player2.y += bot_speed
        elif player2.centery > target_y:
            player2.y -= bot_speed

        player1.y = max(0, min(SCREEN_HEIGHT - PLATFORM_HEIGHT, player1.y))
        player2.y = max(0, min(SCREEN_HEIGHT - PLATFORM_HEIGHT, player2.y))

        # Движение мяча
        ball.x += ball_sx
        ball.y += ball_sy
        ball_angle -= ball_sx * 2

        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_sy *= -1
            ball_bounce_sound.play()

        if ball.colliderect(player1):
            ball_sx = min(abs(ball_sx) * 1.05, MAX_BALL_SPEED)
            relative_intersect_y = (player1.centery - ball.centery) / (PLATFORM_HEIGHT / 2)
            ball_sy = -relative_intersect_y * abs(ball_sx)
            ball.left = player1.right
            ball_bounce_sound.play()

        if ball.colliderect(player2):
            ball_sx = -min(abs(ball_sx) * 1.05, MAX_BALL_SPEED)
            relative_intersect_y = (player2.centery - ball.centery) / (PLATFORM_HEIGHT / 2)
            ball_sy = -relative_intersect_y * abs(ball_sx)
            ball.right = player2.left
            ball_bounce_sound.play()

        if ball.left < 0:
            score2 += 1
            reset_ball()
        if ball.right > SCREEN_WIDTH:
            score1 += 1
            reset_ball()

        screen.blit(bg, (0, 0))
        pygame.draw.line(screen, (0, 0, 0), (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 2)

        rotated_ball = pygame.transform.rotate(ball_original, ball_angle)
        screen.blit(rotated_ball, rotated_ball.get_rect(center=ball.center))
        screen.blit(plat_img, player1)
        screen.blit(plat_img, player2)

        score_text = font_obj.render(f"{score1}   {score2}", True, (0, 0, 0))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(60)