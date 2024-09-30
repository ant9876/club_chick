from doctest import master

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
        pygame.draw.rect(screen, "gray", self, 0)



class Object(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.vx = 0
        self.vy = 0

    def update(self):
        self.x+=self.vx
        self.y+=self.vy

class Tree(Object):
    def draw(self):
        pygame.draw.rect(screen, "green", self, 0)

class House(Object):
    def draw(self):
        pygame.draw.rect(screen, "brown", self, 0)



player = Player()


master_list.append(Tree(500, 300, 10, 50))
master_list.append(Tree(-50, 300, 10, 50))
master_list.append(House(200,300,12,12))

show_popup = None  # Flag to indicate if the pop-up should be shown

def show_collision_popup():
    popup_width, popup_height = 200, 100
    popup_rect = pygame.Rect(200, 250, popup_width, popup_height)
    pygame.draw.rect(screen, "lightgray", popup_rect)


while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if show_popup is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    for obj in master_list:
                        obj.y =- 1
                        obj.vx = 0
                        obj.vy = 0
                    show_popup = None




        else:
            if event.type == pygame.KEYDOWN:
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
        if not show_popup:
            obj.update()

    for obj in master_list:
        if isinstance(obj, House) and player.colliderect(obj):
            show_popup = (obj.x, obj.y)  # Set the flag if a rock collision occurs


    # Do logical updates here.

    screen.fill("white")  # Fill the display with a solid color

    # Render the graphics here.
    player.draw()

    for obj in master_list:
        obj.draw()

    if show_popup:
        show_collision_popup()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)  # wait until next frame (at 60 FPS)
