import pygame
import random
import sys


def start_game():
    pygame.init()

    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ping Pong")

    PLATFORM_WIDTH = 20
    PLATFORM_HEIGHT = 140
    PLATFORM_SPEED = 5
    BALL_SIZE = 30
    MAX_BALL_SPEED = 15

    font_obj = pygame.font.SysFont("Comic Sans MS", 50)

    player1 = pygame.Rect(50, SCREEN_HEIGHT // 2 - PLATFORM_HEIGHT // 2, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    player2 = pygame.Rect(SCREEN_WIDTH - 50 - PLATFORM_WIDTH, SCREEN_HEIGHT // 2 - PLATFORM_HEIGHT // 2, PLATFORM_WIDTH,
                          PLATFORM_HEIGHT)
    ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BALL_SIZE)

    ball_sx = 0
    ball_sy = 0
    ball_angle = 0
    score1 = 0
    score2 = 0

    plat_img = pygame.transform.scale(pygame.image.load("platform.jpg").convert_alpha(),
                                      (PLATFORM_WIDTH, PLATFORM_HEIGHT))
    ball_original = pygame.transform.scale(pygame.image.load("ball.png").convert_alpha(), (BALL_SIZE, BALL_SIZE))
    bg = pygame.image.load("bg.png").convert_alpha()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def reset_ball():
        nonlocal ball_sx, ball_sy
        ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        ball_sx = random.choice([-5, 5])
        ball_sy = random.uniform(-2, 2)

    reset_ball()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= PLATFORM_SPEED
        if keys[pygame.K_s] and player1.bottom < SCREEN_HEIGHT:
            player1.y += PLATFORM_SPEED
        if keys[keys[pygame.K_UP]] and player2.top > 0:
            player2.y -= PLATFORM_SPEED
        if keys[pygame.K_DOWN] and player2.bottom < SCREEN_HEIGHT:
            player2.y += PLATFORM_SPEED

        if keys[pygame.K_UP] and player2.top > 0:
            player2.y -= PLATFORM_SPEED
        if keys[pygame.K_DOWN] and player2.bottom < SCREEN_HEIGHT:
            player2.y += PLATFORM_SPEED

        ball.x += ball_sx
        ball.y += ball_sy

        ball_angle -= ball_sx * 2

        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_sy *= -1

        if ball.colliderect(player1):
            if abs(ball_sx) < MAX_BALL_SPEED:
                ball_sx = abs(ball_sx) * 1.05
            else:
                ball_sx = abs(ball_sx)

            relative_intersect_y = (player1.centery - ball.centery) / (PLATFORM_HEIGHT / 2)
            ball_sy = -relative_intersect_y * abs(ball_sx)

            ball.left = player1.right

        if ball.colliderect(player2):
            if abs(ball_sx) < MAX_BALL_SPEED:
                ball_sx = -abs(ball_sx) * 1.05
            else:
                ball_sx = -abs(ball_sx)

            relative_intersect_y = (player2.centery - ball.centery) / (PLATFORM_HEIGHT / 2)
            ball_sy = -relative_intersect_y * abs(ball_sx)

            ball.right = player2.left

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