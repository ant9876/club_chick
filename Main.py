from doctest import master
import os
import pygame
from pygame.draw_py import draw_polygon

pygame.init()

screen = pygame.display.set_mode((600, 600))

clock = pygame.time.Clock()

master_list = []



class Player(pygame.Rect):
    def __init__(self):
        super().__init__(300, 300, 20, 20)

    def draw(self):
        pygame.draw.rect(screen, (245,228,156), self, 0)



class Object(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.vx = 0
        self.vy = 0

    def update(self):
        self.x+=self.vx
        self.y+=self.vy

class Tree(Object):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height)
        self.image = pygame.image.load(image_path)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))  # Draw the tree image


class Rock(Object):
    def draw(self):
        pygame.draw.rect(screen, "brown", self, 0)



player = Player()

tree_one = os.path.expanduser("~/Downloads/pixil-frame-0 (2).png")
master_list.append(Tree(500, 300, 10, 50, tree_one))
master_list.append(Tree(-50, 300, 10, 50, tree_one))
master_list.append(Rock(100,200,12,12))


while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                for obj in master_list:
                    obj.vx += 3
            elif event.key == pygame.K_RIGHT:
                for obj in master_list:
                    obj.vx -= 3
            elif event.key == pygame.K_UP:
                for obj in master_list:
                    obj.vy += 3
            elif event.key == pygame.K_DOWN:
                for obj in master_list:
                    obj.vy -= 3

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                for obj in master_list:
                    obj.vx -= 3
            elif event.key == pygame.K_RIGHT:
                for obj in master_list:
                    obj.vx += 3
            elif event.key == pygame.K_UP:
                for obj in master_list:
                    obj.vy -= 3
            elif event.key == pygame.K_DOWN:
                for obj in master_list:
                    obj.vy += 3

    for obj in master_list:
        obj.update()

    # Do logical updates here.

    screen.fill((123, 191, 98)) # Fill the display with a solid color

    # Render the graphics here.
    player.draw()

    for obj in master_list:
        obj.draw()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)  # wait until next frame (at 60 FPS)
