from doctest import master
import os
import pygame
from pygame.draw_py import draw_polygon
from pygame.examples.cursors import image
import BubbleGame

pygame.init()

PLAYER_SPEED = 3
is_hungry = False
is_thirsty = False
in_water = False
has_apples = False

master_list = []
house_list = []

first_draw = True
game_state = "map"
entered_game = False
space_pressed = False
in_barn = False
in_house = False
game_state = "map"  # Game state to track what screen you're on
entered_game = False  # Flag to track if we entered the game screen
space_pressed = False  # Flag to track if the space bar is pressed
apples_count=0
total_count =0


chick_left = os.path.expanduser("chick_left.png")
chick_right = os.path.expanduser("chick_right.png")
chick_front = os.path.expanduser("chick_front.png")
chick_back = os.path.expanduser("chick_back.png")
tree_one = os.path.expanduser("tree_one.png")
bush_one = os.path.expanduser("bush_one.png")
house_1 = os.path.expanduser("house1.png")
apple_one = os.path.expanduser("tree_apple.png")
river = os.path.expanduser("river.png")
barn_1 = os.path.expanduser("barn.png")
garden_one = os.path.expanduser('garden.png')

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


class River(Object):
    def __init__(self,x, y, image_path):
        self.image=pygame.image.load(image_path)
        super().__init__(x, y, image_path)


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

            # Create a transparent surface with SRCALPHA mode
            popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)

            # Fill the surface with a semi-transparent color (RGBA)
            popup_surface.fill((200, 200, 200, 200))  # Light gray with 50% opacity

            # Blit the transparent popup surface to the main screen
            screen.blit(popup_surface, popup_rect.topleft)

            # Load and render text in Times New Roman
            font = pygame.font.SysFont("Times New Roman", 30)  # Set to Times New Roman with size 30

            # Split the text into three lines
            text1 = "Press A by any"
            text2 = "apple tree to"
            text3 = "collect Apples!"

            # Render the first line
            text1_surface = font.render(text1, True, (0, 0, 0))
            text1_rect = text1_surface.get_rect(
                center=(popup_rect.centerx, popup_rect.centery - 40))  # Adjust y-position for centering

            # Render the second line
            text2_surface = font.render(text2, True, (0, 0, 0))
            text2_rect = text2_surface.get_rect(
                center=(popup_rect.centerx, popup_rect.centery))  # Adjust y-position for centering

            # Render the third line
            text3_surface = font.render(text3, True, (0, 0, 0))
            text3_rect = text3_surface.get_rect(
                center=(popup_rect.centerx, popup_rect.centery + 40))  # Adjust y-position for centering

            # Blit the text onto the screen
            screen.blit(text1_surface, text1_rect)
            screen.blit(text2_surface, text2_rect)
            screen.blit(text3_surface, text3_rect)



class Bush(Object):
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path)
        super().__init__(x, y, image_path)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Garden(Object):
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

    # Check the player's current status and set the text accordingly
    if is_hungry and is_thirsty:
        stats_text = f"Welcome to club_chick!       Apples: {apples_count}      //      Health: Hungry & Thirsty :("
    elif is_thirsty:
        stats_text = f"Welcome to club_chick!       Apples: {apples_count}      //      Health: Thirsty :/"
    elif is_hungry:
        stats_text = f"Welcome to club_chick!       Apples: {apples_count}      //      Health: Hungry :/"
    else:
        stats_text = f"Welcome to club_chick!       Apples: {apples_count}      //      Health: Happy!"

    # Render and display the text
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

class HorseGame:
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
player_rect = pygame.Rect(player.x + player.width // 4 + 64, player.y + player.height // 4 + 56, player.width // 2, player.height // 2)

master_list.append(Tree(830, 220, tree_one))
master_list.append(Tree(-180, 220, tree_one))


house_list.append(House(650, 80, house_1))
house_list.append(House(-150, 80, barn_1))


for i in range(0,20):
    master_list.append(River(-600+i*100, 760, river))
for i in range(0, 40):
    master_list.append(Bush(-600 + i * 110, 680, bush_one))
for i in range(-2, 3):
    master_list.append(Apple_Tree(i*100+350,200,apple_one))
    master_list.append(Apple_Tree(i * 100 + 350, 400, apple_one))
for i in range(-2, 4):
    master_list.append(Apple_Tree(i * 100 + 300, 300, apple_one))


master_list.append(Garden(-550, 200, garden_one))

show_popup = None  # Flag to indicate if the pop-up should be shown


def show_collision_popup():
        popup_width, popup_height = 250, 150
        popup_rect = pygame.Rect(screen.get_width() / 2 - popup_width / 2, screen.get_height() / 2 - popup_height / 2,
                                 popup_width, popup_height)

        # Create a transparent surface with SRCALPHA mode
        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)

        # Fill the surface with a semi-transparent color (RGBA)
        popup_surface.fill((200, 200, 200, 200))  # Light gray with 50% opacity

        # Blit the transparent popup surface to the main screen
        screen.blit(popup_surface, popup_rect.topleft)

        if in_barn:
            font = pygame.font.SysFont('Courier New', 24)
            text1_surface = font.render("Welcome to:", True, (0, 0, 0))

            text2_surface = font.render("Barn!", True, (0, 0, 0))
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

        if in_house:
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


# Function to stop the player's movement
def stop_movement():
    for obj in master_list:
        obj.vx = 0
        obj.vy = 0
    for house in house_list:
        house.vx = 0
        house.vy = 0

# Function to show the game screen text
def show_game_screen():
    font = pygame.font.SysFont('Courier New', 20)
    if game_state == "blank":
        font = pygame.font.SysFont('Courier New', 20)
        text_surface = font.render("Welcome to house game! Press 'space' continue or 'e' to exit.", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
        screen.blit(text_surface, text_rect)
    if game_state == "barn":
        font = pygame.font.SysFont('Courier New', 20)
        text_surface = font.render("Welcome to barn game! Press 'space' continue or 'e' to exit.", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(text_surface, text_rect)
player_speed = 3

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if apples_count>1:
            has_apples = True

        total_count+=1
        if total_count%100==0:
            is_thirsty=True
        if total_count%20==0:
            is_hungry=True



        if event.type == pygame.KEYDOWN:
            if is_hungry and event.key == pygame.K_f:
                is_hungry = False
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
                            if player_rect.colliderect(obj.get_rect()):
                                obj.collect_apples()


                elif event.key == pygame.K_h:

                    if in_house:
                        game_state = "blank"  # Change the game state to 'blank' when 'H' key is pressed
                        entered_game = True  # Set the flag for entering the house
                        space_pressed = False

                    if in_barn:
                        game_state = "barn"  # Change the game state to 'blank' when 'H' key is pressed
                        entered_game = True  # Set the flag for entering the house
                        space_pressed = False


            # Stop movement when the keys are released
            elif event.type == pygame.KEYUP and game_state == "map":
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    stop_movement()  # Stop all movement

            # Handle input in the "blank" state
            elif game_state == "blank" or game_state == "barn":
                if event.key == pygame.K_e:
                    game_state = "map"  # Return to the original map if 'E' is pressed
                    entered_game = False  # Reset the flag when exiting
                elif event.key == pygame.K_SPACE:
                    space_pressed = True
                    if game_state == "blank":
                        apples_collected = bubble_game.bubble_main()
                        apples_count += apples_collected

        if event.type == pygame.KEYUP and game_state == "map":
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                for obj in master_list:
                    obj.vx = 0  # Stop horizontal movement
                for house in house_list:
                    house.vx = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                for obj in master_list:
                    obj.vy = 0  # Stop vertical movement
                for house in house_list:
                    house.vy = 0

    # Handle game state "map" logic
    if game_state == "map":
        in_barn = False
        in_house = False
        in_water = False
        # Reset the flag at the start of each frame

        for obj in master_list:
            obj.update()
            if isinstance(obj, River) and player_rect.colliderect(obj):
                in_water = True
                if in_water and is_thirsty:
                    is_thirsty = False
                    break




        for house in house_list:
            house.update()
        for house in house_list:
            inside_rect = pygame.Rect(player.x + player.width // 4 + 64, player.y + player.height // 4 + 56,
                                      player.width // 2, player.height // 2)
            door_rect_1 = house_list[0].get_rect()
            door_rect_2 = house_list[1].get_rect()
            if door_rect_1.colliderect(inside_rect):
                in_house = True
                in_barn = False
                show_popup = (player.x, player.y)
                break
            if door_rect_2.colliderect(inside_rect):
                in_barn = True
                in_house = False
                show_popup = (player.x, player.y)
            else:
                show_popup = None
                in_barn = False
                in_house = False

    # Handle game state "blank" logic
    if game_state == "blank" or game_state == "barn":
        screen.fill((255, 255, 255))  # Blank white screen
        if entered_game and not space_pressed:
            show_game_screen()


    if game_state == "map":
        screen.fill((123, 191, 98))  # Fill the display with a solid color

        # Render the graphics here.

        for house in house_list:
                house.draw()

        player.draw()




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

        font = pygame.font.SysFont("Courier New", 20)
        # Create the text to display the in_water status
        status_text = f"In Water: {'Yes' if in_water else 'No'}"
        text_surface = font.render(status_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(topleft=(10, 10))  # Position it at the top left corner
        screen.blit(text_surface, text_rect)
    #pygame.display.update()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)  # wait until next frame (at 60 FPS)