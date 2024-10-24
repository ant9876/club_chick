from doctest import master
import os
import pygame
from pygame.draw_py import draw_polygon
from pygame.examples.cursors import image
import BubbleGame

pygame.init()

PLAYER_SPEED = 3

master_list = []
house_list = []

is_touching = False
first_draw = True
game_state = "map"
entered_game = False
space_pressed = False
apples_count=0

chick_left = os.path.expanduser("chick_left.png")
chick_right = os.path.expanduser("chick_right.png")
chick_front = os.path.expanduser("chick_front.png")
chick_back = os.path.expanduser("chick_back.png")
tree_one = os.path.expanduser("tree_one.png")
bush_one = os.path.expanduser("bush_one.png")
house_1 = os.path.expanduser("house1.png")
apple_one = os.path.expanduser("tree_apple.png")
river = os.path.expanduser("river.png")

bubble_game = BubbleGame

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

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
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path)
        super().__init__(x, y, self.image.get_width(), self.image.get_height())
        self.vx = 0
        self.vy = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Tree(Object):
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path)
        self.interacted = False
        super().__init__(x, y, image_path)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Apple_Tree(Tree):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)
        self.show_popup = False

    def get_rect(self):
        return pygame.Rect(self.x+15, self.y+15, 50, 45)

    def first_interact(self):
        if not self.interacted:
            self.show_popup = True
            self.interacted = True

    def leave_interaction(self):
        self.show_popup = False

    def collect_apples(self):
        global apples_count
        apples_count += 1

    def draw_popup(self):
        if self.show_popup:
            popup_width, popup_height = 250, 150
            popup_rect = pygame.Rect(screen.get_width() / 2 - popup_width / 2,
                                     screen.get_height() / 2 - popup_height / 2, popup_width, popup_height)

            popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
            popup_surface.fill((200, 200, 200, 200))
            screen.blit(popup_surface, popup_rect.topleft)
            font = pygame.font.SysFont("Times New Roman", 30)
            text1 = "Press A by any"
            text2 = "apple tree to"
            text3 = "collect Apples!"
            text1_surface = font.render(text1, True, (0, 0, 0))
            text1_rect = text1_surface.get_rect(
                center=(popup_rect.centerx, popup_rect.centery - 40))
            text2_surface = font.render(text2, True, (0, 0, 0))
            text2_rect = text2_surface.get_rect(
                center=(popup_rect.centerx, popup_rect.centery))
            text3_surface = font.render(text3, True, (0, 0, 0))
            text3_rect = text3_surface.get_rect(
                center=(popup_rect.centerx, popup_rect.centery + 40))
            screen.blit(text1_surface, text1_rect)
            screen.blit(text2_surface, text2_rect)
            screen.blit(text3_surface, text3_rect)

class Bush(Object):
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path)
        super().__init__(x, y, image_path)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class House(Object):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)
        self.image = pygame.image.load(image_path)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        # door_rect = pygame.Rect(self.x + 133, self.y + 188, 35, 51)
        # pygame.draw.rect(screen, "pink", door_rect)

    def get_rect(self):
        return pygame.Rect(self.x + 133, self.y + 188, 35, 51)

def draw_stats_bar(apples_count):
    bar_height = 30
    bar_rect = pygame.Rect(0, 0, screen.get_width(), bar_height)
    pygame.draw.rect(screen, (211, 211, 211), bar_rect)
    font = pygame.font.SysFont("Times New Roman", 20)
    stats_text = f"Apples: {apples_count}"
    text_surface = font.render(stats_text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(bar_rect.centerx, bar_rect.centery))
    screen.blit(text_surface, text_rect)

class BubbleGame:
    def __init__(self):
        self.running = True

    def run(self, screen):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.running = False

            screen.fill((0, 0, 255))
            pygame.display.flip()
            clock.tick(60)

player = Player(chick_front, chick_back, chick_right, chick_left)

master_list.append(Tree(500, 300, tree_one))
master_list.append(Tree(-50, 300, tree_one))
master_list.append(Apple_Tree(80,400,apple_one))


house_list.append(House(300, 200, house_1))
for i in range(0,20):
    master_list.append(Object(-600+i*100, 800, river))
for i in range(0, 40):
    master_list.append(Bush(-600 + i * 110, 900, bush_one))

show_popup = None

def show_collision_popup():
    if is_touching:
        popup_width, popup_height = 250, 150
        popup_rect = pygame.Rect(screen.get_width() / 2 - popup_width / 2, screen.get_height() / 2 - popup_height / 2,
                                 popup_width, popup_height)
        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        popup_surface.fill((200, 200, 200, 200))
        screen.blit(popup_surface, popup_rect.topleft)

        font = pygame.font.SysFont('Courier New', 24)
        text1_surface = font.render("Welcome to:", True, (0, 0, 0))
        text2_surface = font.render("House!", True, (0, 0, 0))
        text3_surface = font.render("Type 'H' if you", True, (0, 0, 0))
        text4_surface = font.render("wish to enter.", True, (0, 0, 0))

        text1_rect = text1_surface.get_rect(center=(popup_rect.centerx, popup_rect.centery - 50))
        text2_rect = text2_surface.get_rect(center=(popup_rect.centerx, popup_rect.centery - 20))
        text3_rect = text3_surface.get_rect(center=(popup_rect.centerx, popup_rect.centery + 10))
        text4_rect = text4_surface.get_rect(center=(popup_rect.centerx, popup_rect.centery + 40))

        screen.blit(text1_surface, text1_rect)
        screen.blit(text2_surface, text2_rect)
        screen.blit(text3_surface, text3_rect)
        screen.blit(text4_surface, text4_rect)
def stop_movement():
    for obj in master_list:
        obj.vx = 0
        obj.vy = 0
    for house in house_list:
        house.vx = 0
        house.vy = 0

def show_game_screen():
    font = pygame.font.SysFont('Courier New', 20)
    text_surface = font.render("Welcome to house game! Press 'space' continue or 'e' to exit.", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
    screen.blit(text_surface, text_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if game_state == "map":
                if event.key == pygame.K_LEFT:
                    player.current_image = player.image4
                    for obj in master_list:
                        obj.vx += PLAYER_SPEED
                    for house in house_list:
                        house.vx += PLAYER_SPEED
                elif event.key == pygame.K_RIGHT:
                    player.current_image = player.image3
                    for obj in master_list:
                        obj.vx -= PLAYER_SPEED
                    for house in house_list:
                        house.vx -= PLAYER_SPEED
                elif event.key == pygame.K_UP:
                    player.current_image = player.image2
                    for obj in master_list:
                        obj.vy += PLAYER_SPEED
                    for house in house_list:
                        house.vy += PLAYER_SPEED
                elif event.key == pygame.K_DOWN:
                    player.current_image = player.image1
                    for obj in master_list:
                        obj.vy -= PLAYER_SPEED
                    for house in house_list:
                        house.vy -= PLAYER_SPEED
                elif event.key == pygame.K_a:
                    for obj in master_list:
                        if isinstance(obj, Apple_Tree):
                            player_rect = pygame.Rect(player.x + player.width // 4 + 64, player.y + player.height // 4 + 56, player.width // 2, player.height // 2)
                            if player_rect.colliderect(obj.get_rect()):
                                obj.collect_apples()

                elif event.key == pygame.K_h and is_touching:
                    game_state = "blank"
                    entered_game = True
                    space_pressed = False
            elif event.type == pygame.KEYUP and game_state == "map":
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    stop_movement()

            elif game_state == "blank":
                if event.key == pygame.K_e:
                    game_state = "map"
                    entered_game = False
                elif event.key == pygame.K_SPACE:
                    space_pressed = True
                    apples_collected = bubble_game.bubble_main()
                    apples_count += apples_collected

        if event.type == pygame.KEYUP and game_state == "map":
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                for obj in master_list:
                    obj.vx = 0
                for house in house_list:
                    house.vx = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                for obj in master_list:
                    obj.vy = 0
                for house in house_list:
                    house.vy = 0

    if game_state == "map":
        is_touching = False

        for obj in master_list:
            obj.update()
        for house in house_list:
            house.update()
        for house in house_list:
            inside_rect = pygame.Rect(player.x + player.width // 4 + 64, player.y + player.height // 4 + 56, player.width // 2, player.height // 2)
            door_rect = house.get_rect()
            if door_rect.colliderect(inside_rect):
                is_touching = True
                show_popup = (player.x, player.y)
            else:
                show_popup = None

    if game_state == "blank":
        screen.fill((255, 255, 255))
        if entered_game and not space_pressed:
            show_game_screen()

    if game_state == "map":
        screen.fill((123, 191, 98))

        # Render the graphics here.
        for house in house_list:
                house.draw()

        player.draw()

        for obj in master_list:
                obj.draw()


        for obj in master_list:
            obj.draw()
            if isinstance(obj, Apple_Tree):
                tree_rect = obj.get_rect()
                inside_rect = pygame.Rect(player.x + player.width // 4 + 64, player.y + player.height // 4 + 56, player.width // 2, player.height // 2)
                if inside_rect.colliderect(tree_rect):
                    obj.first_interact()
                else:
                    obj.leave_interaction()

                obj.draw_popup()


        draw_stats_bar(apples_count)

                # Draw the tree's bounding rectangle
                # tree_rect = obj.get_rect()
                # pygame.draw.rect(screen, "green", tree_rect, 2)  # Green rectangle with a 2-pixel border
                # pygame.draw.rect(screen, "green", inside_rect)

        if show_popup:
            show_collision_popup()

    #pygame.display.update()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)  # wait until next frame (at 60 FPS)