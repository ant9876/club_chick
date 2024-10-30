import pygame
import math
import random

pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Horse Game")

background_image = pygame.image.load("horses_clear.png")
background_image = pygame.transform.scale(background_image, (width, height))

apple_image = pygame.image.load("apple.png")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ball_radius = 15
ball_speed = 15

initial_ball_position = (550, height - ball_radius)
ball_x, ball_y = initial_ball_position

def pick_a_color():
    colors = ['#C08B61', '#ef513d', '#C00425', '#59010F', '#FB8345']
    return pygame.Color(random.choice(colors))

targets = {
    pygame.K_1: (190, 535),
    pygame.K_2: (370, 485),
    pygame.K_3: (550, 420),
    pygame.K_4: (730, 370)
}

moving = False
target_x, target_y = ball_x, ball_y
direction_x, direction_y = 0, 0

current_prompt_key = random.choice(list(targets.keys()))

font = pygame.font.Font(None, 36)
ball_color = pick_a_color()

running = True
while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            if event.key == current_prompt_key and not moving:
                target_x, target_y = targets[event.key]

                dx, dy = target_x - ball_x, target_y - ball_y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                direction_x, direction_y = dx / distance, dy / distance
                moving = True
    if moving:
        ball_x += direction_x * ball_speed
        ball_y += direction_y * ball_speed

        if math.hypot(target_x - ball_x, target_y - ball_y) < ball_speed:
            moving = False
            ball_x, ball_y = initial_ball_position
            ball_color = pick_a_color()

            current_prompt_key = random.choice(list(targets.keys()))

    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    image_rect = apple_image.get_rect(center=(ball_x, ball_y))
    screen.blit(apple_image, image_rect)

    prompts = {
        pygame.K_1: "Mr. Hopps is hungry! Press 1 to feed him!",
        pygame.K_2: "Anishka is hungry! Press 2 to feed her!",
        pygame.K_3: "Arpi is hungry! Press 3 to feed her!",
        pygame.K_4: "Miriam is hungry! Press 4 to feed her!"
    }
    prompt_text = font.render(prompts[current_prompt_key], True, BLACK)
    screen.blit(prompt_text, (50, 50))

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
