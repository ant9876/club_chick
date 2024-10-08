from doctest import master
import os
import pygame
from pygame.draw_py import draw_polygon
from pygame.examples.cursors import image

pygame.init()

screen = pygame.display.set_mode((800, 800))

clock = pygame.time.Clock()

master_list = []


is_touching = False

first_draw = True

chick_left = os.path.expanduser("chick_left.png")
chick_right = os.path.expanduser("chick_right.png")
chick_front = os.path.expanduser("chick_front.png")
chick_back = os.path.expanduser("chick_back.png")


class Player(pygame.Rect):
    def __init__(self, image_path1, image_path2, image_path3, image_path4):
        super().__init__(325, 325, 20, 20)
        self.image1 = pygame.image.load(image_path1)
        self.image2 = pygame.image.load(image_path2)
        self.image3 = pygame.image.load(image_path3)
        self.image4 = pygame.image.load(image_path4)
        self.current_image = self.image1

    def draw(self):
        screen.blit(self.current_image, (self.x, self.y))


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


class House(Object):
    def draw(self):
        pygame.draw.rect(screen, "brown", self, 0)



player = Player(chick_front, chick_back, chick_right, chick_left)

tree_one = os.path.expanduser("tree_one.png")
master_list.append(Tree(500, 300, 10, 50, tree_one))
master_list.append(Tree(-50, 300, 10, 50, tree_one))
master_list.append(House(200,300,12,12))

show_popup = None  # Flag to indicate if the pop-up should be shown

def show_collision_popup():
    if is_touching:
        popup_width, popup_height = 250, 150
        popup_rect = pygame.Rect(screen.get_width()/2 - popup_width/2, screen.get_height()/2 - popup_height/2, popup_width, popup_height)

    # Create a transparent surface with SRCALPHA mode
        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)

    # Fill the surface with a semi-transparent color (RGBA)
        popup_surface.fill((200, 200, 200, 200))  # Light gray with 50% opacity

    # Blit the transparent popup surface to the main screen
        screen.blit(popup_surface, popup_rect.topleft)



while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.current_image = player.image4
                    for obj in master_list:
                        obj.vx += 3
                elif event.key == pygame.K_RIGHT:
                    player.current_image = player.image3
                    for obj in master_list:
                        obj.vx -= 3
                elif event.key == pygame.K_UP:
                    player.current_image = player.image2
                    for obj in master_list:
                        obj.vy += 3
                elif event.key == pygame.K_DOWN:
                    player.current_image = player.image1
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



    inside_rect = pygame.Rect(player.x + player.width // 4 + 64, player.y + player.height // 4 + 56, player.width // 2,
                              player.height // 2)
    for obj in master_list:
        obj.update()

    is_touching = False  # Reset the flag at the start of each frame
    for obj in master_list:
        if isinstance(obj, House) and inside_rect.colliderect(obj):
            is_touching = True  # Set to True if the green rect is touching the house
            break  # No need to check further



    inside_rect = pygame.Rect( player.x + player.width // 4 + 64, player.y + player.height // 4 + 56, player.width // 2, player.height // 2)
    for obj in master_list:
        if isinstance(obj, House) and inside_rect.colliderect(obj):
            show_popup = (player.x, player.y)  # Set the flag if a rock collision occurs


    # Do logical updates here.

    screen.fill((123, 191, 98)) # Fill the display with a solid color

    # Render the graphics here.

    player.draw()

    for obj in master_list:
        obj.draw()

    pygame.draw.rect(screen, "green", inside_rect)

    if show_popup:
        show_collision_popup()


    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)  # wait until next frame (at 60 FPS)