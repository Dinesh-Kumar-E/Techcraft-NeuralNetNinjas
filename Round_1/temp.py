import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BRICK_WIDTH = 80
BRICK_HEIGHT = 20
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 10
BALL_RADIUS = 10
WHITE = (255, 255, 255)
BRICK_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Initialize the paddle
paddle = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)

# Initialize the ball
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x = 7
ball_speed_y = -7

# Create bricks
bricks = []
for row in range(5):
    for column in range(10):
        brick = pygame.Rect(column * BRICK_WIDTH, row * BRICK_HEIGHT + 50, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)

# Initialize game variables
score = 0
level = 1
lives = 3
game_over = False

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.x -= 10
    if keys[pygame.K_RIGHT]:
        paddle.x += 10

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collisions
    if ball.colliderect(paddle):
        ball_speed_y = -abs(ball_speed_y)

    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y = -ball_speed_y

    # Check for collisions with bricks
    for brick in bricks[:]:
        if ball.colliderect(brick):
            ball_speed_y = -ball_speed_y
            bricks.remove(brick)
            score += 1

    # Check for game over and level completion
    if ball.bottom >= SCREEN_HEIGHT:
        lives -= 1
        if lives == 0:
            game_over = True
        else:
            ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
            ball_speed_x = 7
            ball_speed_y = -7

    if not bricks:
        level += 1
        ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        ball_speed_x = 7
        ball_speed_y = -7
        for row in range(5 + level):
            for column in range(10):
                brick = pygame.Rect(column * BRICK_WIDTH, row * BRICK_HEIGHT + 50, BRICK_WIDTH, BRICK_HEIGHT)
                bricks.append(brick)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the paddle, ball, and bricks
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    for brick in bricks:
        pygame.draw.rect(screen, BRICK_COLORS[bricks.index(brick) % 3], brick)

    # Display the score, level, and lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (SCREEN_WIDTH - 150, 10))
    screen.blit(lives_text, (10, SCREEN_HEIGHT - 40))

    # Update the screen
    pygame.display.flip()

    # Control the game speed
    pygame.time.delay(30)

# Game over screen
font = pygame.font.Font(None, 72)
game_over_text = font.render("Game Over", True, WHITE)
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
pygame.display.flip()

# Wait for a few seconds before closing the game
pygame.time.delay(3000)

# Quit Pygame
pygame.quit()

# Exit the program
sys.exit()