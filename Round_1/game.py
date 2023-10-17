import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 80, 20
WHITE = (255, 255, 255)
PADDLE_SPEED = 10
BALL_SPEED_X, BALL_SPEED_Y = 5, 5
BRICK_ROWS, BRICK_COLS = 6, 10
MAX_LIVES = 3

# Colors for bricks
BRICK_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Create a font for displaying text
font = pygame.font.Font(None, 36)

# Create the paddle
paddle = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)

# Create the ball
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, BALL_RADIUS)
ball_speed = [BALL_SPEED_X, -BALL_SPEED_Y]

# Create bricks with random colors
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick = pygame.Rect(col * (BRICK_WIDTH + 5), row * (BRICK_HEIGHT + 5) + 50, BRICK_WIDTH, BRICK_HEIGHT)
        brick_color = random.choice(BRICK_COLORS)
        bricks.append((brick, brick_color))

# Life counter
lives = MAX_LIVES

# Score counter
score = 0

# Game over flag
game_over = False

# Function to display a message and buttons
def display_message(message, button1, button2):
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    screen.blit(button1[0], button1[1])
    screen.blit(button2[0], button2[1])

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_play_again.collidepoint(x, y):
                    # Reset the game
                    lives = MAX_LIVES
                    score = 0
                    bricks = []
                    for row in range(BRICK_ROWS):
                        for col in range(BRICK_COLS):
                            brick = pygame.Rect(col * (BRICK_WIDTH + 5), row * (BRICK_HEIGHT + 5) + 50, BRICK_WIDTH, BRICK_HEIGHT)
                            brick_color = random.choice(BRICK_COLORS)
                            bricks.append((brick, brick_color))
                    game_over = False
                elif button_quit.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-PADDLE_SPEED, 0)
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.move_ip(PADDLE_SPEED, 0)

        ball.move_ip(ball_speed)

        # Ball collisions
        if ball.left < 0 or ball.right > WIDTH:
            ball_speed[0] = -ball_speed[0]
        if ball.top < 0:
            ball_speed[1] = -ball_speed[1]

        if ball.colliderect(paddle):
            ball_speed[1] = -ball_speed[1]

        for brick, brick_color in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove((brick, brick_color))
                ball_speed[1] = -ball_speed[1]
                score += 10  # Increase the score when a brick is hit

# Game over condition
        if ball.bottom > HEIGHT:
            lives -= 1
            if lives == 0:
                game_over = True
                game_over_message = "Game Over"
                button_play_again_text = font.render("Play Again", True, WHITE)
                button_quit_text = font.render("Quit", True, WHITE)
                button_play_again = (button_play_again_text, button_play_again_text.get_rect(center=(WIDTH // 3, HEIGHT // 2 + 50)))
                button_quit = (button_quit_text, button_quit_text.get_rect(center=(2 * WIDTH // 3, HEIGHT // 2 + 50)))
            else:
                # Reset the paddle and ball
                paddle = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)
                ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, BALL_RADIUS)
                ball_speed = [BALL_SPEED_X, -BALL_SPEED_Y]

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        for brick, brick_color in bricks:
            pygame.draw.rect(screen, brick_color, brick)

        # Display the number of lives and score in visible regions
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(lives_text, (10, 10))
        screen.blit(score_text, (WIDTH - 120, 10))
    else:
        display_message(game_over_message, button_play_again, button_quit)

    pygame.display.flip()
    pygame.time.delay(30)