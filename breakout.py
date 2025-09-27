import json
import pygame
import sys
import random
from level import Level
from bullet import Bullet
from powerup import Powerup
from brick import Brick
from ball import Ball
from sprite import Sprite
from bricktype import BrickType
from sprites import sprites

DARK_BLUE = (0, 0, 80)
LIGHT_BLUE = (100, 180, 255)

def draw_game():
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    SHADOW_COLOR = (0, 0, 0, 128)  # black, 50% opaque
    shadow_offset = 8
    # Draw brick shadows
    for brick in bricks:
        shadow_rect = brick.rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        shadow_surface.fill(SHADOW_COLOR)
        screen.blit(shadow_surface, (shadow_rect.x, shadow_rect.y))
    # Draw paddle shadow
    paddle_shadow_rect = paddle.copy()
    paddle_shadow_rect.x += shadow_offset
    paddle_shadow_rect.y += shadow_offset
    paddle_shadow_surface = pygame.Surface((paddle_shadow_rect.width, paddle_shadow_rect.height), pygame.SRCALPHA)
    paddle_shadow_surface.fill(SHADOW_COLOR)
    screen.blit(paddle_shadow_surface, (paddle_shadow_rect.x, paddle_shadow_rect.y))
    # Draw paddle
    paddle_color = RED if laser_active else BLUE
    pygame.draw.rect(screen, paddle_color, paddle)
    # Draw ball shadows and balls
    for ball in balls:
        ball_shadow_rect = ball.rect.copy()
        ball_shadow_rect.x += shadow_offset
        ball_shadow_rect.y += shadow_offset
        ball_shadow_surface = pygame.Surface((ball_shadow_rect.width, ball_shadow_rect.height), pygame.SRCALPHA)
        ball_shadow_surface.fill((0, 0, 0, 0))  # fully transparent
        pygame.draw.ellipse(ball_shadow_surface, SHADOW_COLOR, ball_shadow_surface.get_rect())
        screen.blit(ball_shadow_surface, (ball_shadow_rect.x, ball_shadow_rect.y))
        # Draw mid-blue ball with white outer circle
        pygame.draw.ellipse(screen, WHITE, ball.rect)
        center_radius = ball.radius // 2
        center_rect = pygame.Rect(int(ball.x - center_radius), int(ball.y - center_radius), center_radius * 2, center_radius * 2)
        pygame.draw.ellipse(screen, MID_BLUE, center_rect)
    # Draw bricks
    for brick in bricks:
        draw_sprite(brick.sprite_idx, brick.rect.x, brick.rect.y, screen,3.0)
    # Draw powerup shadows
    for powerup in powerups:
        shadow_rect = powerup.rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        shadow_surface.fill(SHADOW_COLOR)
        screen.blit(shadow_surface, (shadow_rect.x, shadow_rect.y))
    # Draw powerups
    for powerup in powerups:
        pygame.draw.rect(screen, powerup.colour, powerup.rect)
        small_font = pygame.font.SysFont(None, font.get_height() // 2)
        type_text = small_font.render(str(powerup.type), True, WHITE)
        text_rect = type_text.get_rect(center=powerup.rect.center)
        screen.blit(type_text, text_rect)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {player_lives}", True, WHITE)
    screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))
    screen.blit(score_text, (10, 10))

    # Display current bat powerup type at top center
    bat_powerup_text = None
    if laser_active:
        bat_powerup_text = "Laser"
    elif widebat_active:
        bat_powerup_text = "Wide Bat"
    elif powerball_active:
        bat_powerup_text = "Power Ball"
    # You can add more types here if you add more bat effects
    if bat_powerup_text:
        powerup_display = font.render(bat_powerup_text, True, WHITE)
        powerup_rect = powerup_display.get_rect(center=(SCREEN_WIDTH // 2, 20))
        screen.blit(powerup_display, powerup_rect)
    if paused:
        pause_font = pygame.font.SysFont(None, 72)
        pause_text = pause_font.render('Paused', True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(pause_text, pause_rect)
    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet.rect)
    pygame.display.flip()

def draw_sprite(sprite, x, y, surface: pygame.Surface, scale=1.0):
    """
    Draws a sprite from the spritesheet at position (x, y) on the main screen, scaled by 'scale'.
    Args:
        sprite: index into the sprites array
        x, y: position to draw the sprite
        scale: multiplier to scale the sprite size
    """
    sprite_rect = sprites[sprite].rect
    sprite_image = SPRITE_SHEET.subsurface(sprite_rect)
    if scale != 1.0:
        new_size = (int(sprite_rect.width * scale), int(sprite_rect.height * scale))
        sprite_image = pygame.transform.scale(sprite_image, new_size)
    surface.blit(sprite_image, (x, y))

# Game settings
SCALE = 3
SCREEN_WIDTH, SCREEN_HEIGHT = 224 * SCALE, 256 * SCALE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Breakout')
clock = pygame.time.Clock()

# Initialize array of 10 BrickType objects
brick_types = [BrickType(sprite_idx=i, hits=(i % 3) + 1) for i in range(10)]

# Load sprite sheet and create background subsurface after display init
SPRITE_SHEET = pygame.image.load('sprites.png').convert_alpha()
BACKGROUND_IMAGE = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
for y in range(0, SCREEN_HEIGHT, 32 * SCALE):
    for x in range(0, SCREEN_WIDTH, 24 * SCALE):
        draw_sprite(20, x, y, BACKGROUND_IMAGE, 3.0)

# Paddle
paddle_width, paddle_height = 32 * SCALE, 8 * SCALE
paddle = pygame.Rect(SCREEN_WIDTH // 2 - paddle_width // 2, SCREEN_HEIGHT - 64, paddle_width, paddle_height)
paddle_speed = 8

# Ball settings
BALL_RADIUS = 6
BALL_SPEED_X = 5
BALL_SPEED_Y = -5
MID_BLUE = (0, 80, 200)

# Initialize balls
balls = [Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SPEED_X, BALL_SPEED_Y, BALL_RADIUS)]


brick_rows = 8
brick_cols = 13
BRICK_GAP = 0
brick_width = 16 * SCALE
brick_height = 8 * SCALE
bricks = []

for row in range(brick_rows):
    for col in range(brick_cols):
        x = 24 + col * (brick_width + BRICK_GAP)
        y = 64 + row * (brick_height + BRICK_GAP)
        bricks.append(Brick(pygame.Rect(x, y, brick_width, brick_height), brick_types[row]))

score = 0

player_lives = 3
font = pygame.font.SysFont(None, 36)


# Powerup effect tracking
widebat_active = False
powerball_active = False
laser_active = False


# Powerup settings
POWERUP_WIDTH = 32
POWERUP_HEIGHT = 12
POWERUP_COLOR_RED = (255, 0, 0)
POWERUP_COLOR_BLUE = (0, 120, 255)
POWERUP_COLOR_GREY = (128, 128, 128)
POWERUP_COLOR_BLACK = (0, 0, 0)
POWERUP_CHANCE = 0.5  # 20% chance to drop
POWERUP_SPEED = 4


powerups = []  # List of active powerups
bullets = []  # List of active bullets
running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
        if event.type == pygame.MOUSEMOTION:
            mouse_x = event.pos[0]
            paddle.centerx = mouse_x
            # Clamp paddle within screen
            if paddle.left < 0:
                paddle.left = 0
            if paddle.right > SCREEN_WIDTH:
                paddle.right = SCREEN_WIDTH
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and laser_active:
                # Fire bullet from center of paddle, but only if fewer than 2 bullets
                if len(bullets) < 2:
                    bullet_x = paddle.centerx
                    bullet_y = paddle.top
                    bullets.append(Bullet(bullet_x, bullet_y))

    current_time = pygame.time.get_ticks()
    # Remove powerup expiration checks

    if not paused:
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
            paddle.x += paddle_speed


        # Ball movement
        for ball in balls[:]:
            ball.x += ball.speed_x
            ball.y += ball.speed_y

        # Powerup collision with paddle
        for powerup in powerups[:]:
            if powerup.rect.colliderect(paddle):
                # Reset all bat powerup effects before applying new one
                paddle.width = paddle_width
                widebat_active = False
                powerball_active = False
                laser_active = False
                # Apply new powerup
                if powerup.type == Powerup.WIDEBAT:
                    paddle.width = paddle_width * 2
                    widebat_active = True
                elif powerup.type == Powerup.MULTIBALL:
                    # Spawn two new balls at the first ball's location with split angles
                    if balls:
                        main_ball = balls[0]
                        balls.append(Ball(main_ball.x, main_ball.y, main_ball.speed_x - 2, -abs(main_ball.speed_y)))
                        balls.append(Ball(main_ball.x, main_ball.y, main_ball.speed_x + 2, -abs(main_ball.speed_y)))
                elif powerup.type == Powerup.POWERBALL:
                    powerball_active = True
                elif powerup.type == Powerup.LASER:
                    laser_active = True
                # Remove powerup after collection
                powerups.remove(powerup)

        # Ball collision with walls, paddle, bricks
        for ball in balls[:]:
            # Walls
            if ball.rect.left <= 0 or ball.rect.right >= SCREEN_WIDTH:
                ball.speed_x *= -1
            if ball.rect.top <= 0:
                ball.speed_y *= -1
            if ball.rect.bottom >= SCREEN_HEIGHT:
                balls.remove(ball)
                if not balls:
                    player_lives -= 1
                    # Reset all bat powerup effects when life is lost
                    paddle.width = paddle_width
                    widebat_active = False
                    powerball_active = False
                    laser_active = False
                    if player_lives == -1:
                        # Game over
                        game_over_font = pygame.font.SysFont(None, 72)
                        game_over_text = game_over_font.render('GAME OVER', True, RED)
                        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                        screen.blit(game_over_text, text_rect)
                        pygame.display.flip()
                        waiting = True
                        while waiting:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event.type == pygame.KEYDOWN:
                                    waiting = False
                        running = False
                    else:
                        # Reset balls
                        balls = [Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SPEED_X, BALL_SPEED_Y, BALL_RADIUS)]
                continue
            # Paddle
            if ball.rect.colliderect(paddle):
                ball.speed_y *= -1
                offset = (ball.rect.centerx - paddle.centerx) / (paddle_width // 2)
                max_angle = 7
                ball.speed_x = int(offset * max_angle)
                if ball.speed_x == 0:
                    ball.speed_x = random.choice([-2, 2])
            # Bricks
            for brick in bricks[:]:
                if ball.rect.colliderect(brick.rect):
                    if powerball_active:
                        bricks.remove(brick)
                        score += 10
                        # Powerup drop
                        if len(powerups) < 2 and random.random() < POWERUP_CHANCE:
                            powerup_x = brick.rect.centerx - POWERUP_WIDTH // 2
                            powerup_y = brick.rect.centery - POWERUP_HEIGHT // 2
                            powerups.append(Powerup(powerup_x, powerup_y))
                        # Do not bounce, just continue
                        continue
                    else:
                        if brick.hit():
                            bricks.remove(brick)
                            score += 10
                            # Powerup drop
                            if len(powerups) < 2 and random.random() < POWERUP_CHANCE:
                                powerup_x = brick.rect.centerx - POWERUP_WIDTH // 2
                                powerup_y = brick.rect.centery - POWERUP_HEIGHT // 2
                                powerups.append(Powerup(powerup_x, powerup_y))
                        else:
                            score += 5
                        ball.speed_y *= -1
                        break

        # Move powerups
        for powerup in powerups[:]:
            powerup.y += POWERUP_SPEED
            if powerup.y > SCREEN_HEIGHT:
                powerups.remove(powerup)
        # Move bullets
        for bullet in bullets[:]:
            bullet.y -= bullet.speed
            if bullet.y < 0:
                bullets.remove(bullet)
        # Bullet collision with bricks
        for bullet in bullets[:]:
            for brick in bricks[:]:
                if bullet.rect.colliderect(brick.rect):
                    if brick.hit():
                        bricks.remove(brick)
                        score += 10
                    else:
                        score += 5
                    bullets.remove(bullet)
                    break
        # Check for stage clear
        if len(bricks) == 0:
            stage_clear_font = pygame.font.SysFont(None, 72)
            stage_clear_text = stage_clear_font.render('STAGE CLEAR', True, YELLOW)
            stage_clear_rect = stage_clear_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(stage_clear_text, stage_clear_rect)
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        waiting = False
            running = False
    draw_game()
    clock.tick(FPS)

pygame.quit()
sys.exit()
