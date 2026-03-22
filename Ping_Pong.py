import pygame
import random
import sys
import random

def start_game():
    pygame.init()

    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ping Pong")

    PLATFORM_WIDTH = 20
    PLATFORM_HEIGHT = 160
    PLATFORM_SPEED = 5
    BALL_SIZE = 30
    MAX_BALL_SPEED = 50

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
    bg = pygame.image.load("assets/bg.png").convert_alpha()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    ball_bounce_sound = pygame.mixer.Sound("assets/BounceYoFrankie.flac")
    ball_bounce_sound2 = pygame.mixer.Sound("assets/qubodup-cfork-ccby3-jump.ogg")

    def reset_ball():
        nonlocal ball_sx, ball_sy, turn
        turn = 0
        ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        ball_sx = random.choice([-10, 10])
        ball_sy = random.uniform(-4, 4)
#opengame.org
    reset_ball()
    clock = pygame.time.Clock()
    turn = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        dynamic_speed = abs(ball_sx) * 1.3

        if turn != 2:
            if abs(player1.centery - ball.centery) > dynamic_speed:
                if player1.centery > ball.centery:
                    player1.y -= dynamic_speed
                else:
                    player1.y += dynamic_speed
            else:
                player1.centery = ball.centery

        if turn != 1:
            if abs(player2.centery - ball.centery) > dynamic_speed:
                if player2.centery > ball.centery:
                    player2.y -= dynamic_speed
                else:
                    player2.y += dynamic_speed
            else:
                player2.centery = ball.centery

        player1.y = max(0, min(SCREEN_HEIGHT - PLATFORM_HEIGHT, player1.y))
        player2.y = max(0, min(SCREEN_HEIGHT - PLATFORM_HEIGHT, player2.y))

        """
        if keys[pygame.K_UP] and player2.top > 0:
            player2.y -= PLATFORM_SPEED
        if keys[pygame.K_DOWN] and player2.bottom < SCREEN_HEIGHT:
            player2.y += PLATFORM_SPEED
        """
        ball.x += ball_sx
        ball.y += ball_sy

        ball_angle -= ball_sx * 2

        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_sy *= -1
            ball_bounce_sound.play()

        if ball.colliderect(player1):
            if abs(ball_sx) < MAX_BALL_SPEED:
                ball_sx = abs(ball_sx) * 1.05
            else:
                ball_sx = abs(ball_sx)

            relative_intersect_y = (player1.centery - (ball.centery+5)) / (PLATFORM_HEIGHT / 2)
            ball_sy = -relative_intersect_y * abs(ball_sx)

            ball.left = player1.right
            ball_bounce_sound.play()
            turn = 2
        if ball.colliderect(player2):
            if abs(ball_sx) < MAX_BALL_SPEED:
                ball_sx = -abs(ball_sx) * 1.05
            else:
                ball_sx = -abs(ball_sx)

            relative_intersect_y = (player2.centery - (ball.centery+5)) / (PLATFORM_HEIGHT / 2)
            ball_sy = -relative_intersect_y * abs(ball_sx)

            ball.right = player2.left
            ball_bounce_sound.play()
            turn = 1
        if ball.left < 0:
            score2 += 1
            reset_ball()
        if ball.right > SCREEN_WIDTH:
            score1 += 1
            reset_ball()

        screen.blit(bg, (0, 0))

        pygame.draw.line(screen, (0, 0, 0), (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 2)

        rotated_ball = pygame.transform.rotate(ball_original, ball_angle)
        new_rect = rotated_ball.get_rect(center=ball.center)
        screen.blit(rotated_ball, new_rect)

        screen.blit(plat_img, player1)
        screen.blit(plat_img, player2)

        score_text = font_obj.render(f"{score1}   {score2}", True, (0, 0, 0))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    start_game()