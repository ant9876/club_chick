from doctest import master
import os
import pygame
from pygame.draw_py import draw_polygon
from pygame.examples.cursors import image

pygame.init()

screen = pygame.display.set_mode((800, 800))

clock = pygame.time.Clock()

master_list = []

house_list = []


is_touching = False

first_draw = True


chick_left = os.path.expanduser("chick_left.png")
chick_right = os.path.expanduser("chick_right.png")
chick_front = os.path.expanduser("chick_front.png")
chick_back = os.path.expanduser("chick_back.png")
tree_one = os.path.expanduser("tree_one.png")
bush_one = os.path.expanduser("bush_one.png")


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
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path)
        super().__init__(x, y, self.image.get_width(), self.image.get_height())

    def draw(self):
        screen.blit(self.image, (self.x, self.y))  # Draw the tree image



class Bush(Object):
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path)
        super().__init__(x, y, self.image.get_width(), self.image.get_height())
    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class House(Object):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height)
        self.image = pygame.image.load(image_path)



    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        door_rect = pygame.Rect(self.x + 133, self.y + 188, 35, 51)
        pygame.draw.rect(screen, "pink", door_rect)

    def get_rect(self):
        return pygame.Rect(self.x + 133, self.y + 188, 35, 51)



player = Player(chick_front, chick_back, chick_right, chick_left)


master_list.append(Tree(500, 300,  tree_one))
master_list.append(Tree(-50, 300,  tree_one))
house_1 = os.path.expanduser("house1.png")
house_list.append(House(300, 200, 300, 300, house_1))


for i in range(0,40):
    master_list.append(Bush(-600+i*110,900,bush_one))

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

        # Render the four lines of text
        font = pygame.font.SysFont('Courier New', 24)  # Font size 36
        text1_surface = font.render("Welcome to:", True, (0, 0, 0))  # First line: "Welcome to:"
        text2_surface = font.render("House!", True, (0, 0, 0))  # Second line: "house_name_tbd"
        text3_surface = font.render("Type 'A' if you", True, (0, 0, 0))  # Third line: "Type A"
        text4_surface = font.render("wish to enter.", True, (0, 0, 0))  # Fourth line: "to enter the house"

        # Get the rects for the text surfaces and center them
        text1_rect = text1_surface.get_rect(center=(popup_rect.centerx, popup_rect.centery - 50))  # First line
        text2_rect = text2_surface.get_rect(center=(popup_rect.centerx, popup_rect.centery - 20))  # Second line
        text3_rect = text3_surface.get_rect(center=(popup_rect.centerx, popup_rect.centery + 10))  # Third line
        text4_rect = text4_surface.get_rect(center=(popup_rect.centerx, popup_rect.centery + 40))  # Fourth line

        # Blit the text onto the screen
        screen.blit(text1_surface, text1_rect)
        screen.blit(text2_surface, text2_rect)
        screen.blit(text3_surface, text3_rect)
        screen.blit(text4_surface, text4_rect)


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

                    for house in house_list:
                        house.vx += 3

                elif event.key == pygame.K_RIGHT:

                    player.current_image = player.image3

                    for obj in master_list:
                        obj.vx -= 3

                    for house in house_list:
                        house.vx -= 3

                elif event.key == pygame.K_UP:

                    player.current_image = player.image2

                    for obj in master_list:
                        obj.vy += 3

                    for house in house_list:
                        house.vy += 3

                elif event.key == pygame.K_DOWN:

                    player.current_image = player.image1

                    for obj in master_list:
                        obj.vy -= 3

                    for house in house_list:
                        house.vy -= 3


            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT:

                    for obj in master_list:
                        obj.vx -= 3

                    for house in house_list:
                        house.vx -= 3

                elif event.key == pygame.K_RIGHT:

                    for obj in master_list:
                        obj.vx += 3

                    for house in house_list:
                        house.vx += 3

                elif event.key == pygame.K_UP:

                    for obj in master_list:
                        obj.vy -= 3

                    for house in house_list:
                        house.vy -= 3

                elif event.key == pygame.K_DOWN:

                    for obj in master_list:
                        obj.vy += 3

                    for house in house_list:
                        house.vy += 3


    inside_rect = pygame.Rect(player.x + player.width // 4 + 64, player.y + player.height // 4 + 56, player.width // 2,
                              player.height // 2)
    for obj in master_list:
        obj.update()

    for house in house_list:
        house.update()

    is_touching = False  # Reset the flag at the start of each frame
    for house in house_list:
            door_rect = house.get_rect()  # Get the door rectangle
            if door_rect.colliderect(inside_rect):  # Check if player intersects with the door
                is_touching = True  # Set the flag if the player is touching the door
                show_popup = (player.x, player.y)  # Show the popup only if player is at the door
            else:
                show_popup = None  # Don't



    # Do logical updates here.

    screen.fill((123, 191, 98)) # Fill the display with a solid color

    # Render the graphics here.


    for house in house_list:
        house.draw()

    player.draw()

    for obj in master_list:
        obj.draw()



    pygame.draw.rect(screen, "green", inside_rect)



    if show_popup:
        show_collision_popup()


    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)  # wait until next frame (at 60 FPS)