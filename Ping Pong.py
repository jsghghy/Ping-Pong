import pygame
import random

pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Ping Pong")
PLATFORM_WIDTH = 15
PLATFORM_HEIGHT = 120
PLATFORM_SPEED = 7

player1 = pygame.Rect(50, SCREEN_HEIGHT // 2 - PLATFORM_HEIGHT // 2, PLATFORM_WIDTH, PLATFORM_HEIGHT)
player2 = pygame.Rect(SCREEN_WIDTH - 50 - PLATFORM_WIDTH, SCREEN_HEIGHT // 2 - PLATFORM_HEIGHT // 2, PLATFORM_WIDTH, PLATFORM_HEIGHT)

clock = pygame.time.Clock()

BALL_SIZE = 30
ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BALL_SIZE)

score1 = 0
score2 = 0

font = pygame.font.SysFont("Comic Sans MS", 40)

ball_sy = 0
ball_sx = 0

def random_ball_position():
    global ball_sx, ball_sy
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_sx = random.choice([-4, 4])
    ball_sy = random.choice([-4, 4])

random_ball_position()
def draw_score():
    global score1, score2
    text = font.render(f"{score1} : {score2}", True, "White")
    screen.blit(text, (SCREEN_WIDTH // 2, 10))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill("Black")

    draw_score()

    key = pygame.key.get_pressed()

    if key[pygame.K_w] and player1.top > 0:
        player1.y -= PLATFORM_SPEED
    elif key[pygame.K_s] and player1.bottom < SCREEN_HEIGHT:
        player1.y += PLATFORM_SPEED

    if key[pygame.K_UP] and player2.top > 0:
        player2.y -= PLATFORM_SPEED
    elif key[pygame.K_DOWN] and player2.bottom < SCREEN_HEIGHT:
        player2.y += PLATFORM_SPEED

    ball.x += ball_sx
    ball.y += ball_sy

    if ball.bottom > SCREEN_HEIGHT or ball.top < 0:
        ball_sy *= -1

    if ball.colliderect(player1):
        ball_sx *= -1.05
    if ball.colliderect(player2):
        ball_sx *= -1.05
    if ball.x < 0:
        random_ball_position()
        score1 += 1
        draw_score()
    if ball.x > SCREEN_WIDTH:
        random_ball_position()
        score2 += 1
        draw_score()
    pygame.draw.rect(screen, "White", player2)
    pygame.draw.rect(screen, "White", player1)
    pygame.draw.ellipse(screen, "White", ball)

    pygame.display.update()
    clock.tick(60)
